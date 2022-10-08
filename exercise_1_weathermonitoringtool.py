import datetime
import time
import requests
import matplotlib.pyplot as plt


# Queries a cities location from external service (https://openweathermap.org/current),
# returns tuple with location info about the choosen city
def query_city_location(city, api_key):
    if not hasattr(query_city_location, "counter"):
        # it doesn't exist yet, so initialize it
        query_city_location.citylocationcache = {}
    if (query_city_location.citylocationcache.get(city) != None):
        return query_city_location.citylocationcache.get(city)
    locationUrl = "http://api.openweathermap.org/geo/1.0/direct?q=%s&limit=%d&appid=%s" % (
        city, 1, api_key)
    response = requests.get(locationUrl)
    locationData = response.json()
    query_city_location.citylocationcache[city] = (
        locationData[0]['lat'], locationData[0]['lon'])
    return (locationData[0]["lat"], locationData[0]["lon"])


# Queries the current weather info from external service (https://openweathermap.org/current),
# returns dictioanry with weather info about the choosen city
def query_weather_data(city, api_key):
    # fetch coordinates of the city
    lat, lon = query_city_location(city, api_key)
    # fetch weather data
    weatherUrl = "https://api.openweathermap.org/data/2.5/weather?lat=%f&lon=%f&appid=%s" % (
        lat, lon, api_key)
    response = requests.get(weatherUrl)
    return response.json()


# takes a temperature in kelvin and returns it in celsius,fahrenheit tuple
def temperature_to_celsius_and_fahrenheit(temp):
    return (round(temp-273.15, 2), round((temp - 273.15) * (9/5) + 32, 2))


def time_until_sunrise_or_sundown(sunrise, sunset):
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
    city2data = query_weather_data(city2, api_key)
    city3data = query_weather_data(city3, api_key)
    city4data = query_weather_data(city4, api_key)
    plt.savefig("comparison.png")