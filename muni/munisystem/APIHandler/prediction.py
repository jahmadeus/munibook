import simplejson

class Message:
    """Represents the messages being retreived from the API"""
    def __init__(self, text, priority):
        self.text = text
        self.priority = priority

    def __str__(self):
        return self.text

class Prediction:
    """Represents a prediction being retreived from the API"""
    def __init__(self, epochTime, seconds, minutes, isDeparture, dirTag,
                 vehicleId, affectedByLayover='false'):
        self.epochTime = epochTime
        self.seconds = seconds
        self.minutes = minutes
        self.isDeparture = isDeparture
        self.dirTag = dirTag
        self.vehicleId = vehicleId
        self.affectedByLayover = affectedByLayover

    def __iter__(self):
        for i in (self.epochTime, self.seconds,
                  self.minutes, self.isDeparture,
                  self.dirTag, self.vehicleId, self.affectedByLayover):
            yield i

class Direction:
    """Represents the prediction direction being retreived from the API.
    Contains a liste of corresponding Prediction objects"""
    def __init__(self, title, predictions=None):
        self.title = title
        # If predictions were not given, initialze empty list
        if predictions is None:
            self.predictions = []
        else:
            self.predictions = predictions[:]

    def __str__(self):
        """Return Direction as a string. (Just the title)"""
        return self.title

    def getPredictions_Dict(self):
        """Gets list of contained Directions as dictionaries"""
        dict_predictions = []
        # For each prediction in list, append dictionary version to list
        for prediction in self.predictions:
            dict_predictions.append(prediction.__dict__)
        # Return list of direction dictionaries
        return dict_predictions

    def asDict(self):
        """Return Direction object and contained list of Predictions as
        dictionary"""
        dir_dict = {}
        # Add direction title and list of Predictions dict's to dictionary
        dir_dict['title'] = self.title
        dir_dict['predictions'] = self.getPredictions_Dict()
        # Return Direction record as dictionary
        return dir_dict

    def __iter__(self):
        tuplePredictions = []
        for prediction in self.predictions:
            tuplePredictions.append(tuple(prediction))
        for i in (self.title, tuplePredictions):
            yield i

class Response:
    """Responsible for containing the predictions response data retreived from
    the API."""
    def __init__(self, routeTitle, stopTitle, predictionDirections=None,
                 messages=None):
        self.routeTitle = routeTitle
        self.stopTitle = stopTitle

        # If predictionDirections were not given, initialze empty list
        if predictionDirections is None:
            self.predictionDirections = []
        else:
            # Else, copy given list to object attribute
            self.predictionDirections = predictionDirections[:]

        # If messages were not given, initialze empty list
        if messages is None:
            self.messages = []
        else:
            # Else, copy given list to object attribute
            self.messages = messages[:]


    def getRouteShortTitle(self):
        """Returns shortened route title.
        Example: 30-Stockton becomes Stockton"""
        # Remove everything up to and including the first hyphen
        return self.routeTitle.split("-", 1)[-1]

    def getPredictionsTupleList(self):
        """Returns Prediction Response as a list of tuples. To be removed soon
        as getJSON() or asDict will work better."""
        tuplepredictionDirections = []
        # Step through each predictionDirection and append tuple version
        for routeDirection in self.predictionDirections:
            tuplepredictionDirections.append(tuple(routeDirection))
        # Return list of tuples
        return tuplepredictionDirections

    def getMessages(self):
        """Returns all contained messages"""
        allMessages = []
        for message in self.messages:
            allMessages.append(message.text)
        return allMessages

    def getMessages_Dict(self):
        """Returns all contained  Message records as a list of dictionaries"""
        dict_messages = []
        for message in self.messages:
            dict_messages.append(message.__dict__)
        return dict_messages

    def getDirections_Dict(self):
        """Returns all contained Direction records as list of dictionaries"""
        dict_directions = []
        for direction in self.predictionDirections:
            dict_directions.append(direction.asDict())
        return dict_directions


    def asDict(self):
        """Returns prediction Response as a dictionary of dictionaries"""
        response_dict = {}
        response_dict['route_title'] = self.routeTitle
        response_dict['stop_title'] = self.stopTitle
        response_dict['predictions_data'] = self.getDirections_Dict()
        response_dict['messages'] = self.getMessages_Dict()
        return response_dict

    def getJSON(self):
        """Return prediction Response (in dictionary form) as JSON"""
        return simplejson.dumps(self.asDict())

    def getVehicles(self):
        """Returns all vehicle Id's associated with Prediction records"""
        vehicles = []
        for direction in self.predictionDirections:
            for prediction in direction.predictions:
                vehicles.append(prediction.vehicleId)
        return vehicles
