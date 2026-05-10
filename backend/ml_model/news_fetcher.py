import requests

API_KEY = "2d04ecb3a2c44280832f5fce6ab3da47"


URL = "https://newsapi.org/v2/everything"

def fetch_disaster_news():
    params = {
        "q": "disaster OR flood OR earthquake OR wildfire OR cyclone",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
        "apiKey": API_KEY
    }

    response = requests.get(URL, params=params)
    data = response.json()

    articles = data.get("articles", [])

    news_list = []

    for a in articles:
        text = f"{a.get('title')} {a.get('description')}"
        if text:
            news_list.append(text)

    return news_list