__author__ = 'wbjohnston'
import unittest
import os
import json
from pywmta import WMTAApi

BASE_DIR = os.path.dirname(__file__)
KEYFILE_PATH = '/'.join((BASE_DIR, 'resources/key'))

class PyWMTATests(unittest.TestCase):
    routes = ['10A', '10B', '10C', '11Y', '15K']
    stations = ['1A']
    def test_line_request(self):
        #read in key
        with open(KEYFILE_PATH, 'r') as f:
            key = f.read()

        wmta = WMTAApi(key)
        data = wmta.rail_station.lines()
        self.assertIsNotNone(data)








if __name__ == '__main__':
    unittest.main()
