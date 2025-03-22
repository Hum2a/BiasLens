import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fetch_guardian_news(api_key=None, query=""):
    """
    Fetch news articles from The Guardian API.
    
    Args:
        api_key (str, optional): The Guardian API key. If None, uses GUARDIAN_KEY from .env
        query (str): Search query term
        
    Returns:
        list: List of article dictionaries
    """
    # Use provided API key or get from environment variables
    api_key = api_key or os.getenv("GUARDIAN_KEY")
    
    if not api_key:
        print("Error: Guardian API key not found. Please set GUARDIAN_KEY in .env file")
        return []
    
    url = f"https://content.guardianapis.com/search?q={query}&api-key={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        # Guardian API response structure is different - extract results correctly
        articles = data.get("response", {}).get("results", [])
        print(f"Fetched {len(articles)} articles from The Guardian.")
        return articles
    except Exception as e:
        print(f"Error fetching from The Guardian API: {e}")
        return []


if __name__ == "__main__":
    # When run directly, use the API key from .env
    api_key = os.getenv("GUARDIAN_KEY")
    if not api_key:
        print("Warning: GUARDIAN_KEY not found in environment variables")
    
    articles = fetch_guardian_news(api_key=api_key, query="technology")
    print(f"Fetched {len(articles)} articles from The Guardian API.")
    
    # Display the first few articles
    for i, article in enumerate(articles[:3]):
        print(f"\nArticle {i+1}:")
        print(f"Title: {article.get('webTitle')}")
        print(f"Section: {article.get('sectionName')}")
        print(f"URL: {article.get('webUrl')}")
