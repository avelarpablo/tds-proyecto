from linkedList import LinkedList
from stage import Stage
from cashiersStage import CashierStage
from numpy import np
import math
import csv

IDLE = 100000

# Events types
ARRIVAL = "ARRIVAL"
DEPARTURE = "DEPARTURE"
BREAK = "BREAK"
OPERATION = "OPERATION"

def setEventType(typeCode, serverType, index):
    return { "typeCode": typeCode, "serverType": serverType, "index": index }

class Simulation:
    def __init__(self, fistArrival):
        self.masterClock = 0
        self.arrivalTime = fistArrival
        self.stage = Stage(0, IDLE, 15, IDLE, 0)
        self.cashierStage = CashierStage(0, 0, 3, 1, 25)
        self.createFutureEventList()
        self.createResultsTable()

    def getNewArrivalTime(self):
        return self.masterClock + math.trunc(np.random.normal(223.69, 92.15))

    def createFutureEventList(self):
        self.futureEventList = LinkedList()

        self.futureEventList.insertNode(
            setEventType(ARRIVAL, 's', 0),
            self.arrivalTime
        )

        # First stage events
        self.futureEventList.insertNode(
            setEventType(BREAK, 's', 0),
            self.stage.breakTime
        )            

        # Second stage events
        # Common cashiers
        for index, cashier in enumerate(self.cashierStage.commonCashiers):
            if cashier.breakTime != IDLE:
                self.futureEventList.insertNode(
                    setEventType(BREAK, 'c', index),
                    cashier.breakTime
                )            

            if cashier.operationalTime != IDLE:
                self.futureEventList.insertNode(
                    setEventType(OPERATION, 'c', index),
                    cashier.operationalTime
                )            
                
        # Common cashiers
        for index, cashier in enumerate(self.cashierStage.prioritaryCashiers):
            if cashier.breakTime != IDLE:
                self.futureEventList.insertNode(
                    setEventType(BREAK, 'p', index),
                    cashier.breakTime
                )            

            if cashier.operationalTime != IDLE:
                self.futureEventList.insertNode(
                    setEventType(OPERATION, 'p', index),
                    cashier.operationalTime
                )            

    def createResultsTable(self):
        self.resultsTable = []

        commonHeader = []
        for i in range(len(self.cashierStage.commonCashiers)):
            header = [
                f"DT2-C{i + 1}",
                f"BT2-C{i + 1}",
                f"OT2-C{i + 1}",
                f"CS{i + 1}"
            ]
            
            for element in header:
                commonHeader.append(element)

        priotaryHeader = []
        for i in range(len(self.cashierStage.prioritaryCashiers)):
            header = [
                f"DT2-D{i + 1}",
                f"BT2-D{i + 1}",
                f"OT2-D{i + 1}",
                f"PS{i + 1}"
            ]

            for element in header:
                priotaryHeader.append(element)

        self.resultsTable = [[
            "Steps",
            "MC",
            "AT",
            *[f"NC1", f"DT1", f"BR1", f"OP1", f"SS1"],
            "NC2",
            *commonHeader,
            *priotaryHeader,
            "BR2",
            "OP2"
        ]]

        # Setting results table initial values with empty step
        self.addCurrentStateToTable("") 
    
    def addCurrentStateToTable(self, step):
        # Save current state
        self.resultsTable.append([
            step,
            self.masterClock,
            self.arrivalTime,
            *self.stage.getStageStatus(),
            *self.cashierStage.getStageStatus() 
        ])
    
    def printResultsTable(self):
        for line in self.resultsTable:
            lineString = "|"
            for element in line:
                lineString += str(element).center(8) + "|"
            print(lineString)
    
    def printRestultsTableAsCSV(self):
        with open('simulation_results.csv', mode='w') as restult_file:
            results_writer = csv.writer(
                restult_file,
                delimiter=',',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL
            )

            for row in self.resultsTable:
                results_writer.writerow(row)

    def getNextEvent(self):
        return self.futureEventList.removeFirstNode()

    def advanceTime(self, nextTime):
        self.masterClock = nextTime
    
    def executeAction(self, eventType):
        typeCode = eventType["typeCode"]
        serverType = eventType["serverType"]
        index = eventType["index"]
        # stage = self.stages[stageIndex]

        # Case ARRIVAL
        if typeCode == ARRIVAL:
            self.stage.arrival()            
            
            # Set new arrival
            self.arrivalTime = self.getNewArrivalTime()
            self.futureEventList.insertNode(
                setEventType(ARRIVAL, 's', 0),
                self.arrivalTime
            )

        # Case DEPARTURE
        if typeCode == DEPARTURE:
            # If first stage
            if serverType == 's':
                if not self.cashierStage.isFull():
                    self.cashierStage.arrival()
                    self.stage.departure()
                else:
                    self.stage.blockServer()
            else:
                self.cashierStage.departure(serverType, index)

                # Check if stage 1 is blocked
                if self.stage.isBlocked():
                    self.stage.unlockServer()
                    self.cashierStage.arrival()

        # Case BREAK
        if typeCode == BREAK:
            stage = self.stage if serverType == 's' else self.cashierStage

            eventReturn = stage.breakEvent(self.masterClock, serverType, index)

            if eventReturn is not None:
                eventCode, eventValues = eventReturn

                self.futureEventList.insertNode(
                    setEventType(
                        eventCode,
                        eventValues["serverType"],
                        int(eventValues["index"])
                    ),
                    eventValues["time"]
                )
        
        # Case OPERATION
        if typeCode == OPERATION:
            stage = self.stage if serverType == 's' else self.cashierStage

            eventValues = stage.operationEvent(
                self.masterClock,
                serverType,
                index
            )

            self.futureEventList.insertNode(
                setEventType(
                    BREAK,
                    eventValues["serverType"],
                    int(eventValues["index"])
                ),
                eventValues["time"]
            )
            
        # Check if there is any break in the same time in the same machine
        nextEvent = self.futureEventList.head

        if (nextEvent.type["typeCode"] == BREAK
            and nextEvent.clock == self.masterClock 
            and nextEvent.type["serverType"] == serverType
            and nextEvent.type["index"] == index):
            return
        
        # Check if there is any idle server
        for stage in [self.stage, self.cashierStage]:
            departureValues = stage.getToWork(self.masterClock)

            if departureValues is not None:
                # Add event to futureEventList
                self.futureEventList.insertNode(
                    setEventType(
                        DEPARTURE,
                        departureValues["serverType"],
                        int(departureValues["index"])
                    ),
                    departureValues["time"]
                )

    def executeSimulation(self, steps=100):
        for step in range(steps):
            if self.futureEventList.head == None:
                break
            
            # Find next event
            event = self.getNextEvent()

            # Advance time
            self.advanceTime(event.clock)

            # Execute actions
            self.executeAction(event.type)

            # Check if there is any aditional event in this time
            while self.futureEventList.head.clock == event.clock:
                event = self.getNextEvent()
                self.executeAction(event.type)
            
            # Add current state to results table
            self.addCurrentStateToTable(step + 1)            
      
        # Print results table
        self.printRestultsTableAsCSV()
        print("See results in file simulation_results.csv")
