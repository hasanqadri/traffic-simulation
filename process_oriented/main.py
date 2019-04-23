from __future__ import division
from heapq import heappush, heappop
import time
#Graphing and Analysis imports
import numpy as np
#import scipy
#import scipy.stats as stats
import math
import random
#Reading JSON file imports (Converted CSV to JSON in preprocessing)
import json

from util import *
from threaded import *


#Initializing simulation
FEL = []

#GLT, RLT, GTR, RTR/LT
#Below are street light lengths for each street
northSignals10 = [10.6, 2.2, 38.1, 49.3]
northSignals14 = [12.4, 3.6, 37.8, 45.3]
#GTR, RTR/LT
northSignals11 = [44.7, 55.4]
northSignals12 = [64.1, 35.7]
#13th street has no lights!

START_TIME = 1163030800
currentTime = START_TIME

carTravelTimes = []
leftTurnChance = 0
rightTurnChance = 0
rightTurn = 0
leftTurn = 0

#Queue initializations and system states. Segments are named after the preceding intersection
curr10Light = 'green'
curr10LeftLight = 'green'
tenLeftDelay = 0
tenDelay = 0

curr11Light = 'green'
elevenDelay = 0

curr12Light = 'green'
twelveDelay = 0

curr14Light = 'green'
curr14LeftLight = 'green'
fourteenDelay = 0
fourteenLeftDelay = 0

events = {}
numCars = 1
numEvents = 0


# Populates our event list with inital events.
# There is a chance our simulation is short-lived or very long depending on these initial events
def getHistoricalEvents():
    global events
    global leftTurnChance
    global rightTurnChance
    events = {}

    with open('../data/trajectories0.json') as json_data:
        events = json.load(json_data)

    with open('../data/trajectories1.json') as json_data:
        events.update(json.load(json_data))

    with open('../data/trajectories2.json') as json_data:
        events.update(json.load(json_data))

    with open('../data/trajectories3.json') as json_data:
        events.update(json.load(json_data))

    with open('../data/trajectories4.json') as json_data:
        events.update(json.load(json_data))

    numEvents = len(events.keys())
    heappush(FEL,(currentTime + northSignals10[3]*1000, ['NorthSignals10', 'red']))      #Traffic lights shceduled
    heappush(FEL,(currentTime + northSignals11[1]*1000, ['NorthSignals11', 'red']))
    heappush(FEL,(currentTime + northSignals12[1]*1000, ['NorthSignals12', 'red']))
    heappush(FEL,(currentTime + northSignals14[3]*1000, ['NorthSignals14', 'red']))
    heappush(FEL,(currentTime + northSignals10[1]*1000, ['NorthSignalsLeft10', 'red']))    #Traffic left-turn lights scheduled
    heappush(FEL,(currentTime + northSignals14[3]*1000, ['NorthSignalsLeft14', 'red']))
    arrivalTime = getInterArrivalTime()
    leftTurnChance = getLeftTurnChance()
    rightTurnChance = getRightTurnChance()
    heappush(FEL,(arrivalTime, ['NinthSegment', leftTurnChance, rightTurnChance, arrivalTime]))  #First car event that is scheduled
    return FEL

# Randomly generated interarrival time from empirical distribution which is used for initial car creation
def getInterArrivalTime():
    global numEvents
    #Interarrival times
    interArrivalTimes = [0]
    for n in range(int(numEvents/10000)):  #Dividing by 1000 limits range of interarrival times but GREATLY speeds up the simulation
        interArrivalTimes.append(0)
    for z in range(int(numEvents/10000)):
        interArrivalTimes[z] = events[str(z)]['Epoch_ms'] - START_TIME
    i = random.randint(0, int(numEvents/10000))
    if (interArrivalTimes[i] < currentTime):
        return abs(interArrivalTimes[i] - currentTime) + interArrivalTimes[i] + 5000
    return interArrivalTimes[i]

#Calculate chance for left turn for cars at any given intersection
def getRightTurnChance():
    #Left turns
    intersectionCounter = 0
    leftTurnCounter = 0
    for z in range(len(events.keys())):
        if (events[str(z)]['Intersection'] != 0):
            intersectionCounter = intersectionCounter + 1
            if (events[str(z)]['Movement'] == 2):
                leftTurnCounter = leftTurnCounter + 1
    leftTurnChance = leftTurnCounter / intersectionCounter
    return leftTurnChance

#Calculate chance for right turn for cars at any given itnersection
def getLeftTurnChance():
    #Left turns
    intersectionCounter = 0
    rightTurnCounter = 0
    for z in range(len(events.keys())):
        if (events[str(z)]['Intersection'] != 0):
            intersectionCounter = intersectionCounter + 1
            if (events[str(z)]['Movement'] == 3):
                rightTurnCounter = rightTurnCounter + 1
    rightTurnChance = rightTurnCounter / intersectionCounter
    return rightTurnChance

