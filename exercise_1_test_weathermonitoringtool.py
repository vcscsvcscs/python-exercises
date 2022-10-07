import unittest
from exercise_1_weathermonitoringtool import query_weather_data, temperature_to_celsius_and_fahrenheit

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

if __name__ == '__main__':
    unittest.main()