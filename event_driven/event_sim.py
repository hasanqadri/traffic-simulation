from __future__ import division
from heapq import heappush, heappop
import time

#Graphing and Analysis imports
import numpy as np
import math
import random

#Reading JSON file imports (Converted CSV to JSON in preprocessing)
import json
import scipy.stats

#Initializing simulation
FEL = [];

#GLT, RLT, GTR, RTR/LT
#Below are street light lengths for each street
northSignals10 = [10.6, 2.2, 38.1, 49.3];
northSignals14 = [12.4, 3.6, 37.8, 45.3];
#GTR, RTR/LT
northSignals11 = [44.7, 55.4];
northSignals12 = [64.1, 35.7];
#13th street has no lights!

START_TIME = 1163030800;
currentTime = START_TIME;

carTravelTimes = [];
carTravelTimes10 = [];
carTravelTimes11 = [];
carTravelTimes12 = [];
carTravelTimes14 = [];
arrivalTimes = [];
leftTurnChance = 0;
rightTurnChance = 0;
rightTurn = 0;
leftTurn = 0;

#Queue initializations and system states. Segments are named after the preceding intersection
curr10Light = 'green'
curr10LeftLight = 'green';
tenLeftDelay = 0;
tenDelay = 0;

curr11Light = 'green'
elevenDelay = 0;

curr12Light = 'green'
twelveDelay = 0;

curr14Light = 'green'
curr14LeftLight = 'green';
fourteenDelay = 0;
fourteenLeftDelay = 0;

events = {}
numCars = 1;
numCarsWarmup = 1;
numEvents = 0;

warmedUp = False;
currMavg = [];
mAvgTotal = [];
# Populates our event list with inital events.
# There is a chance our simulation is short-lived or very long depending on these initial events
def getHistoricalEvents():
    global events
    global leftTurnChance
    global rightTurnChance
    events = {}

    with open('../data/trajectories0.json') as json_data:   #Sample of total data
        events = json.load(json_data)
    '''
    with open('../data/trajectories1.json') as json_data:
        events.update(json.load(json_data))
    '''
    numEvents = len(events.keys())
    heappush(FEL,(currentTime + northSignals10[3], ['NorthSignals10', 'red']))      #Traffic lights shceduled
    heappush(FEL,(currentTime + northSignals11[1], ['NorthSignals11', 'red']))
    heappush(FEL,(currentTime + northSignals12[1], ['NorthSignals12', 'red']))
    heappush(FEL,(currentTime + northSignals14[3], ['NorthSignals14', 'red']))
    heappush(FEL,(currentTime + northSignals10[1], ['NorthSignalsLeft10', 'red']))    #Traffic left-turn lights scheduled
    heappush(FEL,(currentTime + northSignals14[3], ['NorthSignalsLeft14', 'red']))
    arrivalTime = getInterArrivalTime()
    leftTurnChance = getLeftTurnChance();
    rightTurnChance = getRightTurnChance();
    heappush(FEL,(arrivalTime, ['NinthSegment', leftTurnChance, rightTurnChance, arrivalTime]))  #First car event that is scheduled
    return FEL;

# Randomly generated interarrival time from empirical distribution which is used for initial car creation
def getInterArrivalTime():
    global numEvents
    global arrivalTimes
    #Interarrival times
    interArrivalTimes = [0]
    for n in range(len(events.keys())):
        interArrivalTimes.append(0)
    for z in range(len(events.keys())):
        interArrivalTimes[z] = events[str(z)]['Epoch_ms'] - START_TIME;
    i = random.randint(0, len(events.keys()))
    if (interArrivalTimes[i] < currentTime):
        arrivalTimes.append(interArrivalTimes[i])
        return abs(interArrivalTimes[i] - currentTime) + interArrivalTimes[i] + 5000
    arrivalTimes.append(interArrivalTimes[i])
    return interArrivalTimes[i];

#Calculate chance for left turn for cars at any given intersection
def getRightTurnChance():
    #Left turns
    intersectionCounter = 0;
    leftTurnCounter = 0;
    for z in range(len(events.keys())):
        if (events[str(z)]['Intersection'] != 0):
            intersectionCounter = intersectionCounter + 1
            if (events[str(z)]['Movement'] == 2):
                leftTurnCounter = leftTurnCounter + 1
    leftTurnChance = leftTurnCounter / intersectionCounter;
    return leftTurnChance

