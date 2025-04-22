# llm.py
from llama_cpp import Llama

llm = Llama(model_path="models/llama-2-7b.gguf")

def classify_and_translate(user_input: str) -> str:
    prompt = f"""
You are a database assistant. Convert this natural language request into a database query.

Respond with either:
- A SQL query (if it's about structured movie data like title, rating, revenue, cast)
- A MongoDB Python dict (if it's about user reviews, tags, or text search)

Query: "{user_input}"
Database command:
    """
    
    response = llm(prompt, max_tokens=256, temperature=0.3)
    return response["choices"][0]["text"].strip()
