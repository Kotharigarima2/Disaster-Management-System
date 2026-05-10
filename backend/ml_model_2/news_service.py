import requests

API_KEY = "2d04ecb3a2c44280832f5fce6ab3da47"

URL = "https://newsapi.org/v2/everything"


def fetch_disaster_news():

    params = {
        "q": "disaster OR flood OR earthquake OR explosion OR wildfire OR cyclone",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
        "apiKey": API_KEY
    }

    try:
        response = requests.get(URL, params=params)

        data = response.json()

        articles = data.get("articles", [])

        headlines = []

        for article in articles:
            title = article.get("title")

            if title:
                headlines.append(title)

        return headlines

    except Exception as e:
        print("News API Error:", e)
        return []