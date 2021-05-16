from simulation import Simulation
from stage import Stage

def validNumberInput(message, min=None, max=None):
    while True:
        error = False

        try:
            value = int(input(message))

            # Validating min
            if min is not None:
                if value < min: error = True
            if max is not None:
                if value > max: error = True
        except ValueError:
            error = True

        if error:
            errorMsg = "Error: you must enter integer values "
            if min is not None and max is not None:
                errorMsg += f"greater than or equals to {min} and lower than or equals to {max}."
            else:
                errorMsg += f"greater than or equals to {min}." if min is not None else ""
                errorMsg += f"lower than or equals to {max}." if max is not None else ""
            
            print(errorMsg + "\n")
        else:
            break

    return value

def main():
    # stages = validNumberInput("Enter the number of stages: ", min=1)

    # stagesList = []
    # for stage in range(stages):
    #     print(f"\nEnter values for stage {stage + 1}:")
    #     numCustomers = validNumberInput("- Initial number of customers: ", min=0)
    #     departureTime = validNumberInput("- Initial departure time: ", min=1)
    #     breakTime = validNumberInput("- Initial break time: ", min=1)
    #     operationalTime = validNumberInput("- Initial operational time: ", min=1)
    #     serverStatus = validNumberInput("- Initial server status: ", min=0, max=3)
    #     departureInterval = validNumberInput("- Departure interval: ", min=1)
    #     operationalInvertal = validNumberInput("- Operational interval: ", min=1)
    #     fixTime = validNumberInput("- Fix time: ", min=1)
    #     # First stage has no queue limit
    #     if stage == 0:
    #         queueLimit = 10000
    #     else:
    #         queueLimit = validNumberInput("- Stage queue limit: ", min=1)

    #     stagesList.append(Stage(numCustomers, departureTime, breakTime, operationalTime, 
    #         serverStatus, departureInterval, operationalInvertal, fixTime, queueLimit))
            
    # firstArrival = validNumberInput("\nEnter the first arrival time: ", min=1)
    # arrivalInterval = validNumberInput("Enter the arrival interval time: ", min=1)

    # simulation = Simulation(firstArrival, arrivalInterval, stagesList)

    simulation = Simulation(10)

    simulation.executeSimulation()

if __name__ == "__main__":
    main()