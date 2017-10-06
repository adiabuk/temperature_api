#!/usr/bin/env python2

import os

from flask import Flask, request, abort, Response

HOME = os.getenv("HOME")
APIKEY = open(HOME + "/.weatherkey", "r").readlines()[0].strip()

# FIXME:
#os.system("curl 'http://api.worldweatheronline.com/premium/v1/weather.ashx?key={0}&q=London&format=json&num_of_days=3&tp=1'".format(APIKEY))

FLASK_APP = Flask(__name__)

@FLASK_APP.route('/time_to_heatwave', methods=['GET'])
def time_to_heatwave():
    return '{"hours_until_heatwave": "36" }'

def main():
    FLASK_APP.run(debug=True, threaded=False)
    #get_heatwave_time()

if __name__ == '__main__':
    main()
