#!/usr/bin/env python

"""
Unit tests for temperature API
"""

import unittest
import temperature

class TempTest(unittest.TestCase):
    """ Temperature test class """

    def test_get_heatwave_time(self):
        """ test the get_heatwave_time endpoint """

        client = temperature.FLASK_APP.test_client()
        result = client.get('/time_to_heatwave')
        self.assertEqual(result.status_code, 200)

    def test_next_10_days(self):
        """ test the next_10_days endpoint """

        client = temperature.FLASK_APP.test_client()
        result = client.get('/next_10_days')
        self.assertEqual(result.status_code, 200)

    def test_bad_endpoint(self):
        """ test non-existant endpoint """

        client = temperature.FLASK_APP.test_client()
        result = client.get('/bad_endpoint')
        self.assertEqual(result.status_code, 404)