#E xecute the event and schedule the next events
# Main event scheduler
def executeEvent(event):
    global numCars
    #Read type of event and execute that event
    if (event[1][0] == 'NorthSignals10'):
        switchTenthLights(event)
    elif (event[1][0] == 'NorthSignalsLeft10'):
        switchTenthLeftLights(event)
    elif (event[1][0] == 'NorthSignals11'):
        switchEleventhLights(event)
    elif (event[1][0] == 'NorthSignals12'):
        switchTwelfthLights(event)
    elif (event[1][0] == 'NorthSignals14'):
        switchFourteenthLights(event)
    elif (event[1][0] == 'NorthSignalsLeft14'):
        switchFourteenthLeftLights(event)
    elif (event[1][0] == 'NinthSegment'):
        numCars = numCars + 1
        ninthSegment(event)
    elif (event[1][0] == 'TenthIntersection'):
        tenthIntersection(event)
    elif (event[1][0] == 'TenthSegment'):
        tenthSegment(event)
    elif (event[1][0] == 'EleventhIntersection'):
        eleventhIntersection(event)
    elif (event[1][0] == 'EleventhSegment'):
        eleventhSegment(event)
    elif (event[1][0] == 'TwelfthIntersection'):
        twelfthIntersection(event)
    elif (event[1][0] == 'TwelfthSegment'):
        twelfthSegment(event)
    elif (event[1][0] == 'FourteenthIntersection'):
        fourteenthIntersection(event)
    elif (event[1][0] == 'FourteenthSegment'):
        fourteenthSegment(event)
    # Simulates adding new car to our sim
    if (currentTime % 10000 < 900):
        arrivalTime = getInterArrivalTime()
        heappush(FEL,(arrivalTime, ['NinthSegment', leftTurnChance, rightTurnChance, arrivalTime]))


# Event - Entering segment before 10th intersection
# Determines if car takes left or right turn at next intersection and schedules that event.
def ninthSegment(event):
    turnResult = checkLeftRightTurn(event)
    if (turnResult == 1):
        heappush(FEL,(event[0] + 1000, ['TenthIntersection', event[1][1], event[1][2], event[1][3], 1]))
        return 1
    elif (turnResult == 2):
        heappush(FEL,(event[0] + 1000, ['TenthIntersection', event[1][1], event[1][2], event[1][3], 2]))
        return 2
    else:
        heappush(FEL,(event[0]+ 1000, ['TenthIntersection', event[1][1], event[1][2], event[1][3], 0]))
        return 0

#Event - Entering 10th intersection
# Car takes left turn or goes straight if light if green. It takes a right turn even if light is red.
# If light is red, then cars wanting to go straight or left wait for a green.
# Returns time delayed (if any)
def tenthIntersection(event):
    global tenDelay
    global tenLeftDelay
    global leftTurn
    global rightTurn
    if (event[1][4] == 2):
        if (curr10LeftLight == 'green'):
            leftTurn = leftTurn + 1
            carTravelTimes.append(event[0] - event[1][3])
        else:
            heappush(FEL,(event[0] + 2000, ['TenthIntersection', event[1][1], event[1][2], event[1][3], 2]))
            tenLeftDelay = tenLeftDelay + 2000
            return tenLeftDelay
    elif (event[1][4] == 1):
        rightTurn = rightTurn + 1
        carTravelTimes.append(event[0] - event[1][3])
    else:
        if (curr10Light == 'green'):
            heappush(FEL,(event[0] + 1000, ['TenthSegment', event[1][1], event[1][2], event[1][3], 0]))
        else:
            heappush(FEL,(event[0] + 2000, ['TenthIntersection', event[1][1], event[1][2], event[1][3], 0]))
            tenDelay = tenDelay + 2000
            return tenDelay
    return 0


# Event - Entering 10th Segment
# Determines if car takes right turn at next intersection and schedules that event if so. Otherwise schedules going straight.
# Returns whether a turn was taken (1 == left and 0 == straight)
def tenthSegment(event):
    turnResult = checkLeftRightTurn(event)
    if (turnResult == 1):
        heappush(FEL,(event[0] + 1000, ['EleventhIntersection', event[1][1], event[1][2], event[1][3], 1]))
        return 1
    else:
        heappush(FEL,(event[0]+ 1000, ['EleventhIntersection', event[1][1], event[1][2], event[1][3], 0]))
        return 0

