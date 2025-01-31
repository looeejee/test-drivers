import dotenv
import os
from neo4j import GraphDatabase

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

# Connect to Neo4j
with GraphDatabase.driver(URL, auth=(USERNAME, PASSWORD)) as driver:
    driver.verify_connectivity()
    print("Connection established.")