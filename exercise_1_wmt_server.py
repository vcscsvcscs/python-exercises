from bottle import Bottle, request
from exercise_1_weathermonitoringtool import query_weather_data, temperature_to_celsius_and_fahrenheit
from exercise_1_weathermonitoringtool import time_until_sunrise_or_sunset, predict_mood_from_weather

wmt_server = Bottle()


@wmt_server.route('/<city>')
def cityfullinfo(city):
    weather_data = query_weather_data(city, request.query.get("api_key"))
    celsius, fahrenheit = temperature_to_celsius_and_fahrenheit(
        weather_data['main']['temp'])
    return {"name": city, "celsius": celsius, "fahrenheit": fahrenheit,
            "mood": predict_mood_from_weather(weather_data), "weather_data": weather_data}


@wmt_server.route('/<city>/weatherdata')
def weatherdata(city):
    return query_weather_data(city, request.query.get("api_key"))


@wmt_server.route('/<city>/temperature')
def citytemperature(city):
    weather_data = query_weather_data(city, request.query.get("api_key"))
    celsius, fahrenheit = temperature_to_celsius_and_fahrenheit(
        weather_data['main']['temp'])
    return {"celsius": celsius, "fahrenheit": fahrenheit}


@wmt_server.route('/<city>/mood')
def citymood(city):
    weather_data = query_weather_data(city, request.query.get("api_key"))
    return {"mood": predict_mood_from_weather(weather_data)}


@wmt_server.route('/<city>/time_until_sunrise_or_sunset')
def citytimeuntilsunriseorsunset(city):
    weather_data = query_weather_data(city, request.query.get("api_key"))
    untilwhat, time = time_until_sunrise_or_sunset(
        weather_data['sys']['sunrise'], weather_data['sys']['sunset'])
    return {untilwhat: time}


"""@wmt_server.route('/comparecities')
def comparecities():
    weather_data1 = query_weather_data(request.query.get("city1"),request.query.get("api_key"))
    weather_data2 = query_weather_data(request.query.get("city2"),request.query.get("api_key"))
    weather_data3 = query_weather_data(request.query.get("city3"),request.query.get("api_key"))
    weather_data4 = query_weather_data(request.query.get("city4"),request.query.get("api_key"))
    """

if __name__ == '__main__':
    wmt_server.run(host='localhost', port=8080)
