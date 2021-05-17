from cashier import Cashier
import random

class CashierStage:
    def __init__(self, commonCustomers, prioritaryCustomers, commonCashiers,
        prioritaryCashiers, queueLimit=10000000):
        # Stage status variables
        self.commonCustomers = commonCustomers 
        self.prioritaryCustomers = prioritaryCustomers
        self.commonCashiers = self.setCashiers(commonCashiers)
        self.prioritaryCashiers = self.setCashiers(prioritaryCashiers) 
        self.breakTime = 240 # 4h de trabajo y descanso almuerzo 
        self.operationalTime = 100000

        # Other variables
        self.departureInterval = 30 # TODO - función de probabilidad 
        self.operationalInvertal = 300 # TODO 
        self.fixTime = 150 # TODO 
        self.queueLimit = queueLimit

    def setCashiers(self, cashiersAmount):
        return [Cashier() for i in range(cashiersAmount)]

    def arrival(self):
        randomValue = random.randint(1, 10) 

        if (randomValue <= 7):
            self.commonCustomers += 1 
        else:
            self.prioritaryCustomers += 1

    def departure(self, cashierType, cashierIndex):
        if cashierType == 'c':
            self.commonCustomers -= 1
            self.commonCashiers[cashierIndex].departure()
        elif cashierType == 'p':
            self.prioritaryCustomers -= 1
            self.prioritaryCashiers[cashierIndex].departure()
    
    def getIdleCashier(self, type):
        if type == 'c':
            cashiers = self.commonCashiers
        elif type == 'p':
            cashiers = self.prioritaryCashiers

        for index, cashier in enumerate(cashiers):
            if cashier.status == 0: return index

        return None
    
    def getBussyCashiers(self, type):
        count = 0
        if type == 'c':
            cashiers = self.commonCashiers
        elif type == 'p':
            cashiers = self.prioritaryCashiers

        for cashier in cashiers:
            if cashier.status == 1: count += 1

        return count

    def getToWork(self, masterClock):
        for cashierType in ['c', 'p']:
            # Check idle cashiers
            cashierIndex = self.getIdleCashier(cashierType)

            if cashierType == 'c':
                customers = self.commonCustomers
                cashiers = self.commonCashiers
            elif cashierType == 'p':
                customers = self.prioritaryCustomers
                cashiers = self.prioritaryCashiers

            if not (cashierIndex is not None
                and customers > 0
                and self.getBussyCashiers(cashierType) < customers):
                continue
            
            # Agregar función de probabilidad
            newDepartureTime = masterClock + self.departureInterval
            cashiers[cashierIndex].setNewDeparture(newDepartureTime)

            return {
                "serverType": cashierType,
                "index": cashierIndex,
                "time": newDepartureTime
            }
        
        return None

    def getNumCustomers(self):
        return self.commonCustomers + self.prioritaryCustomers

    def isFull(self):
        return True if self.getNumCustomers() >= self.queueLimit else False
    
    def getStageStatus(self):
        commonCashiersState = []
        for cashier in self.commonCashiers:
            for element in cashier.getState():
                commonCashiersState.append(element)

        prioritaryCashiersState = []
        for cashier in self.prioritaryCashiers:
            for element in cashier.getState():
                prioritaryCashiersState.append(element)

        return [
            self.getNumCustomers(),
            *commonCashiersState,
            *prioritaryCashiersState,
            self.breakTime,
            self.operationalTime
        ]