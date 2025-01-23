import dotenv
import os
from neo4j import GraphDatabase

# Attempt to load environment variables from .env file
load_status = dotenv.load_dotenv(".env")

# Check if the required variables are set
URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# If the .env file was not loaded or variables are not set, raise an error
if not URI or not USERNAME or not PASSWORD:
    if not load_status:
        print("Warning: .env file not found. Using environment variables.")
    else:
        print("Warning: Required environment variables not found in .env file. Falling back to environment variables.")

    # Check if the environment variables are set
    URI = URI or os.getenv("NEO4J_URI")
    USERNAME = USERNAME or os.getenv("NEO4J_USERNAME")
    PASSWORD = PASSWORD or os.getenv("NEO4J_PASSWORD")

    if not URI or not USERNAME or not PASSWORD:
        raise ValueError("Neo4j connection details are not set. Please provide NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD.")

# Connect to Neo4j
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    print("Connection established.")