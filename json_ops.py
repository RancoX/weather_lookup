import json, requests, sys, logging
from msilib.schema import Error
from geopy.geocoders import Nominatim

'''
a simple app that reads user nominated place from command line and return the weather info
'''

# read location from command line
try:
    place=' '.join(sys.argv[1:])
except:
    print("Please input a place to get weather information for.")
    sys.exit()

# logging set up
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.disable(logging.INFO)

# get the lat and lon of parsed place 
geolocator=Nominatim(user_agent='weather_app')

try:
    location=geolocator.geocode(place)
except:
    raise Error("Invalid location, please revise your input.")
    
place = location.address
logging.warning(f"Application started, user input address: {' '.join(sys.argv[1:])} is mapped to {place}")
logging.warning('Now retrieving weather info...')

# get coordinates using geopy
lat, lon = location.latitude, location.longitude
logging.warning(f"Geographic coordinates extracted: ({lat}, {lon})")

location=geolocator.reverse(f"{lat},{lon}")

# get city and country name
address=location.raw['address']

# API key
API_KEY='19b55da089cdc480fc5baf851b7f7980'
URL=f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}"

# get weather info from openweathermap.org API
res=requests.get(URL)
res.raise_for_status()

# format and output
weather_info=json.loads(res.text)['list'][3]
temp=round(weather_info['main']['temp']-273.15,1)
pressure=weather_info['main']['pressure']
humidity=weather_info['main']['humidity']
weather_des=weather_info['weather'][0]['main']
wind=weather_info['wind']['speed']
logging.warning(f"The weather in {place} is {weather_des}, {temp} degrees, pressure: {pressure}, humidity: {humidity}. Wind speed: {wind}")