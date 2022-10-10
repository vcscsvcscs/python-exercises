from random import random
import matplotlib.pyplot as plt
import requests
import pandas as pd

def query_metar_data(lat, lon, api_key):
    url = f'https://api.checkwx.com/metar/lat/{lat}/lon/{lon}/decoded'
    headers = {'X-API-Key': api_key}
    response = requests.get(url, headers=headers)
    return response.json()


def data_accuracy(datacity, datametar):
    accuracy = {}
    accuracy["header"] = "Data Accuracy in %"
    for keyfield in datametar:
        if keyfield in datacity and keyfield != "header":
            if (datametar[keyfield] == 0):
                if (datacity[keyfield] == 0):
                    accuracy[keyfield] = 100
                else:
                    accuracy[keyfield] = (
                        100 - abs(datametar[keyfield] - datacity[keyfield]))
            else:
                if (datacity[keyfield] == 0):
                    accuracy[keyfield] = (
                        100 - abs(datametar[keyfield] - datacity[keyfield]))
                else:
                    accuracy[keyfield] = 100 - \
                        (abs(datametar[keyfield] - datacity[keyfield]
                             ) / datametar[keyfield]*100)
    return accuracy


def create_dataframe(data):
    AccuracyList = pd.DataFrame()
    i = 0
    while i < len(data):
        df = pd.DataFrame([data_accuracy(data[i], data[(i+1)])])
        AccuracyList = pd.concat([AccuracyList, df])
        i = i + 2
    DataList = pd.DataFrame(data)
    AllAccuracy = AccuracyList.mean(axis=0,numeric_only=True)
    AccuracyDict = AllAccuracy.to_dict()
    AccuracyDict["header"] = "Data Accuracy in %"
    DataList = pd.concat([DataList, pd.DataFrame([AccuracyDict])], axis=0)
    return DataList.dropna(axis=1)


# Exports the data to a csv file and makes a png plot about the accuracy of the data,
# filename should not contain the file extension
def export_dataframe(dataframe, filename):
    dataframe.to_csv((filename+".csv"), index=False)
    plt.close("all")
    plt.title("Accuracy of weather data from OpenWeatherMap in %")
    (dataframe.iloc[-1].drop(labels=["header"])).plot(kind="bar")
    plt.savefig(filename+".png")


# Metar Data from https://www.checkwx.com/ is not in the same format as OpenWeather,
# so we have to find a commonground and normalize the data
def normalize_metardata(data):
    data_normalized = {}
    data = data["data"][0]
    data_normalized["header"] = data['station']["location"] + " METAR Data"
    if (data.get("wind") is not None):
        data_normalized["windspeed"] = data["wind"]["speed_mps"]
        data_normalized["winddirection"] = data["wind"]["degrees"]
    else:
        data_normalized["windspeed"] = random()*20
        data_normalized["winddirection"] = random()*90
    if (data.get("humidity") is not None):
        data_normalized["humidity"] = data["humidity"]["percent"]
    else:
        data_normalized["humidity"] = 0
    if (data.get("barometer") is not None):
        data_normalized["pressure"] = data["barometer"]["mb"]
    else:
        data_normalized["pressure"] = random()*3
    if (data.get("temperature") is not None):
        data_normalized["temperatureincelsius"] = data["temperature"]["celsius"]
        data_normalized["temperatureinfahrenheit"] = data["temperature"]["fahrenheit"]
    else:
        data_normalized["temperatureincelsius"] = random()*30
        data_normalized["temperatureinfahrenheit"] = random()*100
    if (data.get("visibility") is not None):
        data_normalized["visibility"] = data["visibility"]["meters_float"]
    else:
        data_normalized["visibility"] = random()*10000
    if (data.get("rain") is not None):
        data_normalized["rain"] = data["rain"]["inches"]*2.54
    else:
        data_normalized["rain"] = 0
    if (data.get("snow") is not None):
        data_normalized["snow"] = data["snow"]["inches"]*2.54
    else:
        data_normalized["snow"] = 0
    return data_normalized


# OpenWeather Data from https://openweathermap.org/ is not in the same format as Metar,
# so we have to find a commonground and normalize the data
def normalize_citydata(data):
    data_normalized = {}
    data_normalized["header"] = data["name"] + " OpenWeather Data"
    if (data['weather_data'].get("wind") is not None):
        data_normalized["windspeed"] = data["weather_data"]["wind"]["speed"]
        data_normalized["winddirection"] = data['weather_data']["wind"]["deg"]
    else:
        data_normalized["windspeed"] = random()*20
        data_normalized["winddirection"] = random()*90

    if (data['weather_data']['main'].get("humidity") is not None):
        data_normalized["humidity"] = data["weather_data"]["main"]["humidity"]
    else:
        data_normalized["humidity"] = 0

    if (data['weather_data']['main'].get("pressure") is not None):
        data_normalized["pressure"] = data["weather_data"]["main"]["pressure"]
    else:
        data_normalized["pressure"] = random()*3
    data_normalized["temperatureincelsius"] = data["temperature"]['celsius']
    data_normalized["temperatureinfahrenheit"] = data["temperature"]['fahrenheit']
    if (data['weather_data'].get("visibility") is not None):
        data_normalized["visibility"] = data["weather_data"]["visibility"]
    else:
        data_normalized["visibility"] = random()*10000
    if (data['weather_data'].get("rain") is not None):
        data_normalized["rain"] = data["weather_data"]["rain"]["1h"]
    else:
        data_normalized["rain"] = 0
    if (data['weather_data'].get("snow") is not None):
        data_normalized["snow"] = data["weather_data"]["snow"]["1h"]
    else:
        data_normalized["snow"] = 0    
    return data_normalized
