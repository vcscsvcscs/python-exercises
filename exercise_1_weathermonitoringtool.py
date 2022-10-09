import datetime
import time
import requests
import os.path
import matplotlib.pyplot as plt


# Queries a cities location from external service (https://openweathermap.org/current),
# returns tuple with location info about the choosen city
def query_city_location(city, api_key):
    if not hasattr(query_city_location, "citylocationcache"):
        # it doesn't exist yet, so initialize it
        query_city_location.citylocationcache = {}
    # print(city," ",api_key)
    if (city in query_city_location.citylocationcache):
        return query_city_location.citylocationcache.get(city)
    locationUrl = "http://api.openweathermap.org/geo/1.0/direct?q=%s&limit=%d&appid=%s" % (
        city, 1, api_key)
    response = requests.get(locationUrl)
    locationData = response.json()
    query_city_location.citylocationcache[city] = (
        locationData[0]['lat'], locationData[0]['lon'])
    return query_city_location.citylocationcache[city]


# Queries the current weather info from external service (https://openweathermap.org/current),
# returns dictioanry with weather info about the choosen city
def query_weather_data(city, api_key):
    # fetch coordinates of the city
    # print(api_key)
    lat, lon = query_city_location(city, api_key)
    # fetch weather data
    weatherUrl = "https://api.openweathermap.org/data/2.5/weather?lat=%f&lon=%f&appid=%s" % (
        lat, lon, api_key)
    response = requests.get(weatherUrl)
    return response.json()


# takes a temperature in kelvin and returns it in celsius,fahrenheit tuple
def temperature_to_celsius_and_fahrenheit(temp):
    return (round(temp-273.15, 2), round((temp - 273.15) * (9/5) + 32, 2))


def time_until_sunrise_or_sunset(sunrise, sunset):
    untilSunrise = sunrise - datetime.datetime.now().timestamp()
    untilSunset = sunset - datetime.datetime.now().timestamp()
    if (0 < untilSunset and untilSunrise < 0):
        return ("until_sunset", time.strftime("%H:%M:%S", time.gmtime(untilSunset)))
    else:
        if (0 < untilSunrise):
            return ("until_sunrise", time.strftime("%H:%M:%S", time.gmtime(untilSunrise)))
        else:
            return ("until_sunrise", time.strftime("%H:%M:%S", time.gmtime(
                (untilSunrise) + datetime.timedelta(days=1).total_seconds())))


def predict_mood_from_weather(weather_data):
    celsius, fahrenheit = temperature_to_celsius_and_fahrenheit(
        weather_data['main']['feels_like'])
    moods = ["happy", "happy", "neutral", "calm", "depressed", "depressed",
             "aggressive", "aggressive", "aggressive", "aggressive", "aggressive"]
    current_mood = 0
    if (weather_data['clouds']['all'] > 50):
        current_mood += 2
    elif (weather_data['clouds']['all'] > 20):
        current_mood += 1
    if (weather_data['weather'][0]['main'] == "Clouds"):
        current_mood += 0
    if (weather_data['weather'][0]['main'] == "Rain"):
        if (weather_data['rain']['1h'] > 10):
            current_mood += 3
        elif (weather_data['rain']['1h'] > 3):
            current_mood += 2
        else:
            current_mood += 1
    if (weather_data['weather'][0]['main'] == "Clear"):
        current_mood += 0
    if (weather_data['weather'][0]['main'] == "Snow"):
        if (weather_data['snow']['1h'] > 3):
            current_mood += 3
        else:
            current_mood += 2
    if (celsius < 10):
        current_mood += 2
    elif (celsius < 18):
        current_mood += 1
    elif (celsius < 24):
        current_mood += 0
    elif (celsius < 30):
        current_mood += 1
    elif (celsius < 37):
        current_mood += 2
    else:
        current_mood += 4

    return moods[current_mood]


def compare_and_plot_weather_data(city1, city2, city3, city4, api_key):
    city1data = query_weather_data(city1, api_key)
    celsius, fahrenheit = temperature_to_celsius_and_fahrenheit(
        city1data['main']['temp'])
    city2data = query_weather_data(city2, api_key)
    celsius2, fahrenheit2 = temperature_to_celsius_and_fahrenheit(
        city2data['main']['temp'])
    city3data = query_weather_data(city3, api_key)
    celsius3, fahrenheit3 = temperature_to_celsius_and_fahrenheit(
        city3data['main']['temp'])
    city4data = query_weather_data(city4, api_key)
    celsius4, fahrenheit4 = temperature_to_celsius_and_fahrenheit(
        city4data['main']['temp'])
    citiestemp = [celsius, celsius2, celsius3, celsius4]
    cities = [city1, city2, city3, city4]
    colors = ['red', 'green', 'darkblue', 'lightblue']
    plt.bar(cities, citiestemp, color=colors)
    plt.suptitle('Temperature comparison in Celsius')
    if not os.path.exists("comparisonpics/"):
        os.makedirs("comparisonpics")
    plt.savefig(("comparisonpics/"+city1+city2+city3+city4+".png"))
