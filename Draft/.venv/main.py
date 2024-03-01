import os
import datetime as dt
import requests as req
import pandas as pd

API_URL = 'https://api-metrika.yandex.ru/stat/v1/data.csv'
API_token = '9c67124f-9ba9-4d5d-bdb1-48eeb4464e27'
params = {

    'date1': '6daysAgo',
    'date2': 'today',
    'id': 96534053,
    'metrics': 'ym:s:visits,ym:s:users',
    'limit': 100
}
r = req.get(API_URL, params = params, headers={'Authorization':API_token})
print(r)
# pd_city = []
# pd_date = []
# pd_time = []
# temperature_c = []
# is_rainy = []
# pressure = []
# file_name = 'weather.csv'
# city_coordinats = {
#     'Moscow':(55.7522, 37.6155),
#     'SaintPetersburg' : (59.939, 30.316),
#     'Novosibirsk' : (55.03, 82.96),
#     'Kazan' : (55.7499, 49.1263),
#     'Tula' : (54.2048, 37.6185)
# }
#
# API_KEY = "65f14802-4c56-441c-ad2d-a6367e43a6e5"
# URL = 'https://api.weather.yandex.ru/v2/forecast'
# headers = {
#     'X-Yandex-API-Key': API_KEY
# }
# def get_weather():
#     for city in city_coordinats.keys():
#         params = {
#             'lat': city_coordinats[city][0],
#             'lon': city_coordinats[city][-1],
#             'lang': 'ru_RU',
#             'limit': 7,
#             'hours': True,
#             'extra': True
#         }
#         response = req.get(URL, params=params, headers=headers)
#         weather_data = response.json()
#         for i in range(len(weather_data['forecasts'])):
#             for j in range(len(weather_data['forecasts'][i]['hours'])):
#                 pd_city.append(weather_data['geo_object']['locality']['name'])
#                 pd_date.append(weather_data['forecasts'][i]['date'])
#                 pd_time.append(weather_data['forecasts'][i]['hours'][j]['hour'])
#                 temperature_c.append(weather_data['forecasts'][i]['hours'][j]['temp'])
#                 is_rainy.append(int(weather_data['forecasts'][i]['hours'][j]['prec_strength'] + 0.75))
#                 pressure.append(weather_data['forecasts'][i]['hours'][j]['pressure_mm'])
#         print(pd_city)
#     CSV_DATA = pd.DataFrame({
#         'City': pd_city,
#         'date': pd_date,
#         'hour': pd_time,
#         'temperature_c': temperature_c,
#         'pressure': pressure,
#         'is_rainy': is_rainy
#     })
#     print(pd_city)
#     print(CSV_DATA)
#     try:
#         os.remove(file_name)
#     except FileNotFoundError:
#         pass
#     print(CSV_DATA)
#     CSV_DATA.to_csv(file_name, index_label=False, index=False)
# get_weather()
#
# f = open('weather.csv', encoding="utf8")
# file_data = f.readlines()
# columns = file_data[0].replace("\n","").split(sep=',')
# print(columns)
# file_data.pop(0)
# values_dict = {column: [] for column in columns}
# for row in file_data:
#     for i , value in enumerate(row.replace("\n", "").split(sep=','), 1):
#         values_dict[columns[i-1]].append(value)
# print(len())