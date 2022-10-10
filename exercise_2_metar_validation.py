from dataclasses import field
import requests
import pandas as pd
from exercise_1_weathermonitoringtool import query_weather_data, temperature_to_celsius_and_fahrenheit
from exercise_1_weathermonitoringtool import time_until_sunrise_or_sunset, predict_mood_from_weather, compare_and_plot_weather_data

def query_metar_data(lat,lon, api_key):
    url = f'https://api.checkwx.com/metar/lat/{lat}/lon/{lon}/decoded'
    headers = {'X-API-Key': api_key}
    response = requests.get(url, headers=headers)
    return response.json()

def create_dataframe(datacity,datametar):
    accuracy = {}
    accuracy["header"] ="Data Accuracy in %"
    for keyfield in datametar:
        if keyfield in datacity and keyfield != "header":
            accuracy[keyfield] = 100 - (abs(datametar[keyfield] - datacity[keyfield])/datametar[keyfield]*100)
    print (accuracy)
    dataframe = pd.DataFrame([accuracy,datametar,datacity]).dropna(axis=1)
    return dataframe 

def normalize_metardata(data):
    data_normalized = {}
    data = data["data"][0]
    data_normalized["header"] = "METAR Data"
    if(data.get("wind")is not None):
        data_normalized["windspeed"] = data["wind"]["speed_mps"]
        data_normalized["winddirection"] = data["wind"]["degrees"]
    if(data.get("humidity")is not None):
        data_normalized["humidity"] = data["humidity"]["percent"]
    if(data.get("barometer")is not None):
        data_normalized["pressure"] = data["barometer"]["mb"]
    if(data.get("temperature")is not None):
        data_normalized["temperatureincelsius"] = data["temperature"]["celsius"]
        data_normalized["temperatureinfahrenheit"] = data["temperature"]["fahrenheit"]
    if(data.get("visibility")is not None):
        data_normalized["visibility"] = data["visibility"]["meters_float"]
    if(data.get("rain") is not None):
        data_normalized["rain"] = data["rain"]["inches"]*2.54
    if(data.get("snow") is not None):
        data_normalized["snow"] = data["snow"]["inches"]*2.54
    if(data.get("sunrise") is not None):
        data_normalized["sunrise"] = data["sunrise"]["unix"]
    if(data.get("sunset") is not None):
        data_normalized["sunset"] = data["sunset"]["unix"]
    return data_normalized

def normalize_citydata(data):
    data_normalized = {}    
    data_normalized["header"] = "OpenWeather Data"
    if(data['weather_data'].get("wind")is not None):
        data_normalized["windspeed"] = data["weather_data"]["wind"]["speed"]
        data_normalized["winddirection"] = data['weather_data']["wind"]["deg"]
    if(data['weather_data']['main'].get("humidity")is not None):
        data_normalized["humidity"] = data["weather_data"]["main"]["humidity"]
    if(data['weather_data']['main'].get("pressure")is not None):
        data_normalized["pressure"] = data["weather_data"]["main"]["pressure"]
    data_normalized["temperatureincelsius"] = data["temperature"]['celsius']
    data_normalized["temperatureinfahrenheit"] = data["temperature"]['fahrenheit']
    if(data['weather_data'].get("visibility")is not None):
        data_normalized["visibility"] = data["weather_data"]["visibility"]
    if(data['weather_data'].get("rain")is not None):
        data_normalized["rain"] = data["weather_data"]["rain"]["1h"]
    if(data['weather_data'].get("snow")is not None):
        data_normalized["snow"] = data["weather_data"]["snow"]["1h"]
    if(data['weather_data']['sys'].get("sunrise")is not None):
        data_normalized["sunrise"] = data["weather_data"]["sys"]["sunrise"]
    if(data['weather_data']['sys'].get("sunset")is not None):
        data_normalized["sunset"] = data["weather_data"]["sys"]["sunset"]
    if(data['weather_data'].get("clouds")is not None):
        data_normalized["clouds"] = data["weather_data"]["clouds"]["all"]
    
    return data_normalized
#def find_common_fields(full_city_info, metar_data):
    