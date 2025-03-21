import csv
from elasticsearch import Elasticsearch, helpers
import os

# Elasticsearch configuration
ES_HOST = "http://localhost:9200"  # Update if running on a different host
INDEX_NAME = "cv-transcriptions"

# Initialize Elasticsearch client
es = Elasticsearch([ES_HOST])


# Function to create the Elasticsearch index if it doesn't exist
def create_index():
    if not es.indices.exists(index=INDEX_NAME):
        index_body = {
            "settings": {"number_of_shards": 1, "number_of_replicas": 1},
            "mappings": {
                "properties": {
                    "filename": {"type": "keyword"},
                    "text": {"type": "text"},
                    "up_votes": {"type": "integer"},
                    "down_votes": {"type": "integer"},
                    "age": {"type": "keyword"},
                    "gender": {"type": "keyword"},
                    "accent": {"type": "keyword"},
                    "duration": {"type": "float"},
                    "generated_text": {"type": "text"},
                }
            },
        }
        es.indices.create(index=INDEX_NAME, body=index_body)
        print(f"Index '{INDEX_NAME}' created.")
    else:
        print(f"Index '{INDEX_NAME}' already exists.")


# Function to read the CSV file and index data into Elasticsearch
def read_csv_and_index_data(csv_file):
    actions = []

    # Open the CSV file and read the data
    with open(csv_file, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # Convert empty values to None
            up_votes = int(row["up_votes"]) if row["up_votes"].isdigit() else 0
            down_votes = int(row["down_votes"]) if row["down_votes"].isdigit() else 0
            duration = (
                float(row["duration"])
                if row["duration"].replace(".", "", 1).isdigit()
                else 0.0
            )

            # Create an action for bulk insertion
            actions.append(
                {
                    "_index": INDEX_NAME,
                    "_source": {
                        "filename": row["filename"],
                        "text": row["text"],
                        "up_votes": up_votes,
                        "down_votes": down_votes,
                        "age": row["age"] if row["age"] else None,
                        "gender": row["gender"] if row["gender"] else None,
                        "accent": row["accent"] if row["accent"] else None,
                        "duration": duration,
                        "generated_text": row["generated_text"],
                    },
                }
            )

    # Use Elasticsearch bulk API to insert data
    if actions:
        helpers.bulk(es, actions)
        print(f"Indexed {len(actions)} documents into '{INDEX_NAME}'.")


if __name__ == "__main__":
    csv_file_path = "cv-data/common-voice/cv-valid-dev.csv"  # Adjust path if needed

    if not os.path.exists(csv_file_path):
        print(f"CSV file not found: {csv_file_path}")

    create_index()
    read_csv_and_index_data(csv_file_path)
