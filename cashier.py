class Cashier:
    IDLE = 100000
    STATUS = {
        0: "idle",
        1: "busy",
        2: "down"
    }

    def __init__(self, breakTime = 10):
        self.departureTime = self.IDLE
        self.breakTime = breakTime
        self.operationalTime = self.IDLE 
        self.status = 0

        self.departureInterval = 30 # TODO - función de probabilidad 
        self.operationalInvertal = 300 # TODO 
        self.fixTime = 150 # TODO 
    
    def departure(self):
        self.departureTime = self.IDLE 
        self.status = 0
    
    def setNewDeparture(self, time):
        self.departureTime = time
        self.status = 1

    def getStatus(self):
        return self.STATUS[self.status]

    def getState(self):
        return [
            self.departureTime,
            self.breakTime,
            self.operationalTime,
            self.getStatus()
        ]