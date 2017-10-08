#!/usr/bin/env python2
"""
http://tinyurl.com/filtest
"""
import json
import os
import urllib2

from flask import Flask

HOME = os.getenv("HOME")
API_KEY = open(HOME + "/.weatherkey", "r").readlines()[0].strip()
URL = ('http://api.worldweatheronline.com/premium/v1/weather.ashx?key='
       '{0}&q=London&format=json&num_of_days=3&tp=1'.format(API_KEY))
TEMP_THRESHOLD = 15

def get_data(url):
    """ Fetch data from external API """
    data = urllib2.urlopen(url).read()
    json_data = json.loads(data)
    return json_data

JSON = get_data(URL)
#print JSON['data'].keys()


FLASK_APP = Flask(__name__)

@FLASK_APP.route('/time_to_heatwave', methods=['GET'])
def time_to_heatwave():
    return '{"hours_until_heatwave": "36" }'

def main():
    overall_hours = 0    # keep count of number of hours accross days
    for day in range(0, 3):  # iterate through days
        for hour in range(0, 23,):  # iterate through hours in a day
            overall_hours += 1  # increment overall hours
            # get temp for current hour
            temp = int(get_data(URL)['data']['weather'][day]['hourly'][hour]['tempC'])
            if temp > TEMP_THRESHOLD:
                hours_until_heatwave = overall_hours
                break  # Break out of loop as we have crossed the temp threshold
        else:
            continue  # contonue loop
        break  # break out of day threshold

    print "AMROX " + str(hours_until_heatwave)
    print len(get_data(URL)['data']['weather'][0]['hourly']) #[day]['maxtempC']
    #for day in range(0, 3):
      #print get_data(URL)['data']['weather'] #[day]['maxtempC']
    #FLASK_APP.run(debug=True, threaded=False)
    #get_heatwave_time()

if __name__ == '__main__':
    main()
