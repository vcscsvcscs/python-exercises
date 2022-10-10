import unittest
from exercise_2_metar_validation import query_metar_data, create_dataframe, normalize_metardata, normalize_citydata
from exercise_1_weathermonitoringtool import query_weather_data, temperature_to_celsius_and_fahrenheit
from exercise_1_weathermonitoringtool import time_until_sunrise_or_sunset, predict_mood_from_weather,query_city_location

class TestMetarValidation(unittest.TestCase):
    cities = ["Warsaw", "Budapest", "Prague", "Wien"]
    Mapi_key = "93da3fc598a24d2abd890be530"
    Oapi_key = "76717af25a09a9c55ca00b44f771acc0"
    def test_query_metar_data(self):
        lat,lon = query_city_location(self.cities[1],self.Oapi_key)
        metardata = query_metar_data(lat,lon, self.Mapi_key)
        print(metardata["data"][0],'\n')
        weather_data = query_weather_data(self.cities[1], self.Oapi_key)
        celsius, fahrenheit = temperature_to_celsius_and_fahrenheit(
            weather_data['main']['temp'])
        untilsmth, time = time_until_sunrise_or_sunset(
            weather_data['sys']['sunrise'], weather_data['sys']['sunset'])
        data ={"name": self.cities[1], 'temperature':{"celsius": celsius, "fahrenheit": fahrenheit},
                "mood": predict_mood_from_weather(weather_data), "weather_data": weather_data, untilsmth: time}
        print(data,'\n')
        print(normalize_citydata(data),'\n')
        print(normalize_metardata(metardata),'\n')
        print(create_dataframe(normalize_citydata(data),normalize_metardata(metardata)))
        
        
if __name__ == '__main__':
    unittest.main()