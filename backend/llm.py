# llm.py
from llama_cpp import Llama

# Load Llama model (downloaded manually)
llm = Llama(model_path="models/llama-2-7b.gguf")

def classify_and_translate(query: str):
    prompt = f"Convert this natural language query to a database command:\n{query}\n"
    output = llm(prompt, max_tokens=256)
    return output["choices"][0]["text"].strip()