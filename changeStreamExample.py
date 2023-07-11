from pymongo import MongoClient
from pymongo.errors import OperationFailure

# MongoDB connection details
mongodb_url = ''
database_name = ''
collection_name = ''

# Connect to MongoDB
client = MongoClient(mongodb_url)
db = client[database_name]
collection = db[collection_name]

# Create a change stream cursor
try:
    cursor = collection.watch()
    print(f"Listening to changes in '{collection_name}' collection...")

    # Iterate over the change stream
    for change in cursor:
        print(change)

except OperationFailure as e:
    print(f"Failed to listen for changes: {e}")

# Close the MongoDB connection
client.close()
