import os
from pymongo import MongoClient


def get_mongo_client():
    client = MongoClient(os.environ.get("MONGO_URI"))
    return client, client["AI"]["memo"]


def fetch_or_create_memo(date):
    client, collection = get_mongo_client()

    # Find the document with the specified date
    query = {"date": date}
    memo_document = collection.find_one(query)

    # Check if a document exists for that date
    if memo_document is not None:
        client.close()
        return memo_document
    else:
        # Create a new document with an empty memo
        new_memo = {
            "date": date,
            "content": [],
        }  # Assuming content is an array of memos
        collection.insert_one(new_memo)
        client.close()
        return new_memo


def insert_memo(memo, date):
    client, collection = get_mongo_client()

    # Create the query and new data
    query = {"date": date}
    new_data = {"$set": {"content": memo}}

    # Update the document with the specified date, or insert if it doesn't exist
    collection.update_one(query, new_data, upsert=True)

    client.close()
