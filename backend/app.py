from flask import Flask, request, jsonify
from flask_cors import CORS

from llm import classify_and_translate
from handlers import handle_sql_query, handle_nosql_query

app = Flask(__name__)

# ✅ This opens it up completely during development
CORS(app, supports_credentials=True)

@app.route('/query', methods=['POST'])
def query():
    user_input = request.json.get("query", "")
    print("User Input:", user_input)

    try:
        print("Calling LLM")

        translated_query = classify_and_translate(user_input)
        print("Translated Query:", translated_query)

        if "SELECT" in translated_query.upper():
            results = handle_sql_query(translated_query)
        else:
            results = handle_nosql_query(translated_query)

        return jsonify({"query": translated_query, "results": results})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port = 5001)
