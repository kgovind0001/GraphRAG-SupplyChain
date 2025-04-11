from typing import Optional, Dict, List
import logging 

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_supplier_count_query(
    min_supply_amount: Optional[int],
    max_supply_amount: Optional[int],
    grouping_key: Optional[str],
    graph
) -> List[Dict]:
    filters = []
    params = {}

    if min_supply_amount is not None:
        filters.append("t.supply_capacity >= $min_supply_amount")
        params["min_supply_amount"] = min_supply_amount
    if max_supply_amount is not None:
        filters.append("t.supply_capacity <= $max_supply_amount")
        params["max_supply_amount"] = max_supply_amount

    where_clause = " AND ".join(filters)

    cypher_statement = "MATCH (t:Supplier) "
    if where_clause:
        cypher_statement += f"WHERE {where_clause} "
    if grouping_key:
        cypher_statement += f"RETURN t.{grouping_key} AS {grouping_key}, count(t) AS supplier_count"
    else:
        cypher_statement += "RETURN count(t) AS supplier_count"

    logging.info(f"STATEMENT: {cypher_statement}")
    logging.info(f"PARAMS: {params}")
    data = graph.query(cypher_statement, params=params)
    logging.info(f"RESPONSE: {data}")
    return data


def run_supplier_list_query(
    graph, 
    neo4j_vector,
    embedding,  
    sort_by: str = "supply_capacity",
    k : int = 4,
    description: Optional[str] = None,
    min_supply_amount: Optional[int] = None,
    max_supply_amount: Optional[int] = None,
) -> List[Dict]:
    """List suppliers based on particular filters"""

    # Handle vector-only search when no prefiltering is applied
    if description and not min_supply_amount and not max_supply_amount:
        return neo4j_vector.similarity_search(description, k=k)
    filters = [
        ("t.supply_capacity >= $min_supply_amount", min_supply_amount),
        ("t.supply_capacity <= $max_supply_amount", max_supply_amount)
    ]
    params = {
        key.split("$")[1]: value for key, value in filters if value is not None
    }
    where_clause = " AND ".join([condition for condition, value in filters if value is not None])
    cypher_statement = "MATCH (t:Supplier) "
    if where_clause:
        cypher_statement += f"WHERE {where_clause} "
    # Sorting and returning
    cypher_statement += " RETURN t.name AS name, t.location AS location, t.description as description, t.supply_capacity AS supply_capacity ORDER BY "
    if description:
        cypher_statement += (
            "vector.similarity.cosine(t.embedding, $embedding) DESC "
        )
        params["embedding"] = embedding.embed_query(description)
    elif sort_by == "supply_capacity":
        cypher_statement += "t.supply_capacity DESC "
    else:
        # Fallback or other possible sorting
        cypher_statement += "t.year DESC "
    cypher_statement += " LIMIT toInteger($limit)"
    params["limit"] = 100
    logging.info(f"STATEMENT: {cypher_statement}")
    logging.info(f"PARAMS: {params}")
    data = graph.query(cypher_statement, params=params)
    logging.info(f"RESPONSE: {data}")
    return data