# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from llm import classify_and_translate
from handlers import handle_sql_query, handle_nosql_query

app = Flask(__name__)
CORS(app)

@app.route('/query', methods=['POST'])
def query():
    user_input = request.json.get("query", "")
    print("User query:", user_input)

    translated = classify_and_translate(user_input)
    print("Translated:", translated)

    if "SELECT" in translated.upper():
        result = handle_sql_query(translated)
    else:
        result = handle_nosql_query(eval(translated))  # Warning: use eval cautiously!

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
