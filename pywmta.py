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

    def __init__(self, api_key, mode='json'):
        if mode not in ('xml', 'json'):
            raise ValueError('invalid encoding mode: {}'.format(self.mode))
        self.mode = mode
        self.api_key = api_key

    def get_valid_services(self):
        return ('Bus',
                'Incidents',
                'Rail',
                'NextBusService',
                'StationPrediction')

    def get_valid_endpoints(self):
        return ()


    def _decode(self, st):
        if self.mode == 'json':
            return _json.loads(st)
        elif self.mode == 'xml':
            return _xml.ParserCreate(encoding='utf-8').Parse(st)
        else:
            raise ValueError('invalid encoding mode: {}'.format(self.mode))


    def _construct_url(self, service, endpoint, query):
        #if in json mode prepend a j to the endpoint name
        #the Incidents service and StationPrediction service does not follow this scheme
        if self.mode == 'json' and (service not in ('Incidents', 'StationPrediction')):
            endpoint = 'j' + endpoint

        service += '.svc' #append service suffix

        #prepare query
        if type(query) is dict:
            #alter all lists to csv strings
            for key in query:
                if type(query[key]) is list:
                    query[key] = ', '.join(query[key])
            query = _urlencode(query)
        elif type(query) is list:
            query = ', '.join(query)


        path = '/'.join((self.BASE_URL, service, self.mode, endpoint))

        #return a standard query string unless we're using the getPrediction service
        #because for some reason it is the only endpoint that does this
        return '?'.join((path, query)) if endpoint != 'GetPrediction' else '/'.join((path, query)) #full url query


    def _fetch(self, service, endpoint, query=None):
        url = self._construct_url(service, endpoint, query)
        req = _Request(url, headers={'api_key': self.api_key})
        print(req.full_url)
        with _urlopen(req) as r:
            response = str(r.read(), encoding='utf-8')

        return self._decode(response)

    #bus info methods
    def get_bus_position(self, route_id=None, lat=None, lon=None, radius=None ):
        return self._fetch('Bus', 'BusPositions', {'RouteID': route_id,
                                                   'Lat': lat,
                                                   'Lon': lon,
                                                   'Radius': radius})['BusPositions']

    def get_bus_path_details(self, route_id, date=None):
        return self._fetch('Bus', 'RouteDetails', {'RouteID': route_id,
                                                   'Date': date})

    def get_bus_routes(self):
        return self._fetch('Bus', 'Routes')

    def get_bus_route_schedule(self, route_id, date=None, variations=None):
        return self._fetch('Bus', 'RouteSchedule', {'RouteID': route_id,
                                                    'Date': date,
                                                    'IncludingVariations': variations})

    def get_bus_stop_schedule(self, stop_id, date=None):
        return self._fetch('Bus', 'StopSchedule', {'StopID': stop_id,
                                                   'Date': date})['ScheduleArrivals']

    def get_bus_stops(self, lat=None, lon=None, radius=None):
        return self._fetch('Bus', 'Stops', {'Lat': lat,
                                            'Lon': lon,
                                            'Radius': radius})['Stops']

    #incidents service
    def get_bus_incidents(self, route_id=None):
        return self._fetch('Incidents', 'BusIncidents', {'Route': route_id})['BusIncidents']

    def get_elevator_escelator_outages(self, station_id):
        return self._fetch('Incidents', 'ElevatorIncidents', {'StationCode': station_id})['ElevatorIncidents']

    def get_rail_incidents(self):
        return self._fetch('Incidents', 'Incidents')

    #rail station info service
    def get_rail_lines(self):
        return self._fetch('Rail', 'Lines')['Lines']

    def get_rail_parking_info(self, station_id):
        return self._fetch('Rail', 'StationParking', {'StationCode': station_id})['StationsParking']

    def get_rail_path_between(self, from_id, to_id):
        return self._fetch('Rail', 'Path', {'FromStationCode': from_id,
                                            'ToStationCode': to_id})['Path']

    def get_rail_station_entrances(self, lat=None, lon=None, radius=None):
        return self._fetch('Rail', 'StationEntrances', {'Lat': lat,
                                                        'Lon': lon,
                                                        'Radius': radius})['Entrances']

    def get_rail_station_information(self, station_id):
        return self._fetch('Rail', 'StationInfo', {'StationCode': station_id})

    def get_rail_line(self, line_id):
        return self._fetch('Rail', 'Stations', {'LineCode': line_id})['Stations']

    def get_rail_station_timings(self, station_id):
        return self._fetch('Rail', 'StationTimes', {'StationCode': station_id})['StationTimes']

    def get_rail_station_to_station(self, from_id, to_id):
        return self._fetch('Rails', 'SrcStationToDstStationInfo', {'FromStationCode': from_id,
                                                                   'ToStationCode': to_id})['StationToStationInfos']


    #rail prediction service
    def get_rail_prediction(self, station_codes):
        return self._fetch('StationPrediction', 'GetPrediction', station_codes)['Trains']

    #bus prediction service
    def get_bus_prediction(self, bus_codes):
        return self._fetch('NextBusService', 'Predictions', {'StopID': bus_codes})['Predictions']


