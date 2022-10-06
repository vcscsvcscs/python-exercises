from bottle import route, run, Bottle, request, response
from exercise_1_weathermonitoringtool import query_weather_data

wmt_server = Bottle()
@wmt_server.route('/weatherdata')
def weatherdata():
    return query_weather_data(request.query.get("city"), request.query.get("api_key"))

if __name__ == '__main__':
    wmt_server.run(host='localhost', port=8080)
