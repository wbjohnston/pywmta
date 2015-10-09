__author__ = 'wbjohnston'
import unittest
import os
import logging
import json
from pywmta import WMTAApi
import requests
from requests.exceptions import HTTPError

BASE_DIR = os.path.dirname(__file__)

KEYFILE_PATH = '/'.join((BASE_DIR, 'resources/key'))

class PyWMTATests(unittest.TestCase):
    def test_line_request(self):
        try:
            with open(KEYFILE_PATH, 'r') as f:
                key = f.read()
        except Exception as e:
            raise e

        wmta = WMTAApi(key)
        response = wmta.rail_station.information('A01')

        print(json.dumps(response, indent=4, separators=(',', ': ')))








if __name__ == '__main__':
    unittest.main()
