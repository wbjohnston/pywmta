"""
@author: Will Johnston <wbjohnston@gmail.com>
@date: September 8th, 2015

"""

import json as _json
from xml.parsers import expat as _xml
from urllib.request import Request as _Request
from urllib.request import urlopen as _urlopen
from urllib.parse import urlencode as _urlencode

"""
api calls
=========
next buses (NextBusService, Predictions, Predictions)
next trains (StationPrediction, GetPrediction, Trains)
lines (Rail, Lines, Lines)
parking (Rail, StationParking, StationsParking)




"""

class WMTA(object):
    #all requests go through this url in some way
    BASE_URL = 'https://api.wmata.com'
    ENDPOINT_MAP = {

    }

    def __init__(self, api_key, mode='json'):
        if mode not in ('xml', 'json'):
            raise ValueError('invalid encoding mode: {}'.format(self.mode))
        self.mode = mode
        self.api_key = api_key


    def _decode(self, st):
        if self.mode == 'json':
            return _json.loads(st)
        elif self.mode == 'xml':
            return _xml.ParserCreate(encoding='utf-8').Parse(st)
        else:
            raise ValueError('invalid encoding mode: {}'.format(self.mode))


    def _construct_url(self, service, endpoint, query):
        service += '.svc' #append service suffix

        #if in json mode prepend a j to the endpoint name
        if self.mode == 'json':
            endpoint = 'j' + endpoint

        #prepare query
        if type(query) is dict:
            #alter all lists to csv strings
            for key in query:
                if type(query[key]) is list:
                    query[key] = ', '.join(query[key])

        query = _urlencode(query)

        path = '/'.join((self.BASE_URL, service, self.mode))
        return '?'.join(path, query) #full url query


    def _fetch(self, service, endpoint, query):
        url = self._construct_url(service, endpoint, query)
        req = _Request(url, headers={'api_key': self.api_key})

        with _urlopen(req) as r:
            response = str(r.read(), encode='utf-8')

        return self._decode(response)



