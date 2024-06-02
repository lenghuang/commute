'''

Usage, provide an NYC address:

python3 commute.py "159 East 33rd Street"

'''

import requests
from datetime import datetime, timedelta
import urllib
import pytz
import sys
import os
from dotenv import load_dotenv
from pathlib import Path

potential_apt = str(sys.argv[1]) + " New York City"

offices = {"office_len" : "PX6Q+C7 New York",
           "office_raj" : "Q24V+7G New York",
           "office_phi" : "Q26H+RH New York"}

# Get API Key
load_dotenv(Path(".env"))
api_key = os.getenv("GMAPS_API_KEY")



def get_tomorrow_nine_am_epoch():
    timezone = pytz.timezone('US/Eastern')
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_nine_am = datetime(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day, hour=9, minute=0, second=0)
    tomorrow_nine_am = timezone.localize(tomorrow_nine_am)
    epoch_time = int(tomorrow_nine_am.timestamp())
    return epoch_time

def get_transit_split(steps):
    transit_split = {}
    transit_desc = ""
    for step in steps:
        transit_desc += step["html_instructions"] + " || "
        if step["travel_mode"] in transit_split:
            transit_split[step["travel_mode"]] += int(step["duration"]["value"]) / 60
        else:
            transit_split[step["travel_mode"]] = int(step["duration"]["value"]) / 60
    return transit_split, transit_desc


def request_builder(office):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    url += "?origin=" + urllib.parse.quote(potential_apt)
    url += "&destination=" + urllib.parse.quote(office)
    url += "&mode=transit"
    url += "&arrival_time=" + str(get_tomorrow_nine_am_epoch())
    url += "&key=" + api_key
    return url

payload = {}
headers = {}

for name, pluscode in offices.items():
    url = request_builder(pluscode)
    response = requests.request("GET", url, headers=headers, data=payload)
    try:
        # Print the Total Duration of the Trip
        print(name, response.json()["routes"][0]["legs"][0]["duration"]["text"])
        # Print How the Time is Split Up
        transit_split, transit_desc = get_transit_split(response.json()["routes"][0]["legs"][0]["steps"])
        for mode, duration in transit_split.items():
            print("->", mode, "for", round(duration, 2), "minutes")
        # Print the Instructions
        print("->", transit_desc)
        print("")
    except:
        print("ERROR OCCURED")