# Event - Entering 11th intersection
# Car goes straight if light is green. It takes a right turn even if light is red.
# Returns time delayed (if at all)
def eleventhIntersection(event):
    global elevenDelay
    global leftTurn
    global rightTurn
    if (event[1][4] == 1):
        rightTurn = rightTurn + 1
        carTravelTimes.append(event[0] - event[1][3])
    else:
        if (curr11Light == 'green'):
            heappush(FEL,(event[0] + 1000, ['EleventhSegment', event[1][1], event[1][2], event[1][3], 0]))
        else:
            heappush(FEL,(event[0] + 2000, ['EleventhIntersection', event[1][1], event[1][2], event[1][3], 0]))
            elevenDelay = elevenDelay + 2000
            return elevenDelay
    return 0


# Event - Entering 11th segment
# Determines if car takes right turn at next intersection and schedules that event. Otherwise schedules going straight.

def eleventhSegment(event):
    turnResult = checkLeftRightTurn(event)
    if (turnResult == 1):
        heappush(FEL,(event[0] + 1000, ['TwelfthIntersection', event[1][1], event[1][2], event[1][3], 1]))
        return 1
    else:
        heappush(FEL,(event[0]+ 1000, ['TwelfthIntersection', event[1][1], event[1][2], event[1][3], 0]))
        return 0


# Event - Entering 12th intersection
# Car goes straight if light is green. It takes a right turn even if light is red.
def twelfthIntersection(event):
    global twelveDelay
    global leftTurn
    global rightTurn
    if (event[1][4] == 1):
        rightTurn = rightTurn + 1
        carTravelTimes.append(event[0] - event[1][3])
    else:
        if (curr12Light == 'green'):
            heappush(FEL,(event[0] + 1000, ['TwelfthSegment', event[1][1], event[1][2], event[1][3], 0]))
        else:
            heappush(FEL,(event[0] + 2000, ['TwelfthIntersection', event[1][1], event[1][2], event[1][3], 0]))
            twelveDelay = twelveDelay + 2000
            return twelveDelay
    return 0


# Event - Entering 12th segment
# Determines if car takes left or right turn at next intersection and schedules that event. Otherwise schedules going straight.
def twelfthSegment(event):
    turnResult = checkLeftRightTurn(event)
    if (turnResult == 1):
        heappush(FEL,(event[0] + 1000, ['FourteenthIntersection', event[1][1], event[1][2], event[1][3], 1]))
        return 1
    elif (turnResult == 2):
        heappush(FEL,(event[0] + 1000, ['FourteenthIntersection', event[1][1], event[1][2], event[1][3], 2]))
        return 2
    else:
        heappush(FEL,(event[0]+ 1000, ['FourteenthIntersection', event[1][1], event[1][2], event[1][3], 0]))
        return 0

# Event - Entering 14th intersection
# Car takes left turn or goes straight if light if green. It takes a right turn even if light is red.
# If light is red, then cars wanting to go straight or left wait for a green.
def fourteenthIntersection(event):
    global fourteenDelay
    global fourteenLeftDelay
    global leftTurn
    global rightTurn
    if (event[1][4] == 2):
        if (curr14LeftLight == 'green'):
            leftTurn = leftTurn + 1
            carTravelTimes.append(event[0] - event[1][3])
        else:
            heappush(FEL,(event[0] + 2000, ['FourteenthIntersection', event[1][1], event[1][2], event[1][3], 2]))
            fourteenLeftDelay = fourteenLeftDelay + 2000
            return fourteenLeftDelay
    elif (event[1][4] == 1):
        rightTurn = rightTurn + 1
        carTravelTimes.append(event[0] - event[1][3])
    else:
        if (curr14Light == 'green'):
            heappush(FEL,(event[0] + 1000, ['FourteenthSegment', event[1][1], event[1][2], event[1][3], 0]))
        else:
            heappush(FEL,(event[0] + 2000, ['FourteenthIntersection', event[1][1], event[1][2], event[1][3], 0]))
            fourteenDelay = fourteenDelay + 2000
            return fourteenDelay
    return 0


# Event - Entering 14th segment
# Cars leave sim and we update stats
def fourteenthSegment(event):
    carTravelTimes.append(event[0] - event[1][3])

#Determine if car is going to take a left or right at a particular intersection
def checkLeftRightTurn(event):
    u = random.randint(100, 1000)/1000
    if (u < rightTurnChance):
        return 1
    u = random.randint(100, 1000)/1000
    if (u < leftTurnChance + .2): #Added .2 for testing purposes here, the generated left turn chance was too small otherwise
        return 2
    return 0

