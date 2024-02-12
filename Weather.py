import requests as req
import pandas as pd
import os
CSV_DATA = pd.DataFrame()
pd_city = []
pd_date = []
pd_time = []
temperature_c = []
is_rainy = []
pressure = []
file_name = 'weather.csv'
city_coordinats = {
    'Moscow':(55.7522, 37.6155),
    'SaintPetersburg' : (59.939, 30.316),
    'Novosibirsk' : (55.03, 82.96),
    'Kazan' : (55.7499, 49.1263),
    'Tula' : (54.2048, 37.6185)
}

API_KEY = "65f14802-4c56-441c-ad2d-a6367e43a6e5"
URL = 'https://api.weather.yandex.ru/v2/forecast'
headers = {
    'X-Yandex-API-Key': API_KEY
}
def get_weather():
    for city in city_coordinats.keys():
        params = {
            'lat': city_coordinats[city][0],
            'lon': city_coordinats[city][-1],
            'lang': 'ru_RU',
            'limit': 7,
            'hours': True,
            'extra': True
        }
        response = req.get(URL, params=params, headers=headers)
        weather_data = response.json()
        for i in range(len(weather_data['forecasts'])):
            for j in range(len(weather_data['forecasts'][i]['hours'])):
                pd_city.append(weather_data['geo_object']['locality']['name'])
                pd_date.append(weather_data['forecasts'][i]['date'])
                pd_time.append(weather_data['forecasts'][i]['hours'][j]['hour'])
                temperature_c.append(weather_data['forecasts'][i]['hours'][j]['temp'])
                is_rainy.append(int(weather_data['forecasts'][i]['hours'][j]['prec_strength'] + 0.75))
                pressure.append(weather_data['forecasts'][i]['hours'][j]['pressure_mm'])

def weather_csv():
    CSV_DATA = pd.DataFrame({
        'City': pd_city,
        'date': pd_date,
        'hour': pd_time,
        'temperature_c': temperature_c,
        'pressure': pressure,
        'is_rainy': is_rainy
    })
    try:
        os.remove(file_name)
    except FileNotFoundError:
        pass
    CSV_DATA.to_csv(file_name)
    pr
get_weather()
weather_csv()

print()