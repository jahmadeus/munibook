"""Contains all persistant data model definitions. Interfaces with
DBHandler"""
from django.db import models

class Comment(models.Model):
    """Generic comment data model"""
    # add timestamp to record on creation
    datePosted = models.DateField(auto_now_add=True)
    text = models.CharField(max_length=140)

class Stop(models.Model):
    """Stop data model"""
    name = models.CharField(max_length=50)
    tag = models.CharField(max_length=6, unique=True)
    lat = models.CharField(max_length=50)
    lon = models.CharField(max_length=50)
    stopId = models.CharField(max_length=7)

    def __str__(self):
        return self.name

class StopComment(Comment):
    """StopComment data model. Inherits from parent class Comment"""
    stop = models.ForeignKey(Stop)

class Route(models.Model):
    """Route data model"""
    name = models.CharField(max_length=50)
    tag = models.CharField(max_length=10, unique=True)
    color = models.CharField(max_length=6)
    oppositeColor = models.CharField(max_length=6)

    def __str__(self):
        return self.name

    def __iter__(self):
        for i in (self.name, self.tag, self.color, self.oppositeColor):
            yield str(i)

class RouteComment(Comment):
    """RouteComment data model. Inherits from parent class Comment"""
    route = models.ForeignKey(Route)

    def __str__(self):
        return "%s Comment (%s)" % (str(self.route), str(self.datePosted))


class Direction(models.Model):
    """Direction data model"""
    name = models.CharField(max_length=50)
    tag = models.CharField(max_length=15, unique=True)
    direction = models.CharField(max_length=10)
    # Directions contain many Stops. Stops are members of many 'directions'
    stops = models.ManyToManyField(Stop)
    # A direction can only be part of one route
    route = models.ForeignKey(Route, null=True)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    """Vehicle data model"""
    vehicleId = models.CharField(max_length=6, unique=True)
    lastRoute = models.ForeignKey(Route, null=True)

    def __str__(self):
        return "Vehicle #" + self.vehicleId

class VehicleComment(Comment):
    vehicle = models.ForeignKey(Vehicle)

    def __str__(self):
        return "%s Comment (%s)" % (str(self.vehicle), str(self.datePosted))
