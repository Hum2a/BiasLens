import requests

def fetch_mediastack_news(api_key, query, language="en"):
    url = f"http://api.mediastack.com/v1/news?access_key={api_key}&languages={language}&keywords={query}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        print(f"Fetched {len(articles)} articles from MediaStack.")
        return articles
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

if __name__ == "__main__":
    API_KEY = "6300a2f329c810aeca5cdfef53564a65"
    articles = fetch_mediastack_news(API_KEY, "technology")
    print(f"Fetched {len(articles)} articles from MediaStack.")
    for article in articles[:5]:
        print(article)
