# Python Exercises
 
To run any of these programs you have to have python and pip installed, then you can run the following command that installs all the dependencies:

    `pip install -r requirements.txt`

To host the weathermonitoringtool on your localhost port 8080 run the following command:

    `python exercise_1_wmt_server.py`

## Api Documentation/Examples

### City Information /%city%?api_key=%key%

    Returns a json that contains information(name,celsius,fahrenheit,mood,weather_data,time until sunrise or sunset) on the specified city.

Example:

    `http://localhost:8080/Budapest?api_key=76717af25a09a9c55ca00b44f771acc0`

json-response:

    `{"name": "Budapest", "celsius": 12.68, "fahrenheit": 54.82, "mood": "calm", "weather_data": {"coord": {"lon": 19.0404, "lat": 47.498}, "weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04n"}], "base": "stations", "main": {"temp": 285.83, "feels_like": 285.32, "temp_min": 284.44, "temp_max": 285.83, "pressure": 1019, "humidity": 83}, "visibility": 8000, "wind": {"speed": 1.03, "deg": 0}, "clouds": {"all": 98}, "dt": 1665266312, "sys": {"type": 2, "id": 2009566, "country": "HU", "sunrise": 1665204718, "sunset": 1665245438}, "timezone": 7200, "id": 7284844, "name": "Budapest", "cod": 200}, "until_sunrise": "06:52:51"}`

### City Weather-Data /%city%/weatherdata?api_key=%key%>

    Returns a json that contains information(weather_data) on the specified city.

Example:

    `http://localhost:8080/Budapest/weatherdata?api_key=76717af25a09a9c55ca00b44f771acc0`

json-response:

    `{"coord": {"lon": 19.0404, "lat": 47.498}, "weather": [{"id": 804, "main": "Clouds", "description": "overcast clouds", "icon": "04n"}], "base": "stations", "main": {"temp": 285.83, "feels_like": 285.32, "temp_min": 284.44, "temp_max": 285.83, "pressure": 1019, "humidity": 83}, "visibility": 8000, "wind": {"speed": 1.03, "deg": 0}, "clouds": {"all": 98}, "dt": 1665266312, "sys": {"type": 2, "id": 2009566, "country": "HU", "sunrise": 1665204718, "sunset": 1665245438}, "timezone": 7200, "id": 7284844, "name": "Budapest", "cod": 200}`

### City Temperature /%city%/temperature?api_key=%key%>

    Returns a json that contains current temperature in celsius and fahrenheit on the specified city.

Example:

    `http://localhost:8080/Budapest/temperature?api_key=76717af25a09a9c55ca00b44f771acc0`

json-response:

    `{"celsius": 12.68, "fahrenheit": 54.82}`

### City Mood prediction /%city%/mood?api_key=%key%>

    Returns a json that contains a mood prediction based on current information.

Example:

    `http://localhost:8080/Budapest/mood?api_key=76717af25a09a9c55ca00b44f771acc0`

json-response:

    `{"mood": "calm"}`

### City Time until next sunrise or sunset /%city%/time_until_sunrise_or_sunset?api_key=%key%>

    Returns a json that contains the time(h/m/s) until the next sunset or sunrise.

Example:

    `http://localhost:8080/Budapest/time_until_sunrise_or_sunset?api_key=76717af25a09a9c55ca00b44f771acc0`

json-response:

    `{"until_sunrise": "05:59:35"}`

### Compare 4 cities temperature /comparecities?city1=%city1%&city2=%city2%&city3=%city3%&city4=%city4%&api_key=%key%>

    Creates a comparison of 4 cities's current temperature(in celsius) on the server as a png file, then serves it.

Example:

    `http://localhost:8080/comparecities?city1=Warsaw&city2=Budapest&city3=Prague&city4=Wien&api_key=76717af25a09a9c55ca00b44f771acc0`

response-content-type:  `image/png`

## For solving

When solving an exercise use the following filenaming rule:

exercise_x_<custom part>.py

exercise_x_test_<custom part>.py

Write tests in a separate python file for each exercises.
These could be unit tests or functional tests or both.