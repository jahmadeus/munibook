class Message:
    def __init__(self, text, priority):
        self.text = text
        self.priority = priority

    def __str__(self):
        return self.text

    def isHighPriority(self):
        return self.priority == "High"

class Prediction:
    def __init__(self, epochTime, seconds, minutes, isDeparture, dirTag, vehicleId, affectedByLayover='false'):
        self.epochTime = epochTime
        self.seconds = seconds
        self.minutes = minutes
        self.isDeparture = isDeparture
        self.dirTag = dirTag
        self.vehicleId = vehicleId
        self.affectedByLayover = affectedByLayover

    def __iter__(self):
        for i in (self.epochTime, self.seconds, self.minutes, self.isDeparture,
                  self.dirTag, self.vehicleId, self.affectedByLayover):
            yield i


class Direction:
    def __init__(self, title, predictions=None):
        self.title = title
        if predictions is None:
            predictions = []
        else:
            self.predictions = predictions[:]

    def __str__(self):
        return self.title

    def getPredictions_Dict(self):
        dict_predictions = []
        for prediction in self.predictions:
            dict_predictions.append(prediction.__dict__)
        return dict_predictions

    def __iter__(self):
        tuplePredictions = []
        for prediction in self.predictions:
            tuplePredictions.append(tuple(prediction))
        for i in (self.title, tuplePredictions):
            yield i


class Response:
    def __init__(self, routeTitle, stopTitle, predictionDirections=None, messages=None):
        self.routeTitle = routeTitle
        self.stopTitle = stopTitle

        if predictionDirections is None:
            self.predictionDirections = []
        else:
            self.predictionDirections = predictionDirections[:]

        if messages is None:
            self.messages = []
        else:
            self.messages = messages[:]

    def getRouteTitle(self):
        return self.routeTitle

    def getRouteShortTitle(self):
        return self.routeTitle.split("-", 1)[-1]

    def getPredictionsTupleList(self):
        tuplepredictionDirections = []
        for routeDirection in self.predictionDirections:
            tuplepredictionDirections.append(tuple(routeDirection))
        return tuplepredictionDirections

    def getMessages(self):
        allMessages = []
        for message in self.messages:
            allMessages.append(message.text)
        return allMessages
