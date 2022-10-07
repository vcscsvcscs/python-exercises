import datetime
import time
import requests
#Queries the current weather info from external service (https://openweathermap.org/current), returns dictioanry with weather info about the choosen city
def query_weather_data(city,api_key):
    #fetch coordinates of the city
    locationUrl = "http://api.openweathermap.org/geo/1.0/direct?q=%s&limit=%d&appid=%s" % (city, 1, api_key)
    response = requests.get(locationUrl)
    locationData = response.json()
    #fetch weather data
    weatherUrl = "https://api.openweathermap.org/data/2.5/weather?lat=%f&lon=%f&appid=%s" % (locationData[0]["lat"], locationData[0]["lon"], api_key)
    response = requests.get(weatherUrl)
    return response.json()

#takes a temperature in kelvin and returns it in celsius,fahrenheit tuple
def temperature_to_celsius_and_fahrenheit(temp):
    return (round(temp-273.15,2),round((temp - 273.15)* (9/5) + 32,2))

def time_until_sunrise_or_sundown(sunrise,sunset):
    untilSunrise = sunrise - datetime.datetime.now().timestamp()
    untilSunset = sunset - datetime.datetime.now().timestamp()
    if(0 < untilSunset and untilSunrise < 0):
        return ("until_sunset",time.strftime("%H:%M:%S", time.gmtime(untilSunset)))
    else:
        if(0 < untilSunrise):
            return ("until_sunrise",time.strftime("%H:%M:%S", time.gmtime(untilSunrise)))
        else:
            return ("until_sunrise",time.strftime("%H:%M:%S", time.gmtime(24 *datetime.time.hour+untilSunrise)))