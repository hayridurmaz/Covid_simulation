import math
import matplotlib.pyplot as plt
import numpy as np
import random as rm
import os
import sys
import argparse as arg

def getPeopleRecovered(t, z_list):
    recovered_t_delay = 2
    death_t_delay = 2
    p_recovered = 0.9
    p_death = 0.1
    rt_half = 0

    if t < recovered_t_delay:
        rt_half = p_recovered * 0
    else:
        rt_half = p_recovered * z_list[t - recovered_t_delay]

    if t < death_t_delay:
        rt = p_death * 0 + rt_half
    else:
        rt = p_death * z_list[t - death_t_delay] + rt_half
    print("getPeopleRecovered", math.floor(rt))
    return math.floor(rt)


def getPeopleInQuarantine(t, z_list):
    detected_t_delay = 2
    undetected_t_delay = 2
    p_detected = 0.9
    p_undetected = 0.1
    q_half = 0

    if t < detected_t_delay:
        q_half = p_detected * 0
    else:
        q_half = p_detected * z_list[t - detected_t_delay]

    if t < undetected_t_delay:
        qt = p_undetected * 0 + q_half
    else:
        qt = p_undetected * z_list[t - undetected_t_delay] + q_half
    print("getPeopleInQarantine", math.floor(qt))
    return math.floor(qt)


def infectionRate(t, z_list, total_pop):
    tdelay = 0
    mi = 1.01
    temp = (z_list[t - tdelay] * mi) / (total_pop)
    print("infectionRate", temp)
    return temp


# A function that implements the Markov model to forecast the state/mood.
def activity_forecast(days, stateToday="Susceptible"):
    startingProbabilities = [[0.2, 0.6, 0.2, 0], [0, 0.1, 0.6, 0.3], [0, 0, 1, 0], [0, 0, 0, 1]]
    stateList = [stateToday]
    i = 0
    prob = 1
    while i != days:
        if stateToday == "Susceptible":
            change = np.random.choice(transitionName[0], replace=True, p=transitionMatrix[0])
            if change == "SS":
                prob = prob * startingProbabilities[0][0]
                stateList.append("Susceptible")
                pass
            elif change == "SI":
                prob = prob * startingProbabilities[0][1]
                stateToday = "Infected"
                stateList.append("Infected")
            else:
                prob = prob * startingProbabilities[0][2]
                stateToday = "Recovered"
                stateList.append("Recovered")
        elif stateToday == "Infected":
            change = np.random.choice(transitionName[1], replace=True, p=transitionMatrix[1])
            if change == "II":
                prob = prob * startingProbabilities[1][1]
                stateList.append("Infected")
                pass
            elif change == "IR":
                prob = prob * startingProbabilities[1][2]
                stateToday = "Recovered"
                stateList.append("Recovered")
            else:
                prob = prob * startingProbabilities[1][3]
                stateToday = "Dead"
                stateList.append("Dead")
        elif stateToday == "Recovered":
            change = np.random.choice(transitionName[2], replace=True, p=transitionMatrix[2])
            if change == "DD":
                prob = prob * startingProbabilities[2][2]
                stateList.append("Recovered")
                pass
            else:
                prob = prob * 0
                stateToday = "N/A"
                stateList.append("N/A")
        elif stateToday == "Dead":
            change = np.random.choice(transitionName[2], replace=True, p=transitionMatrix[3])
            if change == "DD":
                prob = prob * startingProbabilities[3][3]
                stateList.append("Dead")
                pass
            else:
                prob = prob * 0
                stateToday = "N/A"
                stateList.append("N/A")
        i += 1
    return stateList

def Arg_Parse():
    Arg_Par = arg.ArgumentParser()
    Arg_Par.add_argument("-d", "--Death",
                         help="Current death rate")
    Arg_Par.add_argument("-r", "--recovery",
                         help="Current recovery rate")
    arg_list = vars(Arg_Par.parse_args())
    return arg_list

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Please Provide an argument !!!")
        sys.exit(0)
    Arg_list = Arg_Parse()

    # The statespace
    states = ["Susceptible", "Infected", "Recovered", "Dead"]

    # Possible sequences of events
    transitionName = [["SS", "SI", "SR", "SD"], ["IS", "II", "IR", "ID"], ["RS", "RI", "RR", "RD"],
                      ["DS", "DI", "DR", "DD"]]

    # Probabilities matrix (transition matrix)
    transitionMatrix = [[0.2, 0.6, 0.2, 0], [0, 0.1, 0.6, 0.3], [0, 0, 1, 0], [0, 0, 1, 0]]

    if sum(transitionMatrix[0]) + sum(transitionMatrix[1]) + sum(transitionMatrix[2]) + sum(transitionMatrix[3]) != 4:
        print("Somewhere, something went wrong. Transition matrix, perhaps?")
    else:
        print("All is gonna be okay, you should move on!! ;)")

    # Function that forecasts the possible state for the next 2 days
    activity_forecast(2)

    # To save every activityList
    list_activity = []
    count = 0

    # `Range` starts from the first count up until but excluding the last count
    for iterations in range(1, 10000):
        list_activity.append(activity_forecast(2))

    # Check out all the `activityList` we collected
    # print(list_activity)

    # Iterate through the list to get a count of all activities ending in state:'Run'
    for smaller_list in list_activity:
        if (smaller_list[2] == "Dead"):
            count += 1

    # Calculate the probability of starting from state:'Sleep' and ending at state:'Run'
    percentage = (count / 10000) * 100
    print("The probability of starting at state:'Susp' and ending at state:'Dead'= " + str(percentage) + "%")
