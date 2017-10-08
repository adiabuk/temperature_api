#!/usr/bin/env python2
#pylint: disable=global-statement

"""
http://tinyurl.com/filtest
"""

import json
import os
import sched
import sys
import threading
import time
import urllib2

from flask import Flask

DATA = None
HOME = os.getenv("HOME")

# Get API key from file if it exists, otherwise default to env var
try:
    API_KEY = open(HOME + "/.weatherkey", "r").readlines()[0].strip()
except IOError:
    API_KEY = os.getenv("API_KEY")

if API_KEY is None:
    sys.exit('API Key not found, unable to proceed')

URL = ('http://api.worldweatheronline.com/premium/v1/weather.ashx?key='
       '{0}&q=London&format=json&num_of_days=3&tp=1'.format(API_KEY))
TEMP_THRESHOLD = 27
TIMER = 3600
FLASK_APP = Flask(__name__)
SCHED = sched.scheduler(time.time, time.sleep)

def schedule_data(scheduler):
    """
    Scheduler function for fetching data hourly
    Runs in a background thread to not interfere with flask
    """

    global DATA
    try:
        DATA = get_data(URL)
        sys.stdout.write("Successfullly fetched data")
    except urllib2.URLError:
        sys.stderr.write("Error opening URL\n")

    SCHED.enter(TIMER, 1, schedule_data, (scheduler,))

def get_data(url):
    """ Fetch data from external API """
    data = urllib2.urlopen(url).read()
    json_data = json.loads(data)
    return json_data



@FLASK_APP.route('/time_to_heatwave', methods=['GET'])
def time_to_heatwave():
    """
    API endpoint to return number of hours to next heatwave as JSON
    """
    return '{"hours_until_heatwave": %s}'% calculate_time()

def main():
    """
    Main function
    Start scheduler to fetch data, and Flask API to serve data
    """
    # enter scheduler and fetch data immediately (0 seconds) for initial data
    # Scheduler will handle future runs
    SCHED.enter(0, 1, schedule_data, (SCHED,))
    background_thread = threading.Thread(target=SCHED.run, args=())
    background_thread.start()

    # start Flask
    FLASK_APP.run(debug=True, threaded=True)

def calculate_time():
    """
    Calculate and return time to next heatwave if data is present
    """

    if DATA is None:
        # If data has not yet been successfully fetched
        return "No Data"

    hours_until_heatwave = "None"
    overall_hours = 0    # keep count of number of hours accross days
    for day in range(0, 3):  # iterate through days
        for hour in range(0, 23,):  # iterate through hours in a day
            overall_hours += 1  # increment overall hours
            # get temp for current hour
            temp = int(DATA['data']['weather'][day]['hourly'][hour]['tempC'])
            if temp > TEMP_THRESHOLD:
                hours_until_heatwave = overall_hours
                break  # Break out of loop as we have crossed the temp threshold
        else:
            continue  # contonue loop
        break  # break out of day threshold
    return hours_until_heatwave

if __name__ == '__main__':
    main()
