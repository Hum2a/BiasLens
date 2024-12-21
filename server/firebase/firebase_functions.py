import json

from firebase.firebase_config import db

def upload_to_firestore(input_file):
    # Load articles from the JSON file
    with open(input_file, "r") as file:
        articles = json.load(file)

    # Reference Firestore collection
    collection_ref = db.collection("Articles")

    # Upload each article as a document
    for article in articles:
        try:
            # Use URL as document ID to avoid duplicates
            doc_id = article.get("url", "").replace("https://", "").replace("/", "_")
            collection_ref.document(doc_id).set(article)
            print(f"Uploaded article: {article['title']}")
        except Exception as e:
            print(f"Error uploading article: {e}")

    print(f"Uploaded {len(articles)} articles to Firestore.")
