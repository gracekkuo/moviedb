from config import MYSQL_CONFIG, MONGO_URI, MONGO_DB
import pymysql
import pymongo
from bson import ObjectId
import ast

def handle_sql_query(query):
    conn = pymysql.connect(**MYSQL_CONFIG)
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in results]
    finally:
        conn.close()

from pymongo import MongoClient
import ast

def handle_nosql_query(query_str):
    client = MongoClient("mongodb://localhost:27017")
    db = client["moviedb"]

    def clean_doc(doc):
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    try:
        # 🛡️ Schema exploration
        if query_str == "list_collections":
            return db.list_collection_names()

        if query_str.startswith("sample_"):
            collection = query_str.replace("sample_", "")
            docs = db[collection].find().limit(3)
            return [clean_doc(doc) for doc in docs]

        # 🧠 Handle projection format (tuple with projection=...)
        if "projection=" in query_str:
            query_part, proj_part = query_str.split("projection=")
            query = ast.literal_eval(query_part.strip().rstrip(','))
            projection = ast.literal_eval(proj_part.strip())
            results = db.reviews.find(query, projection)
            return [clean_doc(doc) for doc in results]

        # 🔎 Parse generic MongoDB query
        query = ast.literal_eval(query_str.strip())

        if isinstance(query, tuple) and len(query) == 2:
            return [clean_doc(doc) for doc in db.reviews.find(query[0], query[1])]

        if isinstance(query, list):
            return [clean_doc(doc) for doc in db.reviews.aggregate(query)]

        if isinstance(query, dict) and "_action" in query:
            action = query["_action"]
            if action == "delete":
                result = db.reviews.delete_many(query["filter"])
                return {"deleted": result.deleted_count}
            elif action == "update":
                result = db.reviews.update_many(query["filter"], query["update"])
                return {"matched": result.matched_count, "modified": result.modified_count}
            elif action == "insert":
                result = db.reviews.insert_one(query["document"])
                return {"inserted_id": str(result.inserted_id)}

        if isinstance(query, dict):
            return [clean_doc(doc) for doc in db.reviews.find(query)]

        return {"error": "Query was not recognized."}

    except Exception as e:
        return {"error": str(e)}

    finally:
        client.close()
