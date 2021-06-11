class Stage:
    IDLE = 100000
    SERVER_STATUS = {
        0: "idle",
        1: "busy",
        2: "down",
        3: "blocked"
    }

    def __init__(self, numCustomers, departureTime, breakTime, operationalTime,
        serverStatus, queueLimit=10000000):
        # Stage status variables
        self.numCustomers = numCustomers
        self.departureTime = departureTime
        self.breakTime = breakTime
        self.operationalTime = operationalTime
        self.serverStatus = serverStatus

        # Other variables
        self.departureInterval = 20 # TODO función de probabilidad
        self.operationalInvertal = 200 # TODO función de probabilidad
        self.fixTime = 50 # TODO función de probabilidad
        self.queueLimit = queueLimit
    
    def arrival(self):
        self.numCustomers += 1

    def departure(self):
        self.numCustomers -= 1
        self.serverStatus = 0
        self.departureTime = self.IDLE
    
    def getToWork(self, masterClock):
        if not (self.serverStatus == 0 and self.numCustomers > 0):
            return None

        # Agregar función de probabilidad
        self.departureTime = masterClock + self.departureInterval
        self.serverStatus = 1

        return {
            "serverType": "s",
            "index": 0,
            "time": self.departureTime
        }
    
    def breakEvent(self, masterClock, serverType, index):
        if self.serverStatus == 1:
            # Updating status
            self.breakTime = self.departureTime

            return [
                "BREAK",
                {
                    "serverType": serverType,
                    "index": index,
                    "time": self.departureTime
                }
            ]

        elif self.serverStatus == 0:
            newOperationalTime = masterClock + self.fixTime

            # Updating status
            self.breakTime = self.IDLE
            self.operationalTime = newOperationalTime
            self.serverStatus = 2
            
            return [
                "OPERATION",
                {
                    "serverType": serverType,
                    "index": index,
                    "time": newOperationalTime 
                }
            ]
        
        return None 
    
    def operationEvent(self, masterClock, serverType, index):
        # Updating state
        self.operationalTime = self.IDLE

        newBreakTime = masterClock + self.operationalInvertal
        self.breakTime = newBreakTime

        if self.serverStatus != 3:
            if self.departureTime != self.IDLE:
                self.serverStatus = 1
            else:
                self.serverStatus = 0

        return {
            "serverType": serverType,
            "index": index,
            "time": newBreakTime 
        }

    def blockServer(self):
        self.serverStatus = 3
    
    def unlockServer(self):
        self.numCustomers -= 1
        self.serverStatus = 0

    def isBlocked(self):
        return True if self.serverStatus == 3 else False

    def isFull(self):
        return True if self.numCustomers >= self.queueLimit else False

    def getServerStatus(self):
        return self.SERVER_STATUS[self.serverStatus]
    
    def getStageStatus(self):
        return [
            self.numCustomers,
            self.departureTime,
            self.breakTime,
            self.operationalTime,
            self.getServerStatus()
        ]