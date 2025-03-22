import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

def fetch_mediastack_news(api_key=None, query="", language="en"):
    """
    Fetch news articles from MediaStack API.
    
    Args:
        api_key (str, optional): MediaStack API key. If None, uses MEDIASTACK_KEY from .env
        query (str): Search keywords
        language (str): Language code for articles (default: 'en')
        
    Returns:
        list: List of article dictionaries
    """
    # Use provided API key or get from environment variables
    api_key = api_key or os.getenv("MEDIASTACK_KEY")
    
    if not api_key:
        print("Error: MediaStack API key not found. Please set MEDIASTACK_KEY in .env file")
        return []
    
    url = f"http://api.mediastack.com/v1/news?access_key={api_key}&languages={language}&keywords={query}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        articles = data.get("data", [])  # MediaStack uses 'data' key for results
        print(f"Fetched {len(articles)} articles from MediaStack.")
        return articles
    except Exception as e:
        print(f"Error fetching from MediaStack API: {e}")
        return []

if __name__ == "__main__":
    # When run directly, use the API key from .env
    api_key = os.getenv("MEDIASTACK_KEY")
    if not api_key:
        print("Warning: MEDIASTACK_KEY not found in environment variables")
    
    query = "technology"
    articles = fetch_mediastack_news(api_key=api_key, query=query)
    print(f"Fetched {len(articles)} articles from MediaStack about '{query}'.")
    
    # Save to JSON file
    if articles:
        output_path = "../data/mediastack_articles.json"
        with open(output_path, "w") as file:
            json.dump(articles, file, indent=4)
        print(f"Saved articles to {output_path}")
        
        # Display the first few articles
        for i, article in enumerate(articles[:3]):
            print(f"\nArticle {i+1}:")
            print(f"Title: {article.get('title')}")
            print(f"Source: {article.get('source')}")
            print(f"URL: {article.get('url')}")
            if article.get('description'):
                print(f"Description: {article.get('description')[:100]}...")
