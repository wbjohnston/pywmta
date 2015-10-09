__author__ = 'Will Johnston'

import json
import requests

DEFAULT_TIMEOUT = 10
API_BASE_URL = 'https://api.wmata.com/{service}/json/{endpoint}'

class WMTAException(Exception):
    pass

class BaseAPI:
    def __init__(self, api_key=None, timeout=DEFAULT_TIMEOUT):
        self.api_key = api_key
        self.timeout = timeout

    def _request(self, method, service, endpoint, **kwargs):
        if self.api_key:
            kwargs.setdefault('params', {})['api_key'] = self.api_key

        response = method(API_BASE_URL.format(service=service, endpoint=endpoint),
                                              timeout=self.timeout,
                                              headers={'api_key': self.api_key},
                                              **kwargs)

        response.json = json.loads(response.text)
        response.raise_for_status()

        if not response.ok:
            raise WMTAException(response.error)

        return response

    def get(self, service, endpoint, **kwargs):
        return self._request(requests.get,
                             service,
                             endpoint,
                             **kwargs)

    def post(self, service, endpoint, **kwargs):
        return self._request(requests.post,
                             service,
                             endpoint,
                             **kwargs)

class Busroute(BaseAPI):
    RESOURCE_NAME = 'Bus.svc'
    def bus_position(self, route_id=None, lat=None, lon=None, radius=None):
        data = {
            'RouteID': route_id,
            'Lat': lat,
            'Lon': lon,
            'Radius': radius
        }
        return self.get(self.RESOURCE_NAME, 'jBusPositions',
                        params=data).json['BusPositions']

    def path_details(self, route_id, date=None):
        data = {
            'RouteID': route_id,
            'Data': date
        }
        return self.get(self.RESOURCE_NAME, 'jRouteDetails', params=data).json

    def routes(self):
        return self.get(self.RESOURCE_NAME, 'jRoutes').json['Routes']

    def schedule(self, route_id, date=None, incl_variations=None):
        data = {
            'RouteID': route_id,
            'Date': date,
            'IncludingVariations': incl_variations
        }
        return self.get(self.RESOURCE_NAME, 'jRouteSchedule', params=data).json

    def schedule_at_stop(self, stop_id, date=None):
        data = {
            'StopID': stop_id,
            'Date': date
        }
        return self.get(self.RESOURCE_NAME, 'jStopSchedule', params=data).json

    def stop_search(self, lat=None, lon=None, radius=None):
        data = {
            'Lat': lat,
            'Lon': lon,
            'Radius': radius
        }
        return self.get(self.RESOURCE_NAME, 'jStops', params=data).json['Stops']

class Incidents(BaseAPI):
    RESOURCE_NAME = 'Incidents.svc'
    def bus(self, route=None):
        data = {
            'Route': route
        }
        return self.get(self.RESOURCE_NAME, 'BusIncidents', params=data).json['BusIncidents']

    def elevator_escalator(self, station_code=None):
        data = {
            'StationCode': station_code
        }
        return self.get(self.RESOURCE_NAME, 'ElevatorIncidents', params=data).json['ElevatorIncidents']

    def rail(self):
        return self.get(self.RESOURCE_NAME, 'Incidents').json['Incidents']

class RailStation(BaseAPI):
    RESOURCE_NAME = 'Rail.svc'
    def lines(self):
        return self.get(self.RESOURCE_NAME, 'jLines').json['Lines']

    def parking(self, station_code=None):
        data = {
            'StationCode': station_code
        }
        return self.get(self.RESOURCE_NAME, 'jStationParking', params=data).json

    def path_between(self, from_station_code, to_station_code):
        data = {
            'FromStationCode': from_station_code,
            'ToStationCode': to_station_code
        }
        return self.get(self.RESOURCE_NAME, 'jPath', params=data).json

    def entrances(self, lat=None, lon=None, radius=None):
        data = {
            'Lat': lat,
            'Lon': lon,
            'Radius': radius
        }
        return self.get(self.RESOURCE_NAME, 'jStationEntrances', params=data).json

    def information(self, station_code):
        data = {
            'StationCode': station_code
        }
        return self.get(self.RESOURCE_NAME, 'jStationInfo', params=data).json

    def list(self, line_code):
        data = {
            'LineCode': line_code
        }
        return self.get(self.RESOURCE_NAME, 'jStations', params=data).json['Stations']

    def timings(self, station_code):
        data = {
            'StationCode': station_code
        }
        return self.get(self.RESOURCE_NAME, 'jStationTimes', params=data).json['StationTimes']

    def station_to_station(self, from_station_code=None, to_station_code=None):
        data = {
            'FromStationCode': from_station_code,
            'ToStationCode': to_station_code
        }
        return self.get(self.RESOURCE_NAME, 'jSrcStationToDstStationInfo',
                        params=data).json['StationToStationInfos']

class RailPrediction(BaseAPI):
    RESOURCE_NAME = 'StationPrediction.svc'
    def next_trains(self, station_codes):
        data = {
            'StationCodes': station_codes
        }
        return self.get(self.RESOURCE_NAME, 'GetPrediction', params=data).json

class BusPrediction(BaseAPI):
    RESOURCE_NAME = 'BusPrediction.svc'
    def next_buses(self, stop_id):
        data = {
            'StopID': stop_id
        }
        return self.get(self.RESOURCE_NAME, 'jPredictions', params=data).json


class WMTAApi:
    def __init__(self, api_key, timeout=DEFAULT_TIMEOUT):
        #TODO: add all submodules into this
        self.bus_route = Busroute(api_key=api_key, timeout=timeout)
        self.incidents = Incidents(api_key=api_key, timeout=timeout)
        self.rail_station = RailStation(api_key=api_key, timeout=timeout)
        self.rail_prediction = RailPrediction(api_key=api_key, timeout=timeout)
        self.bus_prediction = BusPrediction(api_key=api_key, timeout=timeout)
