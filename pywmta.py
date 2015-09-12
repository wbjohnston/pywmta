"""
@author: Will Johnston <wbjohnston@gmail.com>
@date: September 8th, 2015

"""

import json as _json
from xml.parsers import expat as _xml
from urllib.request import Request as _Request
from urllib.request import urlopen as _urlopen
from urllib.parse import urlencode as _urlencode


class WMTA(object):
    #all requests go through this url in some way
    BASE_URL = 'https://api.wmata.com'

    def __init__(self, api_key, mode='json'):
        """
        constructor.
        :param api_key: your api key, given at api website
        :param mode: mode to encode
        """
        if mode not in self.get_valid_modes():
            raise ValueError('invalid encoding mode: {}'.format(self.mode))
        self.mode = mode
        self.api_key = api_key


    def get_valid_modes(self):
        """
        valid encoding modes for the api
        :return: tuple containing valid modes
        """
        return 'xml', 'json'

    def get_valid_services(self):
        """
        services that are provided by the api
        :return: tuple containing all services
        """
        return ('Bus',
                'Incidents',
                'Rail',
                'NextBusService',
                'StationPrediction')

    def get_valid_endpoints(self):
        """
        functions that are supported by the api
        :return: tuple containing all functions of this api
        """
        return ()

    def _decode(self, st):
        """
        decode the response string into a datastructure
        into either xml or json
        :param st: string to decode
        :return: data structure containing response
        """
        if self.mode == 'json':
            return _json.loads(st)
        elif self.mode == 'xml':
            return _xml.ParserCreate(encoding='utf-8').Parse(st)
        else:
            raise ValueError('invalid encoding mode: {}'.format(self.mode))


    def _construct_url(self, service, endpoint, query):
        """
        construct a full api call url
        :param service: service to use
        :param endpoint: function to use
        :param query: query data to send
        :return: the url for the service and function desired
        """
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
        """
        get data from the wmta
        :param service: service to use
        :param endpoint: function to use
        :param query: query data to send(usually a dict)
        :return: a data structure containing response(either encoded in xml or json)
        """
        url = self._construct_url(service, endpoint, query)
        req = _Request(url, headers={'api_key': self.api_key})
        with _urlopen(req) as r:
            response = str(r.read(), encoding='utf-8')

        return self._decode(response)

    #bus info methods
    def get_bus_position(self, route_id=None, lat=None, lon=None, radius=None ):
        """
         Returns bus positions for the given route, with an optional search radius.
         If no parameters are specified, all bus positions are returned.
        :param route_id: id of route
        :param lat: latitude to check
        :param lon: longitude to check
        :param radius: radius to check, centering at lat, lon
        :return: the buses in search area
        """
        return self._fetch('Bus', 'BusPositions', {'RouteID': route_id,
                                                   'Lat': lat,
                                                   'Lon': lon,
                                                   'Radius': radius})['BusPositions']

    def get_bus_path_details(self, route_id, date=None):
        """
        For a given date, returns the set of ordered latitude/longitude points along
        a route variant along with the list of stops served.
        :param route_id: id of route to check
        :param date: date of stop information to check
        :return: stop information
        """
        return self._fetch('Bus', 'RouteDetails', {'RouteID': route_id,
                                                   'Date': date})

    def get_bus_routes(self):
        """
        get all bus routes
        :return: all bus routes
        """
        return self._fetch('Bus', 'Routes')

    def get_bus_route_schedule(self, route_id, date=None, variations=None):
        """
        get a route schedule
        :param route_id: id of route to check
        :param date: date to check schedule for
        :param variations: For a given date, returns the set of ordered latitude/longitude
        points along a route variant along with the list of stops served.
        :return: route schedule
        """
        return self._fetch('Bus', 'RouteSchedule', {'RouteID': route_id,
                                                    'Date': date,
                                                    'IncludingVariations': variations})

    def get_bus_stop_schedule(self, stop_id, date=None):
        """
        Returns a set of buses scheduled at a stop for a given date.
        :param stop_id: 7-digit regional stop ID.
        :param date: Date in YYYY-MM-DD format for which to retrieve schedule.
         Defaults to today's date unless specified.
        :return: stop schedule
        """
        return self._fetch('Bus', 'StopSchedule', {'StopID': stop_id,
                                                   'Date': date})['ScheduleArrivals']

    def get_bus_stops(self, lat=None, lon=None, radius=None):
        """
        get bus stops in a search area
        :param lat: latitude
        :param lon: longitude
        :param radius: search radius
        :return: bus stops in search area
        """
        return self._fetch('Bus', 'Stops', {'Lat': lat,
                                            'Lon': lon,
                                            'Radius': radius})['Stops']

    #incidents service
    def get_bus_incidents(self, route_id=None):
        """
        Returns a set of reported bus incidents/delays for a given Route.
        :param route_id: id of route
        :return: incidents on route, or all incidents
        """
        return self._fetch('Incidents', 'BusIncidents', {'Route': route_id})['BusIncidents']

    def get_elevator_escalator_outages(self, station_id):
        """
        Returns a list of reported elevator and escalator outages at a given station
        :param station_id: id of station
        :return: incidents at station
        """
        return self._fetch('Incidents', 'ElevatorIncidents', {'StationCode': station_id})['ElevatorIncidents']

    def get_rail_incidents(self):
        """
        get all incidents pertaining to the trains
        :return: all incidents
        """
        return self._fetch('Incidents', 'Incidents')

    #rail station info service
    def get_rail_lines(self):
        """
        Returns information about all rail lines.
        :return: info about all rail lines
        """
        return self._fetch('Rail', 'Lines')['Lines']

    def get_rail_parking_info(self, station_id):
        """
        get parking info at a station
        :param station_id: id of station to check
        :return: parking info
        """
        return self._fetch('Rail', 'StationParking', {'StationCode': station_id})['StationsParking']

    def get_rail_path_between(self, from_id, to_id):
        """
        Returns a set of ordered stations and distances between two stations on the same line.
        :param from_id: station to start route check at
        :param to_id: station to end route check at
        :return: path between two stations
        """
        return self._fetch('Rail', 'Path', {'FromStationCode': from_id,
                                            'ToStationCode': to_id})['Path']

    def get_rail_station_entrances(self, lat=None, lon=None, radius=None):
        """
        get info about station entrances
        :param lat: latitude
        :param lon: longitude
        :param radius: search radius
        :return: stations found in search area
        """
        return self._fetch('Rail', 'StationEntrances', {'Lat': lat,
                                                        'Lon': lon,
                                                        'Radius': radius})['Entrances']

    def get_rail_station_information(self, station_id):
        """
        get station information
        :param station_id: id of station
        :return: information about selected station
        """
        return self._fetch('Rail', 'StationInfo', {'StationCode': station_id})

    def get_rail_line(self, line_id):
        """
        get all stations on a line
        :param line_id: line to check
        :return: stations on line
        """
        return self._fetch('Rail', 'Stations', {'LineCode': line_id})['Stations']

    def get_rail_station_timings(self, station_id):
        """
        get info about opening, closing, first train, and last train
        :param station_id: id of station to check
        :return: info about opening, closing, first train, and last train
        """
        return self._fetch('Rail', 'StationTimes', {'StationCode': station_id})['StationTimes']

    def get_rail_station_to_station(self, from_id, to_id):
        """
        Returns a distance, fare information, and estimated travel time between any two stations,
        including those on different lines. Omit both parameters to retrieve data for all stations
        :param from_id: station code of origin station
        :param to_id: station code of desintation station
        :return: information about path between stations
        """
        return self._fetch('Rails', 'SrcStationToDstStationInfo', {'FromStationCode': from_id,
                                                                   'ToStationCode': to_id})['StationToStationInfos']

    #rail prediction service
    def get_rail_prediction(self, station_codes):
        """
        get predictions about when a train will arrive
        :param station_codes: stations to get predictions for
        :return: predictions
        """
        return self._fetch('StationPrediction', 'GetPrediction', station_codes)['Trains']

    #bus prediction service
    def get_bus_prediction(self, stop_codes):
        """
        get predictions about when a bus will arrive
        :param stop_codes: stops to check
        :return: predictions
        """
        return self._fetch('NextBusService', 'Predictions', {'StopID': stop_codes})['Predictions']
