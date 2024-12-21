import requests

def fetch_guardian_news(api_key, query):
    url = f"https://content.guardianapis.com/search?q={query}&api-key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        print(f"Fetched {len(articles)} articles from The Guardian.")
        return articles
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

if __name__ == "__main__":
    API_KEY = "5bed318f-70fb-4b5f-a159-0cab7d4cebf7"
    articles = fetch_guardian_news(API_KEY, "sports")
    print(f"Fetched {len(articles)} articles from The Guardian API.")
    for article in articles[:5]:
        print(article)