#Calculate chance for right turn for cars at any given itnersection
def getLeftTurnChance():
    #Left turns
    intersectionCounter = 0;
    rightTurnCounter = 0;
    for z in range(len(events.keys())):
        if (events[str(z)]['Intersection'] != 0):
            intersectionCounter = intersectionCounter + 1
            if (events[str(z)]['Movement'] == 3):
                rightTurnCounter = rightTurnCounter + 1
    rightTurnChance = rightTurnCounter / intersectionCounter;
    return rightTurnChance;

#Execute the event and schedule the next events
# Main event scheduler
def executeEvent(event):
    global numCars;
    global numCarsWarmup
    global warmedUp
    if (numCarsWarmup == 15):
        warmedUp = True
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
        if (warmedUp):
            numCars = numCars + 1
        numCarsWarmup = numCarsWarmup + 1
        arrivalTime = getInterArrivalTime()
        heappush(FEL,(arrivalTime, ['NinthSegment', leftTurnChance, rightTurnChance, arrivalTime]))
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
        twelfthIntersection(event);
    elif (event[1][0] == 'TwelfthSegment'):
        twelfthSegment(event)
    elif (event[1][0] == 'FourteenthIntersection'):
        fourteenthIntersection(event);
    elif (event[1][0] == 'FourteenthSegment'):
        fourteenthSegment(event)


# Event - Entering segment before 10th intersection
# Determines if car takes left or right turn at next intersection and schedules that event.
def ninthSegment(event):
    turnResult = checkLeftRightTurn(event);
    if (turnResult == 1):
        heappush(FEL,(event[0] + 10, ['TenthIntersection', event[1][1], event[1][2], event[1][3], 1]))
        return 1;
    elif (turnResult == 2):
        heappush(FEL,(event[0] + 10, ['TenthIntersection', event[1][1], event[1][2], event[1][3], 2]))
        return 2;
    else:
        heappush(FEL,(event[0]+ 10, ['TenthIntersection', event[1][1], event[1][2], event[1][3], 0]))
        return 0;

#Event - Entering 10th intersection
# Car takes left turn or goes straight if light if green. It takes a right turn even if light is red.
# If light is red, then cars wanting to go straight or left wait for a green.
# Returns time delayed (if any)
def tenthIntersection(event):
    global tenDelay;
    global tenLeftDelay;
    global leftTurn;
    global rightTurn;
    if (event[1][4] == 2):
        if (curr10LeftLight == 'green'):
            if (warmedUp):
                leftTurn = leftTurn + 1
                carTravelTimes10.append(event[0] - event[1][3])
        else:
            heappush(FEL,(event[0] + 10, ['TenthIntersection', event[1][1], event[1][2], event[1][3], 2]))
            tenLeftDelay = tenLeftDelay + 10;
            return tenLeftDelay;
    elif (event[1][4] == 1):
        if (warmedUp):
            rightTurn = rightTurn + 1;
            carTravelTimes10.append(event[0] - event[1][3])
    else:
        if (curr10Light == 'green'):
            heappush(FEL,(event[0] + 13, ['TenthSegment', event[1][1], event[1][2], event[1][3], 0]))
        else:
            heappush(FEL,(event[0] + 10, ['TenthIntersection', event[1][1], event[1][2], event[1][3], 0]))
            tenDelay = tenDelay + 10
            return tenDelay;
    return 0;


# Event - Entering 10th Segment
# Determines if car takes right turn at next intersection and schedules that event if so. Otherwise schedules going straight.
# Returns whether a turn was taken (1 == left and 0 == straight)
def tenthSegment(event):
    turnResult = checkLeftRightTurn(event);
    if (turnResult == 1):
        heappush(FEL,(event[0] + 10, ['EleventhIntersection', event[1][1], event[1][2], event[1][3], 1]))
        return 1;
    else:
        heappush(FEL,(event[0]+ 12, ['EleventhIntersection', event[1][1], event[1][2], event[1][3], 0]))
        return 0;

# Event - Entering 11th intersection
# Car goes straight if light is green. It takes a right turn even if light is red.
# Returns time delayed (if at all)
def eleventhIntersection(event):
    global elevenDelay;
    global leftTurn;
    global rightTurn;
    if (event[1][4] == 1):
        if (warmedUp):
            rightTurn = rightTurn + 1;
            carTravelTimes11.append(event[0] - event[1][3])
    else:
        if (curr11Light == 'green'):
            heappush(FEL,(event[0] + 7, ['EleventhSegment', event[1][1], event[1][2], event[1][3], 0]))
        else:
            heappush(FEL,(event[0] + 10, ['EleventhIntersection', event[1][1], event[1][2], event[1][3], 0]))
            elevenDelay = elevenDelay + 10
            return elevenDelay;
    return 0;


