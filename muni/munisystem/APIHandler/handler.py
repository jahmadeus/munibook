from xml.etree.ElementTree import parse
import urllib

from . import prediction
from muni.munisystem import routeconfig

# Some settings used for accessing API
AGENCY = "sf-muni"
BASE_URL = ("http://webservices.nextbus.com/service/publicXMLFeed?command=")

def getCommandURL(command, route=None, stop=None, options=None):
    """Utility function for generating API command URL"""

    commandURL = BASE_URL + command + "&a=" + AGENCY
    # If route is provided, add to url
    if route is not None:
        commandURL += "&r=" + route
    # If stop is provided, add to url
    if stop is not None:
        commandURL += "&s=" + stop
    # If options is provided, add to url
    if options is not None:
        commandURL += options

    # Returned formatted command URL
    return commandURL

class NextBusHandler:
    """Handler Object responsible for interfacing with the NextBus API"""

    @classmethod
    def getRouteConfig(cls):
        """Returns a RouteConfig object containing all system Routes including
        contained Direction's and Stop's"""

        # Retrieve XML data from the API
        u = urllib.urlopen(getCommandURL("routeConfig", options="&terse"))
        # Parse XML data
        data = parse(u)

        routes = []
        # Step through each route in data
        for currentRoute in data.findall('route'):
            # Keep track of route attributes until Route() creation
            routeTag = currentRoute.attrib['tag']
            routeTitle = currentRoute.attrib['title']
            color = currentRoute.attrib['color']
            oppositeColor = currentRoute.attrib['oppositeColor']

            stops = []
            # Step through each stop of current route
            for stop in currentRoute.findall('stop'):
                # Keep track of stop attributes until Stop() creation
                stopTag = stop.attrib['tag']
                stopTitle = stop.attrib['title']
                lat = stop.attrib['lat']
                lon = stop.attrib['lon']
                stopId = stop.attrib['stopId']
                # Create Stop with attributes
                routeConfigStop = routeconfig.Stop(stopTag, stopTitle, lat,
                                                   lon, stopId)
                # Append to list of route stops
                stops.append(routeConfigStop)

            directions = []
            # Step through each direction of current route
            for direction in currentRoute.findall('direction'):
                # Keep track of Direction attributes until Direction creation
                dirTag = direction.attrib['tag']
                dirTitle = direction.attrib['title']
                dirName = direction.attrib['name']

                stopTags = []
                # For each stop listing in current direction
                for stop in direction.findall('stop'):
                    # Append stop tag to list
                    stopTags.append(stop.attrib['tag'])

                directionStops = []
                # Step through all stops in route stop list
                for s in stops:
                    # If that stops tag matches directions stop tags
                    if s.tag in stopTags:
                        # Append to list
                        directionStops.append(s)

                # Create Direction with attributes and
                # list of contained Stops
                routeConfigDirection = routeconfig.Direction(dirTag, dirTitle,
                                        dirName, directionStops)
                # Append to list of Direction's
                directions.append(routeConfigDirection)

            # Create Route with attributes and list of contained Directions
            routeConfigRoute = routeconfig.Route(routeTag, routeTitle,
                                color, oppositeColor, directions)
            # Append to list of Route's
            routes.append(routeConfigRoute)

        # Once all contained records are collected, create RouteConfig
        routeConfig = routeconfig.RouteConfig(routes)

        # Return RouteConfig
        return routeConfig

    @classmethod
    def getPredictions(cls, route, stopId):
        """Returns a Response object containing all prediction and message
        data for a given Route and Stop"""
        # Retrieve XML data from the API
        u = urllib.urlopen(getCommandURL("predictions", route, stopId))
        # Parse XML data
        data = parse(u)

        # For each predictions package in data
        for predictionPackage in data.findall('predictions'):
            # Keep track of attributes until Response() creation
            routeTitle = predictionPackage.attrib['routeTitle']
            stopTitle = predictionPackage.attrib['stopTitle']
            # Each set of predictions is grouped by direction if needed
            # Collect all direction group and their containing predictions
            predictionDirections = []

            # For each direction in data
            for direction in predictionPackage.findall('direction'):
                # Keep track of attributes until Direction() creation
                directionTitle = direction.attrib['title']

                predictions = []
                # For each prediction in current direction
                for predictionData in direction.findall('prediction'):
                    # Keep track of attribute until Prediction() creation
                    epochTime = predictionData.attrib['epochTime']
                    seconds = predictionData.attrib['seconds']
                    minutes = predictionData.attrib['minutes']
                    isDeparture = predictionData.attrib['isDeparture']
                    dirTag = predictionData.attrib['dirTag']
                    vehicleId = predictionData.attrib['vehicle']
                    # Because this attribute is only present when 'True',
                    # check to see if it exists first.
                    try:
                        affectedByLayover = predictionData.attrib[
                                                    'affectedByLayover']
                    except KeyError:
                        affectedByLayover = 'false'
                    # Create Prediction with collected attributes
                    predict = prediction.Prediction(epochTime, seconds,
                                                    minutes, isDeparture,
                                                    dirTag, vehicleId,
                                                    affectedByLayover)
                    # Append to list of Predictions
                    predictions.append(predict)
                # Create Direction with attributes and list of Prediction's
                routeDirection = prediction.Direction(directionTitle,
                                                      predictions)
                # Append to list of Direction's
                predictionDirections.append(routeDirection)

            # Collect all system messages
            messages = []
            # For message in data
            for messageData in predictionPackage.findall('message'):
                # Keep track of attributes until Message() creation
                text = messageData.attrib['text']
                priority = messageData.attrib['priority']
                # Create Message with collected attributes
                message = prediction.Message(text, priority)
                # Append to list of Message's
                messages.append(message)

        # Once all contained records are collected, create Response
        predictionResponse = prediction.Response(routeTitle, stopTitle,
                                                 predictionDirections,
                                                 messages)
        # return Response
        return predictionResponse

    @classmethod
    def isOnline(cls):
        """Returns the availability of the API service. Sends a small request
        to the API and catches all errors."""

        try:
            # routeList is used as it requires no arguments and requests a
            # minimal amount of data from the API
            u = urllib.urlopen(getCommandURL("routeList"))
        except:
            return False

        return True
