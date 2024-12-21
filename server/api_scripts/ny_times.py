import requests

def fetch_nyt_news(api_key, query):
    url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&api-key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        print(f"Fetched {len(articles)} articles from New York Times.")
        return articles
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

if __name__ == "__main__":
    API_KEY = "nytimesarticleapikey"
    articles = fetch_nyt_news(API_KEY, "climate change")
    print(f"Fetched {len(articles)} articles from The New York Times API.")
    for article in articles[:5]:
        print(article.get("headline", {}).get("main"))
