from simulation import Simulation

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
    steps = validNumberInput("Enter the number of steps to simulate: ", min=1)

    simulation = Simulation()

    simulation.executeSimulation(steps)

if __name__ == "__main__":
    main()