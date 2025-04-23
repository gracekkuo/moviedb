import pandas as pd
from sqlalchemy import create_engine

# MySQL config — update if needed
MYSQL_USER = "root"
MYSQL_PASSWORD = "rootpass"
MYSQL_HOST = "localhost"
MYSQL_PORT = "3307"  # running on 3307
MYSQL_DB = "moviedb"

# Create engine
engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}")

# Paths to your CSVs
base_path = "sql_data"
movies_path = f"{base_path}/movies_metadata.csv"
ratings_path = f"{base_path}/ratings.csv"
links_path = f"{base_path}/links.csv"

# Load and trim datasets
movies_df = pd.read_csv(movies_path, low_memory=False).head(1000)
ratings_df = pd.read_csv(ratings_path).head(1000)
links_df = pd.read_csv(links_path).head(1000)

# Write to SQL
movies_df.to_sql("movies", engine, if_exists="replace", index=False)
ratings_df.to_sql("ratings", engine, if_exists="replace", index=False)
links_df.to_sql("links", engine, if_exists="replace", index=False)

print("Trimmed datasets loaded into MySQL!")
