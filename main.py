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