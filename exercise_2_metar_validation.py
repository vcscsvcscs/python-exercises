import requests
import pandas as pd
from exercise_1_weathermonitoringtool import query_weather_data, temperature_to_celsius_and_fahrenheit
from exercise_1_weathermonitoringtool import time_until_sunrise_or_sunset, predict_mood_from_weather, compare_and_plot_weather_data

def query_metar_data(lat,lon, api_key):
    url = f'https://api.checkwx.com/metar/lat/{lat}/lon/{lon}/decoded'
    headers = {'X-API-Key': api_key}
    response = requests.get(url, headers=headers)
    return response.json()

def create_key_list(data):
    data_keys = [] 
    for field in data:
        if(type(data[field]) is dict):
            data_keys.append({field:create_key_list(data[field])})
        else:
            data_keys.append(field)
    return data_keys

def normalize_data(data):
    df = pd.DataFrame(data)
    df_list = list()

    for col in df.columns[3:]:
        v = pd.json_normalize(df[col])
        v.columns = [f'{col}_{c}' for c in v.columns]
        df_list.append(v)

    # combine into one dataframe
    return pd.concat([df.iloc[:, :3]] + df_list, axis=2)


#def find_common_fields(full_city_info, metar_data):
    