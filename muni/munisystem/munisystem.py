"""MUNISystem class definition. The module that is visable to
django's views.py"""
from APIHandler.handler import NextBusHandler
from DBHandler.handler import DBHandler

class MUNISystem:
    """The 'root' object, responsible to act as an facade/interface to the
     inner workings of the system."""

    @classmethod
    def updateRouteConfigs(cls):
        """Update database records with fresh routeConfig call to API"""
        # Get new RouteConfig
        routeConfig = NextBusHandler.getRouteConfig()
        # Update database
        DBHandler.routeConfigToDB(routeConfig)

    @classmethod
    def getRouteConfig(cls):
        """Returns all Route configuration data from database"""
        return DBHandler.getRouteConfig()

    @classmethod
    def getRouteList(cls):
        """Returns list of all Routes from database"""
        return DBHandler.getRouteList()

    @classmethod
    def getDirectionsByRoute(cls, routeTag):
        """Returns list of Directions matching a given Route from database"""
        return DBHandler.getDirectionsByRoute(routeTag)

    @classmethod
    def getStopsByDirection(cls, directionTag):
        """Returns list of Stops matching a given Direction from database"""
        return DBHandler.getStopsByDirection(directionTag)

    @classmethod
    def isAPIOnline(cls):
        """Returns whether or not the API is available"""
        return NextBusHandler.isOnline()

    @classmethod

    def getPredictions(cls, routeTag, stopTag, updateDB=False):
        """Returns prediction Response from API. If updateDB is set to True,
        the database will be updated with all vehicle id's associated with the
        predictions."""
        # Get prediction Response from API
        predictions = NextBusHandler.getPredictions(routeTag, stopTag)
        # if updateDB is True, add/update Vehicle records
        if updateDB == True:
            vehicles = predictions.getVehicles()
            DBHandler.vehiclesToDB(routeTag, vehicles)
        # Return prediction Response
        return predictions

    @classmethod
    def getVehicles_DB(cls):
        """Returns list of all Vehicle's from Database"""
        return DBHandler.getVehicles()

    @classmethod
    def getVehicleById_DB(cls, vehicleId):
        """Returns Vehicle record, matching a given id, from Database"""
        return DBHandler.getVehicleById(vehicleId)

    @classmethod
    def addRouteComment(cls, routeTag, text):
        """Adds Route Comment to database. Returns updated list of comments"""
        # Add comment to Database
        DBHandler.addRouteComment(routeTag, text)
        # Return list of updated comments
        return DBHandler.getRouteComments(routeTag)

    @classmethod
    def getRouteComments(cls, routeTag):
        """Returns list of all comments for given Route"""
        return DBHandler.getRouteComments(routeTag)

    @classmethod
    def addVehicleComment(cls, vehicleId, text):
        """Adds Vehicle Comment to database. Returns updated list of
        comments"""
        # Add comment to Database
        DBHandler.addVehicleComment(vehicleId, text)
        # Return list of updated comments
        return DBHandler.getVehicleComments(vehicleId)

    @classmethod
    def getVehicleComments(cls, vehicleId):
        """Returns list of all comments for given Vehicle"""
        return DBHandler.getVehicleComments(vehicleId)

    def deleteVehicleComments(cls, vehicleId):
        """Delete all comments, for a specified vehicle (id), from database"""
        # Pass to DBHandler
        DBHandler.deleteVehicleComments(vehicleId)
