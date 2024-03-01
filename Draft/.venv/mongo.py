from pymongo import MongoClient

# Provide the connection details
hostname = 'localhost'
port = 27023  # Default MongoDB port
username = "Test"  # If authentication is required
password = "mongo_Test"  # If authentication is required
# Create a MongoClient instance
client = MongoClient(hostname, port, username=username, password=password)