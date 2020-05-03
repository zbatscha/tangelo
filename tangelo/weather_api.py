import os
import requests
import json

def getWeather(lat, long):
    weather = None
    weather_key = 'ff9101a1b97b3e7617260a4da9012daa' # os.environ.get('WEATHER_KEY')
    if not lat or not long or not weather_key:
        raise Exception('Weather is down.')

    open_weather_url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={weather_key}'
    try:
        response = requests.get(url=open_weather_url)
        response.raise_for_status()
        weather = json.loads(response.content)
    except requests.exceptions.HTTPError as e:
        log.error(f'Error in weather: ', exc_info=True)
        raise Exception('Weather is down.')

    weather_info = weather["main"]

    current_temperature = weather_info["temp"]
    current_temperature = ((current_temperature - 273.15) * 9/5) + 32
    current_temperature = "{:.1f}".format(current_temperature)
    weather_description = weather["weather"][0]
    weather_description = weather_description.get('description')

    return {'temperature': current_temperature, 'description': weather_description}

if __name__=="__main__":
    lat = 34.286320
    long = -118.712799
    print(getWeather(lat, long))