# Event - Entering 11th segment
# Determines if car takes right turn at next intersection and schedules that event. Otherwise schedules going straight.
def eleventhSegment(event):
    turnResult = checkLeftRightTurn(event);
    if (turnResult == 1):
        heappush(FEL,(event[0] + 10, ['TwelfthIntersection', event[1][1], event[1][2], event[1][3], 1]))
        return 1;
    else:
        heappush(FEL,(event[0]+ 10, ['TwelfthIntersection', event[1][1], event[1][2], event[1][3], 0]))
        return 0;


# Event - Entering 12th intersection
# Car goes straight if light is green. It takes a right turn even if light is red.
def twelfthIntersection(event):
    global twelveDelay;
    global leftTurn;
    global rightTurn;
    if (event[1][4] == 1):
        if (warmedUp):
            rightTurn = rightTurn + 1;
            carTravelTimes12.append(event[0] - event[1][3])
    else:
        if (curr12Light == 'green'):
            heappush(FEL,(event[0] + 5, ['TwelfthSegment', event[1][1], event[1][2], event[1][3], 0]))
        else:
            heappush(FEL,(event[0] + 10, ['TwelfthIntersection', event[1][1], event[1][2], event[1][3], 0]))
            twelveDelay = twelveDelay + 10
            return twelveDelay;
    return 0;


# Event - Entering 12th segment
# Determines if car takes left or right turn at next intersection and schedules that event. Otherwise schedules going straight.
def twelfthSegment(event):
    turnResult = checkLeftRightTurn(event);
    if (turnResult == 1):
        heappush(FEL,(event[0] + 10, ['FourteenthIntersection', event[1][1], event[1][2], event[1][3], 1]))
        return 1;
    elif (turnResult == 2):
        heappush(FEL,(event[0] + 10, ['FourteenthIntersection', event[1][1], event[1][2], event[1][3], 2]))
        return 2;
    else:
        heappush(FEL,(event[0]+ 10, ['FourteenthIntersection', event[1][1], event[1][2], event[1][3], 0]))
        return 0;

# Event - Entering 14th intersection
# Car takes left turn or goes straight if light if green. It takes a right turn even if light is red.
# If light is red, then cars wanting to go straight or left wait for a green.
def fourteenthIntersection(event):
    global fourteenDelay;
    global fourteenLeftDelay;
    global leftTurn;
    global rightTurn;
    if (event[1][4] == 2):
        if (curr14LeftLight == 'green'):
            if (warmedUp):
                leftTurn = leftTurn + 1
                carTravelTimes14.append(event[0] - event[1][3])
        else:
            heappush(FEL,(event[0] + 10, ['FourteenthIntersection', event[1][1], event[1][2], event[1][3], 2]))
            fourteenLeftDelay = fourteenLeftDelay + 10;
            return fourteenLeftDelay;
    elif (event[1][4] == 1):
        if (warmedUp):
            rightTurn = rightTurn + 1;
            carTravelTimes14.append(event[0] - event[1][3])
    else:
        if (curr14Light == 'green'):
            heappush(FEL,(event[0] + 5, ['FourteenthSegment', event[1][1], event[1][2], event[1][3], 0]))
        else:
            heappush(FEL,(event[0] + 10, ['FourteenthIntersection', event[1][1], event[1][2], event[1][3], 0]))
            fourteenDelay = fourteenDelay + 10
            return fourteenDelay;
    return 0;


# Event - Entering 14th segment
# Cars leave sim and we update stats
def fourteenthSegment(event):
    if (warmedUp):
        carTravelTimes.append(event[0] - event[1][3])

#Determine if car is going to take a left or right at a particular intersection
def checkLeftRightTurn(event):
    u = random.randint(100, 1000)/1000;
    if (u < rightTurnChance):
        return 1;
    u = random.randint(100, 1000)/1000;
    if (u < leftTurnChance + .2): #Added .2 for testing purposes here, the generated left turn chance was too small otherwise
        return 2;
    return 0;

#Event - Switch 10th Street Lights
#Returns next scheduled light color
def switchTenthLights(event):
    global curr10Light;
    if (event[1][1] == 'red'):
        curr10Light = 'red';
        heappush(FEL,(currentTime + northSignals10[2], ['NorthSignals10', 'green']))      #Traffic lights shceduled
        return 'green';
    else:
        curr10Light = 'green';
        heappush(FEL,(currentTime + northSignals10[3], ['NorthSignals10', 'red']))      #Traffic lights shceduled
        return 'red';

