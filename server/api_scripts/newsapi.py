import requests
import json

def fetch_newsapi_articles(api_key, query, language='en'):
    url = f"https://newsapi.org/v2/everything?q={query}&language={language}&apiKey={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        articles = response.json().get("articles", [])
        print(f"Fetched {len(articles)} articles from NewsAPI.")
        return articles
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

if __name__ == "__main__":
    API_KEY = "618a242afb714a61a5dfe90f0d6ebc11"
    query = "politics"
    articles = fetch_newsapi_articles(API_KEY, query)

    # Save to JSON file
    with open("../data/newsapi_articles.json", "w") as file:
        json.dump(articles, file, indent=4)
