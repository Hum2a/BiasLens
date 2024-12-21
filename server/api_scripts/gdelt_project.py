import requests

def fetch_gdelt_news(query):
    url = f"https://api.gdeltproject.org/api/v2/doc/doc?query={query}&mode=artlist"
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    articles = fetch_gdelt_news("conflict")
    print(f"Fetched articles from GDELT API.")
    print(articles)
