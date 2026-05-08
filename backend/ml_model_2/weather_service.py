import requests

API_KEY = "8f4641fc010de4f45612347d8f72ea64"   # 🔴 put your OpenWeatherMap key here

def get_weather_severity(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()

        weather_main = data['weather'][0]['main'].lower()

        # 🔥 check rain volume if available
        rain = data.get('rain', {}).get('1h', 0)

        if rain > 10:
            return 2   # heavy rain
        elif rain > 2:
            return 1   # moderate rain

        if "storm" in weather_main:
            return 2
        elif "rain" in weather_main:
            return 1
        else:
            return 0

    except:
        print("Weather API error")
        return 0