import unittest
from exercise_1_wmt_server import wmt_server
from webtest import TestApp

class TestWMTServer(unittest.TestCase):
    def test_query_weather_data(self):
        city = "Budapest"
        #this api key is under the acount of the author of this snippet and is solely for testing purposes, it blocks after 60 requests per minute and 1000 requests per day
        api_key = "76717af25a09a9c55ca00b44f771acc0"
        test_app = TestApp(wmt_server)
        response = test_app.get('/weatherdata?city=%s&api_key=%s' % (city, api_key))
        weather_data = response.json
        self.assertEqual(weather_data['name'], city)
        self.assertEqual(weather_data['sys']['country'], 'HU')
        self.assertEqual(weather_data['timezone'], 7200)
        self.assertEqual(weather_data['id'], 3054643)
        self.assertEqual(weather_data['cod'], 200)

if __name__ == '__main__':
    unittest.main()