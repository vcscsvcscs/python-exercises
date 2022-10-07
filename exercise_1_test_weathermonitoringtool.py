import datetime
from time import time
import unittest
from exercise_1_weathermonitoringtool import query_weather_data, temperature_to_celsius_and_fahrenheit, time_until_sunrise_or_sundown, predict_mood_from_weather

class TestWeatherMonitoringTool(unittest.TestCase):
    def test_query_weather_data(self):
        city = "Budapest"
        #this api key is under the acount of the author of this snippet and is solely for testing purposes, it blocks after 60 requests per minute and 1000 requests per day
        api_key = "76717af25a09a9c55ca00b44f771acc0"
        weather_data = query_weather_data(city, api_key)
        self.assertEqual(weather_data['name'], city)
        self.assertEqual(weather_data['sys']['country'], 'HU')
        self.assertEqual(weather_data['timezone'], 7200)
        self.assertEqual(weather_data['id'], 3054643)
        self.assertEqual(weather_data['cod'], 200)

    def test_temperature_to_celsius_and_fahrenheit(self):
        temp = 300
        celsius, fahrenheit = temperature_to_celsius_and_fahrenheit(temp)
        self.assertEqual(celsius, 26.85)
        self.assertEqual(fahrenheit, 80.33)
    
    def test_time_until_sunrise_or_sundown(self):
        city = "Budapest"
        #this api key is under the acount of the author of this snippet and is solely for testing purposes, it blocks after 60 requests per minute and 1000 requests per day
        api_key = "76717af25a09a9c55ca00b44f771acc0"
        weather_data = query_weather_data(city, api_key)
        untilwhat,time = time_until_sunrise_or_sundown(weather_data['sys']['sunrise'], weather_data['sys']['sunset'])
        if(datetime.datetime.now().timestamp() < weather_data['sys']['sunrise'] or datetime.datetime.now().timestamp() > weather_data['sys']['sunset']):
            self.assertEqual(untilwhat, "until_sunrise")
        else:
            self.assertEqual(untilwhat, "until_sunset")

    def test_predict_mood_from_weather(self):    
        weather_data = {'weather':[{'main':'Rain'}],'rain':{'1h':4},'clouds':{'all':100},'main':{'feels_like':300}}
        mood = predict_mood_from_weather(weather_data)
        self.assertEqual(mood, "depressed")
        weather_data = {'weather':[{'main':'Clear'}],'clouds':{'all':20},'main':{'feels_like':290}}
        mood = predict_mood_from_weather(weather_data)
        self.assertEqual(mood, "happy")
        weather_data = {'weather':[{'main':'Rain'}],'rain':{'1h':16},'clouds':{'all':50},'main':{'feels_like':320}}
        mood = predict_mood_from_weather(weather_data)
        self.assertEqual(mood, "aggressive")

if __name__ == '__main__':
    unittest.main()