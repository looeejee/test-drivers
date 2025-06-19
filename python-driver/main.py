import dotenv
import os
import time
import json
from neo4j import GraphDatabase
"""
ENABLE DEBUG LOG FOR TROUBLESHOOTING CONNECTIVITY - BOLT LOGS
"""

# Attempt to load environment variables from .env file
load_status = dotenv.load_dotenv(".env")

# Check if the required variables are set
URL = os.getenv("NEO4J_URL")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# If the .env file was not loaded or variables are not set, raise an error
if not URL or not USERNAME or not PASSWORD:
    if not load_status:
        print("Warning: .env file not found. Using environment variables.")
    else:
        print("Warning: Required environment variables not found in .env file. Falling back to environment variables.")

    # Check if the environment variables are set
    URL = URL or os.getenv("NEO4J_URL")
    USERNAME = USERNAME or os.getenv("NEO4J_USERNAME")
    PASSWORD = PASSWORD or os.getenv("NEO4J_PASSWORD")

    if not URL or not USERNAME or not PASSWORD:
        raise ValueError("Neo4j connection details are not set. Please provide NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD.")
    
def create_nodes_tx(tx, i):
    result = tx.run(
        "CREATE (n:Node {id: $id, name: $name})", id=i, name=f"Node {i}"
    )
    #record = result.single()
    #value = record.value()
    summary = result.consume()
    return summary

def create_rels_tx(tx, i):
    result = tx.run("""
        MATCH (a:Node), (b:Node)
        WHERE a.id = $id1 AND b.id = $id2
        CREATE (a)-[:RELATES_TO]->(b)
        """,
        id1=i % total_nodes, id2=(i + 1) % total_nodes
    )
    #record = result.single()
    #value = record.value()
    summary = result.consume()
    return  summary


def update_nodes_tx(tx, i):
    result = tx.run("MATCH (n:Node {id: $id}) SET n.updated = true", id=i
    )
    #record = result.single()
    #value = record.value()
    summary = result.consume()
    return  summary

# Connect to Neo4j
with GraphDatabase.driver(URL, auth=(USERNAME, PASSWORD)) as driver:
    driver.verify_connectivity()
    print("Connection established.")

    total_nodes = 10  # Number of nodes to create
    total_relationships = 5  # Number of relationships to create

    # Create nodes
    with driver.session() as session:
        create_nodes_summary = 0
        for i in range(total_nodes):
            summary = session.execute_write(create_nodes_tx,i)
            create_nodes_summary += summary.result_available_after
            notifications = summary.summary_notifications
            info = summary.server

    # Create relationships
    with driver.session() as session:
        create_rels_summary = 0
        for i in range(total_relationships):
            create_rels_summary += session.execute_write(update_nodes_tx,i).result_available_after

    # Update properties of some nodes
    with driver.session() as session:
        update_nodes_summary = 0
        for i in range(0, total_nodes, 1000):  # Update every 1000th node
            update_nodes_summary += session.execute_write(create_nodes_tx,i).result_available_after

    print(f"notifiations: {notifications}")
    print(f"Server info: {info.address}, connection_id: {info.connection_id}, protocol_version: {info.protocol_version}")

    # Prepare report data
    report_data = {
        "total_nodes_created": total_nodes,
        "total_relationships_created": total_relationships,
        "created_nodes_summary_ms": create_nodes_summary,
        "created_rels_summary_ms": create_rels_summary,
        "update_nodes_summary_ms": update_nodes_summary,
    }

    # Save report to a file
    report_file_path = "neo4j_performance_report.json"
    with open(report_file_path, 'w') as report_file:
        json.dump(report_data, report_file, indent=4)

    print(f"Report saved to {report_file_path}")
