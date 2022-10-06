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

