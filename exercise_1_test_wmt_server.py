import datetime
import unittest
from urllib import response
from exercise_1_wmt_server import wmt_server
from exercise_1_weathermonitoringtool import query_weather_data
from webtest import TestApp


class TestWMTServer(unittest.TestCase):
    city = "Budapest"
    # this api key is under the acount of the author of this snippet and is solely for testing purposes,
    # it blocks after 60 requests per minute and 1000 requests per day
    api_key = "76717af25a09a9c55ca00b44f771acc0"
    test_app = TestApp(wmt_server)

    def test_query_weather_data(self):
        response = self.test_app.get(
            '/%s/weatherdata?api_key=%s' % (self.city, self.api_key))
        weather_data = response.json
        self.assertEqual(weather_data['name'], self.city)
        self.assertEqual(weather_data['sys']['country'], 'HU')
        self.assertEqual(weather_data['timezone'], 7200)
        self.assertEqual(weather_data['id'], 3054643)
        self.assertEqual(weather_data['cod'], 200)

    def test_query_city_data(self):
        response = self.test_app.get(
            '/%s?api_key=%s' % (self.city, self.api_key))
        data = response.json
        weather_data = data['weather_data']
        self.assertEqual(weather_data['name'], self.city)
        self.assertEqual(weather_data['sys']['country'], 'HU')
        self.assertEqual(weather_data['timezone'], 7200)
        self.assertEqual(weather_data['id'], 3054643)
        self.assertEqual(weather_data['cod'], 200)

    def test_city_temperature(self):
        response = self.test_app.get(
            '/%s/temperature?api_key=%s' % (self.city, self.api_key))
        data = response.json
        self.assertTrue(data.get("celsius") != None)
        self.assertTrue(data.get("fahrenheit") != None)

    def test_city_mood(self):
        response = self.test_app.get(
            '/%s/mood?api_key=%s' % (self.city, self.api_key))
        data = response.json
        self.assertTrue(data.get("mood") != None)

    def test_time_until_sunrise_or_sunset(self):
        weather_data = query_weather_data(self.city, self.api_key)
        response = self.test_app.get(
            '/%s/time_until_sunrise_or_sunset?api_key=%s' % (self.city, self.api_key))
        data = response.json
        if (datetime.datetime.now().timestamp() < weather_data['sys']['sunrise'] or
                datetime.datetime.now().timestamp() > weather_data['sys']['sunset']):
            self.assertTrue(data.get("until_sunrise") != None)
        else:
            self.assertTrue(data.get("until_sunset") != None)


if __name__ == '__main__':
    unittest.main()
