#!/usr/bin/python3

import argparse
import urllib3
from bs4 import BeautifulSoup
import prettytable
from termcolor import colored

parser = argparse.ArgumentParser(description='Gets 10 Day and Hourly Weather.')
parser.add_argument('zip', nargs=1, default=11217,
        help='Provide a zipcode to look up universe (my apartment)')
args = parser.parse_args()

def get_now():
 
    http = urllib3.PoolManager()
    now_page = http.request('GET', 'http://www.weather.com/weather/today/%s' % 
                 args.zip[0]) 
    now_soup = BeautifulSoup(now_page.data)
 
    now = now_soup.find(class_ = 'wx-temperature').text
    wind = now_soup.find(class_ = 'wx-wind-label').text
 
    print(colored('\nCurrent Temperature: ' + now + " | Wind: " + wind + '\n', 'red'))
 
 
def get_tenday():
 
    date = []
    hi   = []
    low  = []
    condition = []
    chance_rain = []
 
    http = urllib3.PoolManager()
 
    tendaypage = http.request('GET', 'http://www.weather.com/weather/tenday/%s' 
                      % args.zip[0]) 
    tenday_soup = BeautifulSoup(tendaypage.data)
    wx_daypart = tenday_soup.find_all(class_ = "wx-daypart")
 
    for x in wx_daypart:
        date.append(x.h3.span.text)
        hi.append(x.div.p.text[1:3])
        low.append(x.div.find(class_ = "wx-temp-alt").text[1:3])
        try:
            condition.append(x.div.find(class_ = 'wx-phrase').text)
        except:
            condition.append("not provided")
        try:
            chance_rain.append(x.dl.dd.text)
        except:
            chance_rain.append("not provided")
 
    p = prettytable.PrettyTable()
 
    print(colored('\nTen Day Forecast:\n', 'yellow'))
 
    p.add_column('Date', date)
    p.add_column('hi', hi)
    p.add_column('low', low)
    p.add_column('Chance of Rain', chance_rain)
    p.add_column('Condition', condition)
    p.align['Condition'] = 'l'
 
    print(p)
 
def get_hourly():
 
    hour = []
    temp = []
    condition = []
    feels_like = []
    humidity = []
    precipitation = []
    wind = []
 
    http = urllib3.PoolManager()
    hourly_page = http.request('GET', 
            'http://www.weather.com/weather/hourbyhour/graph/%s' % args.zip[0])
 
    hourly_soup = BeautifulSoup(hourly_page.data)
    wx_forecast_container = hourly_soup.find(id = 'wx-forecast-container')
    wx_timepart = wx_forecast_container.div.findNextSiblings(class_ =
            'wx-timepart')
 
    for x in wx_timepart:
        hour.append(x.h3.text[0:5].strip())
        temp.append(x.p.text[0:4].strip())
        condition.append(x.find(class_ = 'wx-phrase').text)
        feels_like.append(x.find_all("dd")[0].text.strip())
        humidity.append(x.find_all("dd")[1].text.strip())
        precipitation.append(x.find_all("dd")[2].text.strip())
        wind.append(x.find_all("dd")[3].text)
 
    print(colored('\nHourly Forecast:\n', 'yellow'))
 
    p = prettytable.PrettyTable() 
    p.add_column('Hour', hour)
    p.add_column('Temp', temp)
    p.add_column('Feels Like', feels_like)
    p.add_column('Humidity', humidity)
    p.add_column('Precip', precipitation)
    p.add_column('Wind', wind)
    p.add_column('Condition', condition)
    p.align['Condition'] = 'l'
    p.align['Wind'] = 'l'
 
    print(p)
 
if __name__ == '__main__': 
    get_now()
    get_tenday()
    get_hourly()
