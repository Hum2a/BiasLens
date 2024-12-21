import feedparser
import json

def fetch_rss_articles(feed_url):
    feed = feedparser.parse(feed_url)
    articles = []

    for entry in feed.entries:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "summary": entry.summary,
            "published": entry.published
        })

    print(f"Fetched {len(articles)} articles from RSS feed.")
    return articles

if __name__ == "__main__":
    RSS_FEED_URL = "https://rss.cnn.com/rss/edition.rss"
    articles = fetch_rss_articles(RSS_FEED_URL)

    # Save to JSON file
    with open("../data/rss_articles.json", "w") as file:
        json.dump(articles, file, indent=4)
