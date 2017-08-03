"""Contains RouteConfig class definition as well as the contained Stop,
Route and Direction class definitions"""

class RouteConfig:
    """Responsible for containing the configuration of Routes, Directions and
    Stops. Utilized by both the DBHandler and APIHandler to encapsulate API
    and database responses. Contains list corresponding Route objects."""
    def __init__(self, routes=None):
        if routes is None:
            self.routes = []
        else:
            self.routes = routes[:]

    def getRouteByTag(self, tag):
        """Returns Route object matching the given tag"""
        for route in self.routes:
            if route.tag == tag:
                return route

class Stop:
    """Represents a Stop record retreived from the API or database"""
    def __init__(self, tag, title, lat, lon, stopId):
        self.tag = tag
        self.title = title
        self.lat = lat
        self.lon = lon
        self.stopId = stopId

    def __iter__(self):
        for i in (self.tag, self.title, self.lat, self.lon, self.stopId):
            yield i

class Route:
    """Represents a Route record retreived from the API or database. Contains
     list corresponding Direction objects."""
    def __init__(self, tag, title, color, oppositeColor, directions=None):
        self.tag = tag
        self.title = title
        self.color = color
        self.oppositeColor = oppositeColor

        # If directions were not given, initialze empty list
        if directions is None:
            self.directions = []
        else:
            # Else, copy list to object attribute
            self.directions = directions[:]

    def __iter__(self):
        for i in (self.tag, self.title, self.color,
                  self.oppositeColor, self.directions):
            yield i

    def getRouteShortName(self):
        """Returns shortened route title.
        Example: 30-Stockton becomes Stockton"""
        return self.title.split("-", 1)[-1]

    def getInboundTitle(self):
        """Returns the title of contained 'inbound' direction"""
        for direction in self.directions:
            if not direction.direction == "Inbound":
                continue
            else:
                return direction.title

    def getOutboundTitle(self):
        """Returns the title of contained 'outbound' direction"""
        for direction in self.directions:
            if not direction.direction == "Outbound":
                continue
            else:
                return direction.title

    def getInboundStops(self):
        """Returns a list of stops contained in the 'inbound' direction."""
        inboundStops = []

        # Step through contained directions until Inbound reached
        for direction in self.directions:
            if not direction.direction == "Inbound":
                continue
            else:
                # Then step through contained stops and append to list
                for stop in direction.stops:
                    inboundStops.append(tuple(stop))
                # Return inbound stops
                return inboundStops

    def getOutboundStops(self):
        """Returns a list of stops contained in the 'outbound' direction."""
        outboundStops = []

        # Step through contained directions until Outbound reached
        for direction in self.directions:
            if not direction.direction == "Outbound":
                continue
            else:
                # Then step through contained stops and append to list
                for stop in direction.stops:
                    outboundStops.append(tuple(stop))
                # Return inbound stops
                return outboundStops


class Direction:
    """Represents a Direction record retreived from the API or database.
    Contains list corresponding Stop objects."""
    def __init__(self, tag, title, direction, stops=None):
        self.tag = tag
        self.title = title
        self.direction = direction
        # If directions were not given, initialze empty list
        if stops is None:
            self.stops = []
        else:
            # Else, copy given list to object attribute
            self.stops = stops[:]

    def __iter__(self):
        for i in (self.tag, self.title, self.name, self.stops):
            yield i
