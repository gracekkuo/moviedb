# handlers.py
from config import MYSQL_CONFIG, MONGO_URI, MONGO_DB
import pymysql
import pymongo

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

def handle_nosql_query(query_str):
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    try:
        query = eval(query_str)  # Caution: only if you're trusting the model or have good safety wrappers
        results = db.reviews.find(query)
        return list(results)
    finally:
        client.close()

