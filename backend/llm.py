import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

client = openai.OpenAI()

def classify_and_translate(user_input: str) -> str:
    system_prompt = """
You are a helpful assistant that converts natural language into executable database queries.

Rules:
- Use SQL for structured movie metadata (title, genre, rating).
- Use MongoDB dicts or lists for reviews, tags, or aggregations.
- Use $lookup to join reviews with movies using movieId.
- For schema exploration:
    - Return "list_collections" to list collections.
    - Return "sample_<collection>" to get a few docs from a collection.
- For projection, output a tuple: (filter_dict, projection_dict)
- For modification: output dict with "_action", e.g., {"_action": "delete", "filter": {...}}

Only output the raw query. No extra text. No quotes. No formatting.

Examples:

Q: What collections are in the database?
A: list_collections

Q: Show sample documents from the reviews collection
A: sample_reviews

Q: Show movieId and tag for all reviews with tag 'scary'
A: ({"tag": "scary"}, {"movieId": 1, "tag": 1, "_id": 0})

Q: Delete reviews with tag 'boring'
A: {"_action": "delete", "filter": {"tag": "boring"}}

Q: How many reviews are there per tag?
A: [{"$group": {"_id": "$tag", "count": {"$sum": 1}}}]

Q: Show all reviews with tag 'funny' and include movie titles
A: [
  {"$match": {"tag": "funny"}},
  {"$lookup": {"from": "movies", "localField": "movieId", "foreignField": "movieId", "as": "movie_info"}},
  {"$project": {"tag": 1, "movieId": 1, "userId": 1, "movie_info.title": 1, "_id": 0}}
]

Q: How many reviews has each user made with tag 'funny'?
A: [
  {"$match": {"tag": "funny"}},
  {"$group": {"_id": "$userId", "count": {"$sum": 1}}}
]

Q: Insert a new review with userId 100, movieId 200, tag 'charming'
A: {
  "_action": "insert",
  "document": {
    "userId": 100,
    "movieId": 200,
    "tag": "charming"
  }
}

""".strip()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.2,
        max_tokens=200
    )

    return response.choices[0].message.content.strip()
