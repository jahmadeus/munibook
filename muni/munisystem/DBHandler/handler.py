"""DBHandler class definition. Used by munisystem to interface with
the database"""
from muni.models import (Route, Stop, Direction, Vehicle, Comment,
    RouteComment, VehicleComment)
from muni.munisystem import routeconfig

class DBHandler:
    """Handler Object responsible for interfacing with the database
     (using django's models component)"""
    @classmethod
    def routeConfigToDB(cls, routeConfig):
        # For each route in RouteConfig
        for route in routeConfig.routes:
            # Create Route record with current route attributes

            routeRecord, created = Route.objects.update_or_create(
                                        tag=route.tag,
                                        defaults={
                                        'name': route.title,
                                        'color': route.color,
                                        'oppositeColor': route.oppositeColor})
            if created:
                # Save to database
                routeRecord.save()

            # For each direction contained in current route
            for direction in route.directions:
                # Create Direction record with current direction attributes
                directionRecord, dir_created = Direction.objects.update_or_create(
                                            tag=direction.tag,
                                            defaults={'name': direction.title,
                                            'direction': direction.direction})
                if dir_created:
                    # Add to the created Route records direction set
                    routeRecord.direction_set.add(directionRecord)

                # For each stop contained in current direction
                for stop in direction.stops:


                    # Create Stop record with current direction attributes
                    stopRecord, created = Stop.objects.update_or_create(
                                      tag=stop.tag, defaults={
                                            'name': stop.title,
                                            'lat': stop.lat,
                                            'lon': stop.lon,
                                            'stopId': stop.stopId})

                    if dir_created:
                        # Associate Stop record with Direction record
                        directionRecord.stops.add(stopRecord)
    @classmethod
    def getRouteConfig(cls):
        """Returns a RouteConfig object containing all system Routes including
        contained Direction's and Stop's"""
        routes = []
        # For each Route record in database
        for route in Route.objects.all():
            directions = []
            # For each Direction record in database
            for direction in route.direction_set.all():
                stops = []
                # For each Stop record in database
                for stop in direction.stops.all():
                    # Create Stop object from current Stop Record,
                    # then append to list
                    stops.append(routeconfig.Stop(stop.tag, stop.name, stop.lat, stop.lon, stop.stopId))

                # Create Direction object from current Direction Record and
                # list of Stops, then append to list
                directions.append(routeconfig.Direction(direction.tag, direction.name, direction.direction, stops))
            # Create Route object from current Route Record and list
            # of Directions, then append to list
            routes.append(routeconfig.Route(route.tag, route.name, route.color, route.oppositeColor, directions))

        # Once all data is retrieved from database, return RouteConfig
        return routeconfig.RouteConfig(routes)

    @classmethod
    def getRouteList(cls):
        """Returns list of all routes from database"""
        routes = []
        for route in Route.objects.all():
            routes.append((route.tag, route.name))
        return routes

    @classmethod
    def getDirectionsByRoute(cls, routeTag):
        """Returns list of all routes from database"""
        directions = []
        # Get Route record that matches route tag
        route = Route.objects.get(tag=routeTag)
        # For each Direction record in current Route record
        for direction in route.direction_set.all():
            # Append to list
            directions.append(direction)
        # Return list of directions
        return directions

    @classmethod
    def getStopsByDirection(cls, directionTag):
        """Returns list of Stops matching a given Direction from database"""
        stops = []
        # Get Direction record that matches direction tag
        direction = Direction.objects.get(tag=directionTag)
        # For each Stop record in current Direction record
        for stop in direction.stops.all():
            # Append to list
            stops.append(stop)
        # Return list of directions
        return stops

    @classmethod
    def vehiclesToDB(cls, routeTag, vehicles):
        """Updates database with a list of Vehicles"""
        # Get Route record that matches route tag
        route = Route.objects.get(tag=routeTag)
        # For each Vehicle in Vehicle list
        for vehicle in vehicles:
            # If already exists, update associated Route, else, create record
            v, created = Vehicle.objects.update_or_create(vehicleId=vehicle)
            if created:
                # If record was created, add associate to Route record
                route.vehicle_set.add(v)

    @classmethod
    def getVehicles(cls):
        """Returns list of all Vehicle's from Database"""
        vehicles = []
        # For each Vehicle record in database
        for vehicle in Vehicle.objects.all():
            # Append to list
            vehicles.append(vehicle)
        # Return list of all vehicle records
        return vehicles

    @classmethod
    def getVehicleById(cls, vehicleId):
        """Returns Vehicle record, matching a given id, from Database"""
        # Get Vehicle record matching the given vehicle id
        vehicle = Vehicle.objects.get(vehicleId=vehicleId)
        return vehicle

    @classmethod
    def addRouteComment(cls, routeTag, text):
        """Adds Route Comment to database. Returns updated list of comments"""
        # Get Route record that matches route tag
        route = Route.objects.get(tag=routeTag)
        comment = RouteComment(text=text)
        route.routecomment_set.add(comment)

    @classmethod
    def getRouteComments(cls, routeTag):
        """Returns list of all comments for given Route"""
        # Get Route record that matches route tag
        route = Route.objects.get(tag=routeTag)
        # Get updated Vehicle Comments
        routeComments = route.routecomment_set.all()
        return routeComments

    @classmethod
    def addVehicleComment(cls, vehicleId, text):
        """Adds Vehicle Comment to database. Returns updated list of
        comments"""
        # Get Vehicle record that matches vehicle id
        vehicle = Vehicle.objects.get(vehicleId=vehicleId)
        # Create Vehicle Comment
        comment = VehicleComment(text=text)
        # Save to database
        vehicle.vehiclecomment_set.add(comment)

    @classmethod
    def getVehicleComments(cls, vehicleId):
        """Returns list of all comments for given Vehicle"""
        # Get Vehicle record that matches vehicle id
        vehicle = Vehicle.objects.get(vehicleId=vehicleId)
        # Get updated Vehicle Comments
        vehicleComments = vehicle.vehiclecomment_set.all()
        return vehicleComments

    @classmethod
    def deleteVehicleComments(cls, vehicleId):
        """Delete all comments for a specified vehicle (id)"""
        # Get vehicle record that matches vehicle id
        vehicle = Vehicle.objects.get(vehicleId=vehicleId)
        # Get all associated comments
        vehicleComments = vehicle.vehiclecomment_set.all()
        # Delete associated comments
        vehicleComments.delete()