#Event - Switch 10th Street Lights
#Returns next scheduled light color
def switchTenthLights(event):
    global curr10Light
    if (event[1][1] == 'red'):
        curr10Light = 'red'
        heappush(FEL,(currentTime + northSignals10[2]*1000, ['NorthSignals10', 'green']))      #Traffic lights shceduled
        return 'green'
    else:
        curr10Light = 'green'
        heappush(FEL,(currentTime + northSignals10[3]*1000, ['NorthSignals10', 'red']))      #Traffic lights shceduled
        return 'red'

#Event - Switch 10th Street Left Turn Lights
def switchTenthLeftLights(event):
    global curr10LeftLight

    if (event[1][1] == 'red'):
        curr10LeftLight = 'red'
        heappush(FEL,(currentTime + northSignals10[0]*1000, ['NorthSignalsLeft10', 'green']))      #Traffic lights shceduled
        return 'green'
    else:
        curr10LeftLight = 'green'
        heappush(FEL,(currentTime + northSignals10[1]*1000, ['NorthSignalsLeft10', 'red']))      #Traffic lights shceduled
        return 'red'

#Event - Switch 11th Street Lights
def switchEleventhLights(event):
    global curr11Light
    if (event[1][1] == 'red'):
        curr11Light = 'red'
        heappush(FEL,(currentTime + northSignals11[0]*1000, ['NorthSignals11', 'green']))      #Traffic lights shceduled
        return 'green'
    else:
        curr11Light = 'green'
        heappush(FEL,(currentTime + northSignals11[1]*1000, ['NorthSignals11', 'red']))      #Traffic lights shceduled
        return 'red'

#Event - Switch 12th Street Lights
def switchTwelfthLights(event):
    global curr12Light
    if (event[1][1] == 'red'):
        curr12Light = 'red'
        heappush(FEL,(currentTime + northSignals12[0]*1000, ['NorthSignals12', 'green']))      #Traffic lights shceduled
        return 'green'
    else:
        curr12Light = 'green'
        heappush(FEL,(currentTime + northSignals12[1]*1000, ['NorthSignals12', 'red']))      #Traffic lights shceduled
        return 'red'

#Event - Switch 12th Street Lights
def switchFourteenthLights(event):
    global curr14Light
    if (event[1][1] == 'red'):
        curr14Light = 'red'
        heappush(FEL,(currentTime + northSignals14[2]*1000, ['NorthSignals14', 'green']))      #Traffic lights shceduled
        return 'green'
    else:
        curr14Light = 'green'
        heappush(FEL,(currentTime + northSignals14[3]*1000, ['NorthSignals14', 'red']))      #Traffic lights shceduled
        return 'red'


#Event - Switch 12th Street Left Turn Lights
def switchFourteenthLeftLights(event):
    global curr14LeftLight
    if (event[1][1] == 'red'):
        curr14LeftLight = 'red'
        heappush(FEL,(currentTime + northSignals14[0]*1000, ['NorthSignalsLeft14', 'green']))      #Traffic lights shceduled
        return 'green'
    else:
        curr14LeftLight = 'green'
        heappush(FEL,(currentTime + northSignals14[1]*1000, ['NorthSignalsLeft14', 'red']))      #Traffic lights shceduled
        return 'red'

#Start Program
def main():
    #Initialize event list with first arrival
    getHistoricalEvents()
    #Start timer
    t0 = time.clock()
    wt0 = time.time()
    #Run Simulation
    runSimulation()
    #End Timer
    t1 = time.clock()
    wt1 = time.time()
    print('Mean of car travel times: ' + str(np.mean(carTravelTimes)/1000) + ' seconds')   #Divide by 1000 to convert to seconds
    print('Number of cars: ' + str(numCars))
    print('Number of Right Turns: ' + str(rightTurn))
    print('Number of Left Turns: ' + str(leftTurn))
    print('Cumulative wait time at 10th street: ' + str(tenDelay/1000) + ' seconds')
    print('Cumulative wait time at 11th street: ' + str(elevenDelay/1000) + ' seconds')
    print('Cumulative wait time at 12th street: ' + str(twelveDelay/1000) + ' seconds')
    print('Cumulative wait time at 14th street: ' + str(fourteenDelay/1000) + ' seconds')
    print('Cumulative wait time for left turn at 14th street: ' + str(fourteenLeftDelay/1000) + ' seconds')
    print('Cumulative wait time for left turn at 10th street: ' + str(tenLeftDelay/1000) + ' seconds')

#Our simulation engine
def runSimulation():
    global FEL
    global currentTime
    global START_TIME
    print('Events being processed')
    print('Simulation stats will appear after the list of events - please wait')
    while currentTime < START_TIME + 150000:
        next_item = heappop(FEL)                                #Get next event
        #print(next_item)
        currentTime = currentTime + (next_item[0] - currentTime) #Advance simulation time
        executeEvent(next_item)                                 #Update state variables and counters and generate future events


if __name__ == "__main__":
    main()

