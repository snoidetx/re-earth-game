"""Python Implementation"""

from math import sqrt, log, cos, pi
from random import random

# define constants

POP_MIN = 10
ECO_MAX = 2000
SEA_MAX = 1500
TECH_MAX = 40
FERT_BASE = 0.5
EQ_COEFT = 0.1
SEA_REC = 200
SEA_MIN = 600
popCapacity = 0
DOCK_POLL = 100
CITY_POLL = 200
FOREST_ECOB = 50
POWERP_ECOI = 200
beach_array = []  # coordinates along coast

# Declare variables used in class Tech

numTech = 0
numDock = 0
numFarm = 0
numPowerPlant = 0
numCity = 0
numForest = 0
resourceGain = 0
popCapacity = 0
techGain = 0
resourcePoints = 0

def main():
    array = initState()
    city1.apply([1, 1])
    while True:
        # 玩家操作 可以apply，可以conserve
        resetOnClickGain()
        array = updateArray(array)
        if checkState(array): # 如果checkstate return了任何东西，游戏都结束
            break         

def initState():
    # assign initial value
    global numTech
    global numDock
    global numFarm
    global numPowerPlant
    global numCity
    global numForest
    global resourceGain
    global resourcePoints
    global popCapacity
    global techPoints
    global techGain
    numTech = 0
    numDock = 0
    numFarm = 0
    numPowerPlant = 0
    numCity = 0
    numForest = 40
    resourceGain = 0
    popCapacity = 0
    techGain = 0
    year = 0
    population = 5000
    resourcePoints = 500
    techPoints = 0
    earthquakeLikelihood = 0
    seaPollution = 1000
    ecoImbalance = 0
    array = [population, resourcePoints, earthquakeLikelihood, seaPollution, ecoImbalance, year, techPoints]
    return array

def resetOnClickGain():
    global conservation
    global numClickDock
    global qnsAnswered
    conservation = 0
    numClickDock = 0
    qnsAnswered = 0

class Tech:
    """Generic tech"""
    def __init__(self, type="forest", level=1, techGen=0, resourceGen=0, price=500, numNeg=1, popCap=0):
        self.type = type
        self.level = level
        self.tech = techGen
        self.gain = resourceGen
        self.price = price
        self.popCap = popCap  # TODO change cityCap to popCap
        self.num = numNeg
    
    def apply(self, position):
        global year
        global numTech
        global numDock
        global numFarm
        global numPowerPlant
        global numCity
        global numForest
        global resourceGain
        global resourcePoints
        global popCapacity
        global techPoints
        global techGain
        if self.type == "dock" and position not in beach_array: # beach_array: an array of coordinates aside the sea
            print("error")
        else:
            resourcePoints -= self.price
            resourceGain += self.gain #TODO change to resourceGain
            popCapacity += self.popCap
            techGain += self.tech
            if self.type != "forest":
                numTech += 1
            elif self.type == "dock":
                numDock += self.num
            elif self.type == "powerplant":
                numPowerPlant += self.num
            elif (self.type == "city"):
                numCity += self.num
            elif self.type == "farm":
                numFarm += self.num

def checkState(array):
    if array[0] < POP_MIN:
        return "Simulation fails due to too low population."
    elif array[3] > SEA_MAX:
        return "Simulation fails due to too high sea pollution."
    elif array[4] > ECO_MAX:
        return "Simulation fails due to too great ecosystem Imbalance."
    elif array[0] > 50000 & array[1] >= 200:
        return "Simulation Success"
    else:
        pass
                      

city1 = Tech("city", level=1, techGen=5, resourceGen=-1000, price=1000, numNeg=1, popCap=6000)
city2 = Tech("city", level=2, techGen=7, resourceGen=-1200, price=1500, numNeg=1.2, popCap=8000) # may not be used in tutorial
city3 = Tech("city", level=3, techGen=9, resourceGen=-1300, price=2000, numNeg=1.3, popCap=12000) # may not be used in tutorial
powerplant1 = Tech("powerplant", level=1, techGen=0, resourceGen=1200, price=800)
powerplant2 = Tech("powerplant", level=2, techGen=0, resourceGen=3000, price=1500, numNeg=0.75) # may not be used in tutorial
powerplant3 = Tech("powerplant", level=3, techGen=0, resourceGen=10000, price=3000, numNeg=0.3) # may not be used in tutorial
dock1 = Tech("dock", level=1, techGen=0, resourceGen=1000, price=600, numNeg=1)
farm1 = Tech("farm", level=1, techGen=0, resourceGen=200, price=200, numNeg=1, popCap=1000) # 0 tech, unlocked when initialized

def randomDisaster(p, n):
    """harvest every round"""
    if 0 < p < 1:
        mean = n * p
        variance = n * p * (1-p)
        stddev = sqrt(variance)
        u1 = random()
        u2 = random()
        z0 = sqrt(-2 * log(u1)) * cos(2*pi*u2)
        return z0 * stddev + mean
    elif p <= 0:
        return 0
    else:
        return n

def updateArray(array):
    # update per round
    population_old = array[0]
    seaPollution_old = array[3]
    earthquakeLikelihood = (numPowerPlant + numFarm - numForest + numCity) * EQ_COEFT # aka when numPowerPlant + numFarm - numForest + numCity >= 1/EQ_COEFT, the game will terminate next round
    pop_new = (FERT_BASE + numTech / TECH_MAX - seaPollution_old / SEA_MAX + (popCapacity - population_old)/popCapacity) + population_old - randomDisaster(earthquakeLikelihood, population_old)
    ecoImbalance_old = array[4]
    seaPollution_new = (seaPollution_old + DOCK_POLL * numClickDock + CITY_POLL * numCity) * 1.01 - SEA_REC - conservation
    # dock 是码头 city是城镇 每回合码头和城镇都会对海洋产生污染 每回合海洋自己可以修复200, if nothing is done, terminate in 5 rounds
    if seaPollution_new < SEA_MIN:
        seaPollution_new = SEA_MIN
    ecoImbalance_new = ecoImbalance_old + CITY_POLL * numCity + POWERP_ECOI * numPowerPlant - FOREST_ECOB * numForest - conservation

    global techPoints
    techPoints += techGain + qnsAnswered

    global resourcePoints
    resourcePoints += resourceGain

    year = array[1]
    year += 10 
    techPoints_new = array[5] + techGain + qnsAnswered
    return [pop_new,year, earthquakeLikelihood, seaPollution_new, ecoImbalance_new]

# 这里也需要function
def clickDock():
    # click 
    global numClickDock
    global resourcePoints
    numClickDock += 1
    resourcePoints += 1000

def answerQns():
    """an onclick action"""
    # click
    global qnsAnswered
    qnsAnswered += 1

# TODO 需要写一个function，玩家click一次减resource points 改善环境
def conserve():
    """an onclick action"""
    # click
    global resourcePoints
    global conservation
    resourcePoints -=500
    conservation = 100

main()

# for debugging in Python only

numClickDock = 0
conservation = 0
qnsAnswered = 0