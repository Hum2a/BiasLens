import requests

def fetch_currents_news(api_key, query):
    url = f"https://api.currentsapi.services/v1/search?apiKey={api_key}&keywords={query}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        print(f"Fetched {len(articles)} articles from CurrentAPI.")
        return articles
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

if __name__ == "__main__":
    API_KEY = "3B4dB02-BXairvG1x0sb8EVVizeJrqazH24z_lh1ctV9EWC9"
    articles = fetch_currents_news(API_KEY, "technology")
    print(f"Fetched {len(articles)} articles from Currents API.")
    for article in articles[:5]:
        print(article)
