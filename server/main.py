import json
import os
from dotenv import load_dotenv
from api_scripts.newsapi import fetch_newsapi_articles
from api_scripts.ny_times import fetch_nyt_news
from api_scripts.theguardian import fetch_guardian_news
from api_scripts.res_scraper import fetch_rss_articles
from api_scripts.mediastack import fetch_mediastack_news
from api_scripts.gdelt_project import fetch_gdelt_news
from api_scripts.google_news import fetch_google_news_rss
from api_scripts.currents import fetch_currents_news
from article_analyser import analyze_articles_with_bias, determine_political_bias
from firebase.firebase_functions import upload_to_firestore

# Load environment variables from .env file
load_dotenv()

def normalize_articles(source, articles):
    normalized = []
    for article in articles:
        if isinstance(article, dict):  # Check if article is a dict
            normalized.append({
                "source": source,
                "title": article.get("title") or article.get("headline", {}).get("main"),
                "description": article.get("description") or article.get("summary"),
                "url": article.get("url") or article.get("link"),
                "published": article.get("publishedAt") or article.get("published")
            })
        else:
            print(f"Skipping non-dict article from {source}: {article}")
    return normalized

if __name__ == "__main__":
    # Define API keys and parameters
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
    NYT_KEY = os.getenv("NYT_KEY")
    GUARDIAN_KEY = os.getenv("GUARDIAN_KEY")
    MEDIASTACK_KEY = os.getenv("MEDIASTACK_KEY")
    CURRENTS_KEY = os.getenv("CURRENTS_KEY")

    QUERY = "technology"
    RSS_FEED_URL = "https://rss.cnn.com/rss/edition.rss"

    # Fetch articles
    try:
        newsapi_articles = fetch_newsapi_articles(NEWSAPI_KEY, QUERY)
    except Exception as e:
        print(f"Error fetching from NewsAPI: {e}")
        newsapi_articles = []

    try:
        nyt_articles = fetch_nyt_news(NYT_KEY, QUERY)
    except Exception as e:
        print(f"Error fetching from NYT: {e}")
        nyt_articles = []

    try:
        guardian_articles = fetch_guardian_news(GUARDIAN_KEY, QUERY)
    except Exception as e:
        print(f"Error fetching from The Guardian: {e}")
        guardian_articles = []

    try:
        mediastack_articles = fetch_mediastack_news(MEDIASTACK_KEY, QUERY)
    except Exception as e:
        print(f"Error fetching from MediaStack: {e}")
        mediastack_articles = []

    try:
        gdelt_articles = fetch_gdelt_news(QUERY)
        gdelt_articles = [{"title": line, "url": ""} for line in gdelt_articles.splitlines() if line.strip()]
    except Exception as e:
        print(f"Error fetching from GDELT: {e}")
        gdelt_articles = []

    try:
        google_news_articles = fetch_google_news_rss()
    except Exception as e:
        print(f"Error fetching from Google News: {e}")
        google_news_articles = []

    try:
        currents_articles = fetch_currents_news(CURRENTS_KEY, QUERY)
    except Exception as e:
        print(f"Error fetching from Currents API: {e}")
        currents_articles = []

    try:
        rss_articles = fetch_rss_articles(RSS_FEED_URL)
    except Exception as e:
        print(f"Error fetching from RSS: {e}")
        rss_articles = []

    # Normalize articles
    all_articles = []
    all_articles.extend(normalize_articles("NewsAPI", newsapi_articles))
    all_articles.extend(normalize_articles("NY Times", nyt_articles))
    all_articles.extend(normalize_articles("The Guardian", guardian_articles))
    all_articles.extend(normalize_articles("MediaStack", mediastack_articles))
    all_articles.extend(normalize_articles("GDELT", gdelt_articles))
    all_articles.extend(normalize_articles("Google News", google_news_articles))
    all_articles.extend(normalize_articles("Currents", currents_articles))
    all_articles.extend(normalize_articles("RSS", rss_articles))

    # Save normalized data
    with open("./data/all_articles.json", "w") as file:
        json.dump(all_articles, file, indent=4)

    print(f"Aggregated and normalized {len(all_articles)} articles from all sources.")

    input_file = "./data/all_articles.json"
    output_file = "./data/analyzed_articles.json"

    # Perform sentiment analysis
    analyze_articles_with_bias(input_file, output_file)

    # Upload analyzed articles to Firestore
    upload_to_firestore(output_file)