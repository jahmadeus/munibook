"""Below are the functions called by urls.py. They are used to render the main
HTML pages and handle ajax requests."""
import simplejson
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from . import models
from munisystem.munisystem import MUNISystem

def getRoutes(request):
    """Displays a list of available routes."""
    # Get route list from system
    routeList = MUNISystem.getRouteList()
    # Render route list to template
    return render(request, 'routes_nojs.html', {'route_list': routeList})

def getStops(request, route):
    """Displays a list of available stops, seperated by direction."""
    # Get RouteConfig from system
    routeConfigResponse = MUNISystem.getRouteConfig()

    # TO-DO: Eventually implement routeConfig as a dictionary similiar to how
    # prediction Responses are handled below in getpredictions()...

    # Render routeConfig data to template
    return render(request, 'stops_nojs.html',
    {'routeName': routeConfigResponse.getRouteByTag(route).getRouteShortName(),
    'routeTag': route,
    'inboundTitle': routeConfigResponse.getRouteByTag(route).getInboundTitle(),
    'inboundStops': routeConfigResponse.getRouteByTag(route).getInboundStops(),
    'outboundTitle':
    routeConfigResponse.getRouteByTag(route).getOutboundTitle(),
    'outboundStops':
    routeConfigResponse.getRouteByTag(route).getOutboundStops()})

def getPredictions(request, route, stop):
    """Displays prediction and message data for a given route and stop."""
    # Check if the API service is available
    if MUNISystem.isAPIOnline() == False:
        # If unavailable, render error to template
        return render(request, 'error.html', {'error_message':
        "The NextBus API cannot be reached at this time. Try again later."})
    else:
        # Else get a PredictionResponse (predictions + messages) from system
        predictionResponse = MUNISystem.getPredictions(route, stop)
        # Render to template
        return render(request, 'predictions_nojs.html',
                {'predictionData':
                        predictionResponse.getPredictionsTupleList(),
                 'routeTitle': predictionResponse.getRouteShortTitle(),
                 'routeTag': route,
                 'stopTitle': predictionResponse.stopTitle,
                 'messages': predictionResponse.getMessages()})

def index(request):
    """Displays main index page."""
    # Check if the API service is available
    if MUNISystem.isAPIOnline() == False:
        # If unavailable, render error to template
        return render(request, 'error.html', {'error_message':
        "The NextBus API cannot be reached at this time. Try again later."})
    else:
        # Get route list from system
        routeList = MUNISystem.getRouteList()
        # Render route list to template
        return render(request, 'index.html', {'route_list': routeList})

def getvehicle(request):
    """Displays vehicle information page. Receives id of vehicle via GET.
    (example ?id=3293)"""
    # Retreive id from GET request
    vehicleId = request.GET['id']
    # Get vehicle record from system
    vehicle = MUNISystem.getVehicleById_DB(vehicleId)
    return render(request, 'vehicle.html', {'vehicleId': vehicle.vehicleId,
     'lastRoute': vehicle.lastRoute.name})

def getdirections(request):
    """Takes a GET request as input. Returns a JSON response. Used for ajax
    calls to return directions for a particular route."""
    # Retrieve route tag from GET request
    routeTag = request.GET['rt']
    result_set = []

    # Get list of direction records for route
    directions = MUNISystem.getDirectionsByRoute(routeTag)

    # Step through the list of directions and add to result_set
    for direction in directions:
        result_set.append({'name': direction.name, 'tag': direction.tag})

    # return result_set as JSON
    return HttpResponse(simplejson.dumps(result_set),
                        content_type='application/json')

def getstops(request):
    """Takes a GET request as input. Returns a JSON response. Used for ajax
    calls to return directions for a particular route."""
    # Retrieve direction tag from GET request
    directionTag = request.GET['dir']
    result_set = []

    # Get list of stop records for direction
    stops = MUNISystem.getStopsByDirection(directionTag)

    # Step through the list of stops and add to result_set
    for stop in stops:
        result_set.append({'name': stop.name, 'tag': stop.tag})

    # return result_set as JSON
    return HttpResponse(simplejson.dumps(result_set),
                        content_type='application/json')

