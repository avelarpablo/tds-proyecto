class Cashier:
    IDLE = 100000
    STATUS = {
        0: "idle",
        1: "busy",
        2: "down"
    }

    def __init__(self):
        self.departureTime = self.IDLE
        self.status = 0
    
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
            self.getStatus()
        ]