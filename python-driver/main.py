import dotenv
import os
from neo4j import GraphDatabase

# Load environment variables from .env file if it exists
load_status = dotenv.load_dotenv(".env")
if load_status is False:
    raise RuntimeError('Environment variables not loaded.')

# Get Neo4j connection details from environment variables
URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

# Check if the required variables are set
if not URI or not AUTH[0] or not AUTH[1]:
    raise ValueError("Neo4j connection details are not set. Please provide NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD.")
# Connect to Neo4j
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    print("Connection established.")