def getpredictions(request):
    """Takes a GET request as input. Returns a JSON response. Used for ajax
     calls to return directions for a particular route."""
    # Retreive route and stop tags from GET request
    routeTag = request.GET['route']
    stopTag = request.GET['stop']

    # Get PredictionResponse from system (updateDB flag  set to true)
    predictionResponse = MUNISystem.getPredictions(routeTag, stopTag, True)

    # Use PredictionResponse.getJSON() to serialize object
    predictionResponseJSON = predictionResponse.getJSON()

    # Return JSON
    return HttpResponse(predictionResponseJSON,
                        content_type='application/json')

def getvehicles(request):
    """Returns a JSON response. Used for ajax calls to return all vehicles
     records in system. Primarily used for debugging purposes."""
     # Get list of vehicle records from system
    vehicles = MUNISystem.getVehicles_DB()
    result_set = []

    # Step through list of records and append each record to result_set
    for vehicle in vehicles:
        result_set.append({
            'lastRoute': vehicle.lastRoute.name,
            'vehicleId': vehicle.vehicleId})

    # Return result_set as JSON
    return HttpResponse(simplejson.dumps(result_set),
                        content_type="application/json")

def addroutecomment(request):
    """Takes a GET request as input. Returns a JSON response. Used for adding
    route comments to system and returning updated comments list via ajax.
    Example: ?text=comment&route=30"""
    # Retreive route and comment from GET request
    commentText = request.GET['text']
    routeTag = request.GET['route']
    result_set = []

    # Add comment to system and return updated list of comments
    updatedComments = MUNISystem.addRouteComment(routeTag, commentText)

    # Step through each comment and append to result_set
    for comment in updatedComments:
        result_set.append({
            'datePosted': comment.datePosted.strftime("%Y-%m-%d"),
            'text': comment.text})

    # Return result_set as JSON
    return HttpResponse(simplejson.dumps(result_set),
                        content_type="application/json")

def getroutecomments(request):
    """Takes a GET request as input. Returns a JSON response. Used for adding
    route comments to system and returning updated comments list
    Example: ?route=30"""
    # Retreive route from GET request
    routeTag = request.GET['route']
    result_set = []

    # Get list of comments for route
    comments = MUNISystem.getRouteComments(routeTag)

    # Step through each comment and append to result_set
    for comment in comments:
        result_set.append({
        'datePosted': comment.datePosted.strftime("%Y-%m-%d"),
        'text': comment.text})

    # Return result_set as JSON
    return HttpResponse(simplejson.dumps(result_set),
                        content_type="application/json")

def addvehiclecomment(request):
    """Takes a GET request as input. Returns a JSON response. Used for adding
    vehicle comments to system and returning updated comments list via ajax.
    Example: ?text=comment&vehicleId=3023"""
    # Retreive vehicleId and comment from GET request
    commentText = request.GET['text']
    vehicleId = request.GET['vehicleId']

    result_set = []

    # Add comment to system and return updated list of comments
    updatedComments = MUNISystem.addVehicleComment(vehicleId, commentText)

    # Step through each comment and append to result_set
    for comment in updatedComments:
        result_set.append({
        'datePosted': comment.datePosted.strftime("%Y-%m-%d"),
        'text': comment.text})

    # Return result_set as JSON
    return HttpResponse(simplejson.dumps(result_set),
                        content_type="application/json")

def getvehiclecomments(request):
    """Takes a GET request as input. Returns a JSON response. Used for adding
    vehicle comments to system and returning updated comments list
    Example: ?vehicleId=30"""
    # Retreive route from GET request
    vehicleId = request.GET['vehicleId']

    result_set = []

    # Get list of comments for route
    comments = MUNISystem.getVehicleComments(vehicleId)

    # Step through each comment and append to result_set
    for comment in comments:
        result_set.append({
        'datePosted': comment.datePosted.strftime("%Y-%m-%d"),
        'text': comment.text})

    # Return result_set as JSON
    return HttpResponse(simplejson.dumps(result_set),
                        content_type="application/json")
