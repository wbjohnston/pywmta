# WMTA This is documentation of all the *fun* parts of the washington DC Metro Transit Authority API. There is documentation available online but it doesn't directly state all the *idiosyncrasies*

**note: This api has both an XML and JSON mode**

# Service Overview
###### Bus Route and Stop Methods
Bus stop information, route and schedule data, and bus positions.
###### Incidents
Rail, bus, and elevator disruptions/outages.
###### Rail Station Information
Rail line and station information, including locations, fares, times, and parking.
###### Real-Time Bus Predictions
Real-time bus prediction methods.
###### Real-Time Rail Predictions
Real-time rail prediction methods.

--------

### Bus Route and Stop Methods
###### Bus Position
pass in: dict
endpoint: jBusPositions
###### Path Details
pass in: dict
endpoint: jRouteDetails
###### Routes
pass in: none
endpoint: jRoutes
###### Schedule
pass in: dict
endpoint: jRouteSchedule
###### Schedule at stop
pass in: dict
endpoint: jStopSchedule
###### Stop Search
pass in: none
endpoint: jStops

--------

### Incidents
###### Bus Incidents
pass in: none
endpoint: BusIncidents
###### Elevator/Escalator Outages
pass in: none
endpoint: ElevatorIncidents
###### Rail Incidents
pass in: none
endpoint: Incidents

--------

### Rail Station Information
###### Lines
pass in: none
endpoint: jLines
###### Parking Information
pass in: none
endpoint: jStationParking
###### Path Between Stations
pass in: dict
endpoint: jPath
###### Station Entrances
pas in: dict
endpoint: jStationEntrances
###### Station Information
pass in: dict
endpoint: jStationInfo
###### Station List
pass in: dict
endpoint: jStations
###### Station Timings
pass in: dict
endpoint: jStationTimes
###### Station to Station Information
pass in: dict
endpoint: jSrcStationToDstStationInfo

--------

### Real-Time Bus Predictions
###### Next Buses
pass in: dict
endpoint: jPredictions

--------

### Real-Time Rail Predictions
###### Next Trains
pass in: list
endpoint: GetPrediction
**Note: for some reason this is not a query string it's seperated by a slash uri/query**