#Event - Switch 10th Street Left Turn Lights
def switchTenthLeftLights(event):
    global curr10LeftLight;
    if (event[1][1] == 'red'):
        curr10LeftLight = 'red';
        heappush(FEL,(currentTime + northSignals10[0], ['NorthSignalsLeft10', 'green']))      #Traffic lights shceduled
        return 'green';
    else:
        curr10LeftLight = 'green';
        heappush(FEL,(currentTime + northSignals10[1], ['NorthSignalsLeft10', 'red']))      #Traffic lights shceduled
        return 'red';

#Event - Switch 11th Street Lights
def switchEleventhLights(event):
    global curr11Light
    if (event[1][1] == 'red'):
        curr11Light = 'red';
        heappush(FEL,(currentTime + northSignals11[0], ['NorthSignals11', 'green']))      #Traffic lights shceduled
        return 'green';
    else:
        curr11Light = 'green';
        heappush(FEL,(currentTime + northSignals11[1], ['NorthSignals11', 'red']))      #Traffic lights shceduled
        return 'red';

#Event - Switch 12th Street Lights
def switchTwelfthLights(event):
    global curr12Light
    if (event[1][1] == 'red'):
        curr12Light = 'red';
        heappush(FEL,(currentTime + northSignals12[0], ['NorthSignals12', 'green']))      #Traffic lights shceduled
        return 'green';
    else:
        curr12Light = 'green';
        heappush(FEL,(currentTime + northSignals12[1], ['NorthSignals12', 'red']))      #Traffic lights shceduled
        return 'red';

#Event - Switch 12th Street Lights
def switchFourteenthLights(event):
    global curr14Light
    if (event[1][1] == 'red'):
        curr14Light = 'red';
        heappush(FEL,(currentTime + northSignals14[2], ['NorthSignals14', 'green']))      #Traffic lights shceduled
        return 'green';
    else:
        curr14Light = 'green';
        heappush(FEL,(currentTime + northSignals14[3], ['NorthSignals14', 'red']))      #Traffic lights shceduled
        return 'red';


#Event - Switch 12th Street Left Turn Lights
def switchFourteenthLeftLights(event):
    global curr14LeftLight
    if (event[1][1] == 'red'):
        curr14LeftLight = 'red';
        heappush(FEL,(currentTime + northSignals14[0], ['NorthSignalsLeft14', 'green']))      #Traffic lights shceduled
        return 'green';
    else:
        curr14LeftLight = 'green';
        heappush(FEL,(currentTime + northSignals14[1], ['NorthSignalsLeft14', 'red']))      #Traffic lights shceduled
        return 'red';

#--------------------- Helper Methods ----------------------
def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return (m-h, m+h)


def compute_mavg(travel_times):
    mavg = []
    N = len(travel_times)
    for i in range(1, N):
        mavg.append(np.mean(travel_times[:i]))

    return mavg


# ----------------- End Helper Methods ---------------------
#Start Program
def main():
    global warmedUp
    #Initialize event list with first arrival
    getHistoricalEvents();
    #Start timer
    t0 = time.time();
    wt0 = time.time();
    y = 0;

    numIterations = 1
    #Run Simulation
    while y < numIterations:
        getHistoricalEvents();
        runSimulation();
        # print(y)
        warmedUp = False;
        numCarsWarmup = 0;
        y = y + 1
    #End Timer
    t1 = time.time();
    wt1 = time.time();
    print("Runtime: " + str(t1 - t0) + " seconds")
    print('Size of carTravelTimes: ' + str(len(carTravelTimes)))
    print('Mean travel times: ' + str(np.mean(carTravelTimes)) + ' seconds')
    print('Stdev travel times: ' + str(np.std(carTravelTimes)) + ' seconds')
    print('Mean travel time 95% Confidence Interval: ' + str(mean_confidence_interval(carTravelTimes)) + ' seconds')

#Our simulation engine
def runSimulation():
    global FEL;
    global currentTime;
    global START_TIME

    while currentTime < START_TIME + 1E6:
        next_item = heappop(FEL);                                #Get next event
        #print(next_item)
        currentTime = next_item[0]  #Advance simulation time
        executeEvent(next_item)     #Update state variables and counters and generate future events
    currentTime = START_TIME;
    FEL = [];


if __name__ == "__main__":
    SEED = 42
    np.random.seed(SEED)
    random.seed(SEED)
    main()
