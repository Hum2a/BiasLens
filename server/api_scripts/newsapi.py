import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fetch_newsapi_articles(api_key=None, query="", language='en'):
    """
    Fetch news articles from NewsAPI.
    
    Args:
        api_key (str, optional): NewsAPI key. If None, uses NEWSAPI_KEY from .env
        query (str): Search query term
        language (str): Language code for articles (default: 'en')
        
    Returns:
        list: List of article dictionaries
    """
    # Use provided API key or get from environment variables
    api_key = api_key or os.getenv("NEWSAPI_KEY")
    
    if not api_key:
        print("Error: NewsAPI key not found. Please set NEWSAPI_KEY in .env file")
        return []
    
    url = f"https://newsapi.org/v2/everything?q={query}&language={language}&apiKey={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        articles = data.get("articles", [])
        print(f"Fetched {len(articles)} articles from NewsAPI.")
        return articles
    except Exception as e:
        print(f"Error fetching from NewsAPI: {e}")
        return []

if __name__ == "__main__":
    # When run directly, use the API key from .env
    api_key = os.getenv("NEWSAPI_KEY")
    if not api_key:
        print("Warning: NEWSAPI_KEY not found in environment variables")
    
    query = "politics"
    articles = fetch_newsapi_articles(api_key=api_key, query=query)
    print(f"Fetched {len(articles)} articles from NewsAPI about '{query}'.")
    
    # Save to JSON file
    if articles:
        output_path = "../data/newsapi_articles.json"
        with open(output_path, "w") as file:
            json.dump(articles, file, indent=4)
        print(f"Saved articles to {output_path}")
        
        # Display the first few articles
        for i, article in enumerate(articles[:3]):
            print(f"\nArticle {i+1}:")
            print(f"Title: {article.get('title')}")
            print(f"Source: {article.get('source', {}).get('name')}")
            print(f"URL: {article.get('url')}")
