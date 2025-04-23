from flask import Flask, request, jsonify
from flask_cors import CORS
import ast

from llm import classify_and_translate
from handlers import handle_sql_query, handle_nosql_query

app = Flask(__name__)
CORS(app, supports_credentials=True)

def route_query(llm_response: str):
    try:
        # Try parsing to detect MongoDB-style objects
        parsed = ast.literal_eval(llm_response)

        # Handle NoSQL if it's a Python object (dict, list, tuple)
        if isinstance(parsed, (dict, list, tuple)):
            return handle_nosql_query(llm_response)
        else:
            return {"error": "Unsupported structure from LLM"}

    except (SyntaxError, ValueError):
        # Parsing failed — check for raw string queries
        cleaned = llm_response.strip()

        # Direct MongoDB command strings (like list_collections or sample_reviews)
        if cleaned in {"list_collections"} or cleaned.startswith("sample_"):
            return handle_nosql_query(cleaned)

        # SQL keyword-based routing
        upper = cleaned.upper()
        if upper.startswith(("SELECT", "INSERT", "UPDATE", "DELETE")):
            return handle_sql_query(cleaned)

        return {"error": "Unrecognized query format."}

@app.route('/query', methods=['POST'])
def query():
    user_input = request.json.get("query", "")
    print("User Input:", user_input)

    try:
        print("Calling LLM")
        translated_query = classify_and_translate(user_input)
        print("Translated Query:", translated_query)

        results = route_query(translated_query)
        return jsonify({"query": translated_query, "results": results})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
