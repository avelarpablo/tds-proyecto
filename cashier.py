"""
    Universidad de El Salvador

    Authors: 
    - Avelar Melgar, José Pablo		    –	AM16015
    - Campos Martínez, Abraham Isaac 	– 	CM17045
    - Lizama Escobar, Oscar Omar	    –	LE17004
    - Paredes Pastrán, Carlos Enrique	–	PP17012
    - Quinteros Lemus, Diego Enrique	–	QL17001

    Activity: Application project
    Subject: Técnicas de Simulación (TDS115)
    Professor: Lic. Guillermo Mejía
    Date: 06/11/2021
"""

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