import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

def classify_and_translate(user_input: str) -> str:
    # Step 1: Classify as SQL or MongoDB
    classifier_prompt = f"""
Classify the following query as either "SQL" or "MongoDB".

Guidelines:
- IMPORTANT: If the question explicitly mentions SQL or NoSQL, classify it as that
- Use "SQL" for structured movie metadata (tables: movies, ratings, links)
  Examples: vote_average, genres, titles, release_date, language, filtering, joins, grouping
- Use "MongoDB" for document-style user data (collections: reviews, tags)
  Examples: tags, inserting reviews, counting reviews per user, aggregations, lookups
- "If the prompt is about adding or editing structured metadata like a movie’s title or rating, prefer SQL unless explicitly tagged as NoSQL.

Respond ONLY with one word: SQL or MongoDB

Query: {user_input}
Answer:
""".strip()

    classification = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": classifier_prompt}],
        temperature=0,
        max_tokens=10
    ).choices[0].message.content.strip().upper()

    # Step 2: Use the appropriate system prompt
    if classification == "SQL":
        system_prompt = """
You are MovieDB Assistant — a translator that converts natural language into executable **SQL** queries for the `moviedb` schema.

Focus on structured, tabular movie metadata such as:
- Tables: movies, ratings, links
- Columns like: id, title, release_date, vote_average

Rules:
- Always use full SQL syntax: SELECT, FROM, WHERE, GROUP BY, ORDER BY, JOIN, LIMIT, INSERT, UPDATE, DELETE, etc.
- For filtering or grouping by year, use: YEAR(release_date)
- The primary key for movies is `id` (not `movie_id`)
- Use correct syntax for insert/update/delete:
    - INSERT INTO movies (id, title, vote_average) VALUES (999999, 'New Film', 7.5);
    - UPDATE movies SET title = 'Edited Title' WHERE id = 999999;
    - DELETE FROM movies WHERE id = 999999;
- Do NOT include any explanation or markdown
- Return ONLY the SQL query string
""".strip()

    else:
        system_prompt = """
You are MovieDB Assistant — a translator that converts natural language into executable **MongoDB** queries using Python syntax.

Focus on document-style review data such as:
- Collections: reviews, tags, users
- Fields: tag, userId, movieId

Rules:
- Use `$lookup` to join `reviews` with `movies` on `movieId`
- For schema exploration:
    - Output the plain string: list_collections (DO NOT wrap in quotes)
    - Output: sample_<collection> to show 3 example documents
- For find queries, return:
    - A Python dict: {"tag": "funny"}
    - Or a tuple: ({"tag": "funny"}, {"movieId": 1, "tag": 1, "_id": 0})
- For aggregation, return a list of stages:
    - [ {"$match": {"tag": "funny"}}, {"$group": {"_id": "$userId", "count": {"$sum": 1}}} ]
- For data modification, return a Python dict:
    - {"_action": "insert", "document": {...}}
    - {"_action": "update", "filter": {...}, "update": {...}}
    - {"_action": "delete", "filter": {...}}

Formatting Rules:
- Use Python syntax: True instead of true, None instead of null
- Do NOT use $unwind unless the input clearly refers to an array field
- DO NOT return markdown, explanations, labels, or any extra formatting
- Only return one valid Python object or string — nothing more

Examples of valid MongoDB output:
- list_collections
- sample_reviews
- {"tag": "funny"}
- ({"tag": "funny"}, {"movieId": 1, "tag": 1, "_id": 0})
- [{"$group": {"_id": "$tag", "count": {"$sum": 1}}}]
- {"_action": "insert", "document": {"userId": 100, "movieId": 200, "tag": "cool"}}
""".strip()

    # Step 3: Translate the natural language query
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()
