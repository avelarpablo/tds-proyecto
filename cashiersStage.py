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

from cashier import Cashier
import numpy as np
import math
import random

class CashierStage:
    def __init__(self, commonCustomers, prioritaryCustomers, commonCashiers,
        prioritaryCashiers, queueLimit=10000000):
        # Stage status variables
        self.commonCustomers = commonCustomers 
        self.prioritaryCustomers = prioritaryCustomers
        self.commonCashiers = self.setCashiers(commonCashiers)
        self.prioritaryCashiers = self.setCashiers(prioritaryCashiers) 

        # Other variables
        self.queueLimit = queueLimit

    def setCashiers(self, cashiersAmount):
        return [Cashier(self.getNewBreakTime(0)) for i in range(cashiersAmount)]

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

    def getNewDepartureTime(self, masterClock):
        return masterClock + math.trunc(np.random.lognormal(5.45, 0.53))

    def getNewOperationalTime(self, masterClock):
        return masterClock + math.trunc(np.random.exponential(4095))
    
    def getNewBreakTime(self, masterClock):
        return masterClock + math.trunc(np.random.normal(17022, 6365))
    
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
            newDepartureTime = self.getNewDepartureTime(masterClock)
            cashiers[cashierIndex].setNewDeparture(newDepartureTime)

            return {
                "serverType": cashierType,
                "index": cashierIndex,
                "time": newDepartureTime
            }
        
        return None

    def breakEvent(self, masterClock, serverType, index):
        cashiers = self.commonCashiers if serverType == 'c' else self.prioritaryCashiers
        cashier = cashiers[index]
        
        if cashier.status == 1:
            # Updating status
            cashier.breakTime = cashier.departureTime

            return [
                "BREAK",
                {
                    "serverType": serverType,
                    "index": index,
                    "time": cashier.departureTime
                }
            ]

        elif cashier.status == 0:
            newOperationalTime = self.getNewOperationalTime(masterClock)

            # Updating status
            cashier.breakTime = cashier.IDLE
            cashier.operationalTime = newOperationalTime
            cashier.status = 2
            
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
        cashiers = self.commonCashiers if serverType == 'c' else self.prioritaryCashiers
        cashier = cashiers[index]

        # Updating state
        cashier.operationalTime = cashier.IDLE
        cashier.status = 0

        newBreakTime = self.getNewBreakTime(masterClock)
        cashier.breakTime = newBreakTime

        return {
            "serverType": serverType,
            "index": index,
            "time": newBreakTime 
        }

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
            *prioritaryCashiersState
        ]