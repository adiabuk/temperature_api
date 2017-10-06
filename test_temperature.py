#!/usr/bin/env python

import unittest
import temperature

class TempTest(unittest.TestCase):
    def test_get_heatwave_time(self):
        """ test the get_heatwave_time endpoint """

        client = temperature.FLASK_APP.test_client()
        result = client.get('/time_to_heatwave')
        self.assertEqual(result.status_code, 200)
