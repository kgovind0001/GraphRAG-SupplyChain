import os
import csv
import re
from typing import Optional, Dict, List

from neo4j import GraphDatabase
from dotenv import load_dotenv

from langchain_neo4j import Neo4jGraph
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Neo4jVector
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode

from models import SupplierCountInput, SupplierListInput
from tools import run_supplier_count_query, run_supplier_list_query


class SupplyChainAssistant:
    def __init__(self, nodes_csv="nodes.csv", relationships_csv="relationships.csv"):
        load_dotenv()
        self.NODES_CSV = nodes_csv
        self.RELATIONSHIPS_CSV = relationships_csv
        self.mapping = {
            "Supplier": "Supplier",
            "Manufacturer": "Manufacturer",
            "Distributor": "Distributor",
            "Retailer": "Retailer",
            "Product": "Product"
        }
        self.graph = Neo4jGraph(
            url=os.environ["NEO4J_URI"],
            username=os.environ["NEO4J_USERNAME"],
            password=os.environ["NEO4J_PASSWORD"],
            enhanced_schema=True,
        )
        self.driver = GraphDatabase.driver(
            os.environ["NEO4J_URI"],
            auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"])
        )
        self.embedding = OpenAIEmbeddings(model="text-embedding-3-small", api_key=os.environ["OPENAI_API_KEY"])
        self.neo4j_vector = Neo4jVector.from_existing_graph(
            embedding=self.embedding,
            index_name="supply_chain",
            node_label="Supplier",
            text_node_properties=["description"],
            embedding_node_property="embedding",
        )
        self._prepare_data()
        self._initialize_llm_graph()

    def _get_label_for_type(self, node_type):
        return self.mapping.get(node_type, "Entity")

    def _create_indexes(self):
        with self.driver.session() as session:
            for label in self.mapping.values():
                session.run(f"CREATE CONSTRAINT IF NOT EXISTS FOR (n:{label}) REQUIRE n.id IS UNIQUE")

    def _ingest_nodes(self):
        with self.driver.session() as session:
            with open(self.NODES_CSV, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    node_id = row['id:ID']
                    name = row['name']
                    node_type = row['type']
                    location = row['location']
                    supply_capacity = int(row['supply_capacity'])
                    description = row['description']
                    label = self._get_label_for_type(node_type)
                    if location.strip():
                        query = f"""
                        MERGE (n:{label} {{id:$id}})
                        SET n.name = $name, n.location = $location, 
                            n.description = $description, n.supply_capacity = $supply_capacity
                        """
                        params = {
                            "id": node_id,
                            "name": name,
                            "location": location,
                            "description": description,
                            "supply_capacity": supply_capacity
                        }
                    else:
                        query = f"""
                        MERGE (n:{label} {{id:$id}})
                        SET n.name = $name
                        """
                        params = {"id": node_id, "name": name}
                    session.run(query, params)

    def _ingest_relationships(self):
        with self.driver.session() as session:
            with open(self.RELATIONSHIPS_CSV, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    start_id = row[':START_ID']
                    end_id = row[':END_ID']
                    rel_type = row[':TYPE']
                    product = row['product']
                    if product.strip():
                        query = f"""
                        MATCH (start {{id:$start_id}})
                        MATCH (end {{id:$end_id}})
                        MERGE (start)-[r:{rel_type} {{product:$product}}]->(end)
                        """
                        params = {
                            "start_id": start_id,
                            "end_id": end_id,
                            "product": product
                        }
                    else:
                        query = f"""
                        MATCH (start {{id:$start_id}})
                        MATCH (end {{id:$end_id}})
                        MERGE (start)-[r:{rel_type}]->(end)
                        """
                        params = {
                            "start_id": start_id,
                            "end_id": end_id
                        }
                    session.run(query, params)

    def _prepare_data(self):
        self._create_indexes()
        self._ingest_nodes()
        self._ingest_relationships()


    def _initialize_llm_graph(self):


        @tool("supplier-count", args_schema=SupplierCountInput)
        def supplier_count(
            min_supply_amount: Optional[int],
            max_supply_amount: Optional[int],
            grouping_key: Optional[str],
        ) -> List[Dict]:
            """Calculate the count of Suppliers based on particular filters"""
            return run_supplier_count_query(min_supply_amount, max_supply_amount, grouping_key, self.graph)

        @tool("supplier-list", args_schema=SupplierListInput)
        def supplier_list(
            sort_by: str = "supply_capacity",
            k: int = 4,
            description: Optional[str] = None,
            min_supply_amount: Optional[int] = None,
            max_supply_amount: Optional[int] = None,
        ) -> List[Dict]:
            """List suppliers based on particular filters"""
            return run_supplier_list_query(
                graph=self.graph,
                neo4j_vector=self.neo4j_vector,
                embedding=self.embedding,
                sort_by=sort_by,
                k=k,
                description=description,
                min_supply_amount=min_supply_amount,
                max_supply_amount=max_supply_amount
            )

        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.tools = [supplier_list, supplier_count]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.sys_msg = SystemMessage(content="You are a helpful assistant tasked with finding and explaining relevant information about the supply chain.")

        def assistant(state: MessagesState):
            return {"messages": [self.llm_with_tools.invoke([self.sys_msg] + state["messages"])]}

        builder = StateGraph(MessagesState)
        builder.add_node("assistant", assistant)
        builder.add_node("tools", ToolNode(self.tools))
        builder.add_edge(START, "assistant")
        builder.add_conditional_edges("assistant", tools_condition)
        builder.add_edge("tools", "assistant")
        self.react_graph = builder.compile()

    def query(self, user_query: str):
        messages = [HumanMessage(content=user_query)]
        result = self.react_graph.invoke({"messages": messages})
        return result["messages"][-1].content 
