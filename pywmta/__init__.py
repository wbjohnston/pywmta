uthor__ = 'Bonk'

import json
import requests

DEFAULT_TIMEOUT = 10
API_BASE_URL = 'https://api.wmata.com/{service}/json/{endpoint}'

class WMTAException(Exception):
    pass

class Response:
    def __init__(self, body):
        self.raw = body
        self.body = json.loads(body)
        self.successful = ''
        self.error = ''


class BaseAPI:
    def __init__(self, api_key=None, timeout=DEFAULT_TIMEOUT):
        self.api_key = api_key
        self.timeout = timeout

    def _request(self, method, service, endpoint, **kwargs):
        if self.api_key:
            kwargs.setdefault('params', {})['api_key'] = self.api_key

        response = method(API_BASE_URL.format(service=service,
                                              endpoint=endpoint),
                          timeout=self.timeout,
                          headers={'api_key': self.api_key},
                          **kwargs)

        response.raise_for_status()

        response = Response(response.text)
        if not response.successful:
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
    def bus_position(self, route_id=None, lat=None, lon=None, radius=None):
        data = {
            'RouteID': route_id,
            'Lat': lat,
            'Lon': lon,
            'Radius': radius
        }
        return self.post('Bus.svc', 'jBusPositions', data=data)

    def path_details(self, route_id, date=None):
        data = {
            'RouteID': route_id,
            'Data': date
        }
        return self.post('Bus.svc', 'jRouteDetails', data=data)

    def routes(self):
        return self.get('Bus.svc', 'jRoutes')

    def schedule(self, route_id, date=None, incl_variations=None):
        data = {
            'RouteID': route_id,
            'Date': date,
            'IncludingVariations': incl_variations
        }
        return self.post('Bus.svc', 'jRouteSchedule', data=data)

    def schedule_at_stop(self, stop_id, date=None):
        data = {
            'StopID': stop_id,
            'Date': date
        }
        return self.post('Bus.svc', 'jStopSchedule', data=data)

    def stop_search(self, lat=None, lon=None, radius=None):
        data = {
            'Lat': lat,
            'Lon': lon,
            'Radius': radius
        }
        return self.post('Bus.svc', 'jStops', data=data)

class Incidents(BaseAPI):
    def bus(self, route=None):
        data = {
            'Route': route
        }
        return self.post('Incidents.svc', 'BusIncidents', data=data)

    def elevator_escelator(self, station_code=None):
        data = {
            'StationCode': station_code
        }
        return self.post('Incidents.svc', 'ElevatorIncidents', data=data)

    def rail(self):
        return self.post('Incidents.svc', 'Incidents')

class RailStation(BaseAPI):
    def lines(self):
        return self.get('Rail.svc', 'jLines')

    def parking(self, station_code=None):
        data = {
            'StationCode': station_code
        }
        return self.post('Rail.svc', 'jStationParking', data=data)

    def path_between(self, from_station_code, to_station_code):
        data = {
            'FromStationCode': from_station_code,
            'ToStationCode': to_station_code
        }
        return self.post('Rail.svc', 'jPath', data=data)

    def entrances(self, lat=None, lon=None, radius=None):
        data = {
            'Lat': lat,
            'Lon': lon,
            'Radius': radius
        }
        return self.post('Rail.svc', 'jStationEntrances', data=data)

    def information(self, station_code):
        data = {
            'StationCode': station_code
        }
        return self.post('Rail.svc', 'jStationInfo', data=data)

    def list(self, line_code):
        data = {
            'LineCode': line_code
        }
        return self.post('Rail.svc', 'jStations', data=data)

    def timings(self, station_code):
        data = {
            'StationCode': station_code
        }
        return self.post('Rail.svc', 'jStationTimes', data=data)

    def station_to_station(self, from_station_code=None, to_station_code=None):
        data = {
            'FromStationCode': from_station_code,
            'ToStationCode': to_station_code
        }
        return self.post('Rail.svc', 'jSrcStationToDstStationInfo', data=data)

class RailPrediction(BaseAPI):
    def next_trains(self, station_codes):
        data = {
            'StationCodes': station_codes
        }
        return self.get('StationPrediction.svc', 'GetPrediction', params=data)

class BusPrediction(BaseAPI):
    def next_buses(self, stop_id):
        data = {
            'StopID': stop_id
        }
        return self.post('NextBusService.svc', 'jPredictions', data=data)


class WMTAApi:
    def __init__(self, api_key, timeout=DEFAULT_TIMEOUT):
        #TODO: add all submodules into this
        self.bus_route = Busroute(api_key=api_key, timeout=timeout)
        self.incidents = Incidents(api_key=api_key, timeout=timeout)
        self.rail_station = RailStation(api_key=api_key, timeout=timeout)
        self.rail_prediction = RailPrediction(api_key=api_key, timeout=timeout)
        self.bus_prediction = BusPrediction(api_key=api_key, timeout=timeout)
