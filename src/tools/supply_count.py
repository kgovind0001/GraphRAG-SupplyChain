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