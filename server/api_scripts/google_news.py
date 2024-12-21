import feedparser

def fetch_google_news_rss():
    rss_url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    articles = [
        {"title": entry.title, "link": entry.link, "published": entry.published}
        for entry in feed.entries
    ]
    return articles

if __name__ == "__main__":
    articles = fetch_google_news_rss()
    print(f"Fetched {len(articles)} articles from Google News RSS.")
    for article in articles[:5]:
        print(article)
