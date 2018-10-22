#!/usr/bin/env python

import os
import sys
import json
#from time import time.localtime, time.strftime, tzset, tzname
import time
import requests
from geopy.geocoders import Nominatim
from flask import Flask
from flask import render_template
from pprint import pprint

DARK_SKY = {
    "api_url": "https://api.darksky.net/forecast",
    "img_url": "https://darksky.net/images/weather-icons",
    "img_ext": "png"
}

def get_weather():
  global DARK_SKY
  key = str(os.environ['DARKSKY_API_KEY'])
  gps = str(os.environ['GPS_COORDINATES'])
  url = '{}/{}/{}'.format(DARK_SKY['api_url'], key, gps)
  r = requests.get(url)
  return(r.json())
  # with open('sample.json') as fh:
  #   return(json.load(fh))

def compass(bearing):
  coords = {
    'N':  [0, 22.5],
    'NE': [22.5, 67.5],
    'E':  [67.5, 112.5],
    'SE': [112.5, 157.5],
    'S':  [157.5, 202.5],
    'SW': [202.5, 247.5],
    'W':  [247.5, 292.5],
    'NW': [292.5, 337.5],
    'N':  [337.5, 360]
  }
  for k,v in coords.items():
    if bearing >= v[0] and bearing < v[1]:
      return k

def location(coords):
  geolocator = Nominatim(user_agent="thecase/nook-weather")
  return(geolocator.reverse(str(coords)).address)

def format_time(tz, format, utime):
  os.environ['TZ'] = tz
  time.tzset()
  return time.strftime(format, time.localtime(utime))

def process_data():
  data = get_weather()
  tz = data['timezone']
  unixtime = data['currently']['time']
  now = data['currently']
  now['time'] = format_time(tz, '%A, %B %d %Y', unixtime)
  now['timestamp'] = format_time(tz, '%Y-%m-%d %H:%M:%S', unixtime)
  # only available when all stations are reporing
  # now['hour'] = data['minutely']['summary']
  now['day'] =  data['hourly']['summary']
  now['high'] = data['daily']['data'][0]['temperatureHigh']
  now['low'] =  data['daily']['data'][0]['temperatureLow']
  now['forecast'] = data['daily']['summary']
  now['windDir'] = compass(int(data['currently']['windBearing']))
  now['city'] = location(os.environ['GPS_COORDINATES'])

  hourly = list()
  for i in [2, 4, 6, 8, 10, 12]:
    forecast = data['hourly']['data'][i]
    time = format_time(tz, '%-I %p', int(forecast['time']))
    hourly.append({"time": time, "icon": forecast['icon'],
                   "temp": forecast['temperature']})

  daily = list()
  for i in range(6):
    forecast = data['daily']['data'][i]
    date = format_time(tz, '%m/%d', int(forecast['time']))
    day  = format_time(tz, '%A', int(forecast['time']))
    daily.append(
        {"day": day, "date": date, "icon": forecast['icon'],
         "high": forecast['temperatureHigh'],
         "low":  forecast['temperatureLow']
        })
  return({'now': now, 'hourly': hourly, 'daily': daily})


app = Flask(__name__)
@app.route('/')
def index():
  """ index page function. """
  global DARK_SKY
  pd = process_data()
  return render_template('index.html', now=pd['now'], hourly=pd['hourly']
                                     , daily=pd['daily'], ds=DARK_SKY)


if __name__ == '__main__':
  if 'DARKSKY_API_KEY' not in os.environ:
    print("ERROR Please set the environment variable DARKSK_API_KEY")
    sys.exit(1)
  app.run(debug=True, host='0.0.0.0', port=int(os.environ['BIND_PORT']))
