import numpy as np
import matplotlib.pyplot as plt



# global variables 
NUMBEROFDAYS = 50

INITIALPRICE = 100  # Initial stock price
DRIFT = 0.000456       # Drift term
VOLATILITY = 0.0087  # Volatility term
NUMBEROFSIMULATIONS = 5  # Number of simulations

DT = 1/24


def GenerateStocks(initialPrice, drift, volatility, numDays, dT):
    '''
    This function simulates a stock using geometric brownian motion. 

    dT will be given in fraction of day -> updating every hour 
    '''

    lengthStock = int( 1/dT * numDays ) 


    stockEvolution = np.zeros(lengthStock)

    stockEvolution[0] = initialPrice

    # iterate over stock 
    for i in range(1, lengthStock):
        tempValue = ( drift - volatility**2 / 2 ) * dT + volatility * np.random.normal(0, np.sqrt(dT))
        tempPrice = stockEvolution[i-1] * np.exp(tempValue)
        stockEvolution[i] = tempPrice

    return stockEvolution


def ShowSomeStocks(numberOfStocks):

    plt.figure(figsize=(10, 6))
    for i in range(numberOfStocks):
        prices = GenerateStocks(INITIALPRICE, DRIFT, VOLATILITY, NUMBEROFDAYS, DT)
        plt.plot(prices, label = 'Stock No. ' + str(i))

    plt.title('Stocks simulated using GBM, Drift = ' + str(DRIFT) + ' Volatility = ' +str(VOLATILITY))
    plt.xlabel('Time [h]')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

# ShowSomeStocks(NUMBEROFSIMULATIONS)



def CalculateMovingAverage(stock, dayNo, dT, daysConsidered, onlyClosingPrices): 
    '''
    This function calculates the average in a stock for day dayNo over the last daysConsidered days. 
    '''
    if dayNo < daysConsidered: 
        return None

    numDays = len(stock) * dT

    stepsPerDay = int(len(stock) / numDays)

    # average over closing prices 
    partOfArray = stock[int( (dayNo - daysConsidered) * stepsPerDay) : int(dayNo * stepsPerDay)]

    # calculate average over every stepsperday-th element 
    if onlyClosingPrices: 
        avg = np.mean(partOfArray[:: stepsPerDay ])
    else: 
        # just take into account the whole array for the last few days 
        avg = np.mean(partOfArray)

    return avg



def CalculateZScore(stock, dayNo, dT, daysConsidered): 
    '''
    Z score over 1.5 indicates overvalued -> sell
    Z score under -1.5 indicates undervalued -> buy 
    '''

    if dayNo < daysConsidered+1: 
        return None

    mean = CalculateMovingAverage(stock, dayNo, dT, daysConsidered, False)

    numDays = len(stock) * dT

    stepsPerDay = int(len(stock) / numDays)

    partOfArray = stock[int( (dayNo - daysConsidered) * stepsPerDay) : int(dayNo * stepsPerDay)]

    deviation = partOfArray[-1] - mean 

    std = np.std(partOfArray)

    zScore = deviation / std

    return zScore





'''
PLOTTING
'''


def ShowStock(stock, showZ, dayRangeZ, showMA, dayRangeList, numberOfDays, dT, title):

    plt.plot(stock)
    daysList = np.arange(numberOfDays) * 1/dT



    if showMA: 



        for element in dayRangeList: 
            averageList10 = []
            averageList5 = []

            for i in range(numberOfDays):
                averageList10.append(CalculateMovingAverage(stock, i, dT, element, False))
                averageList5.append(CalculateMovingAverage(stock, i, dT, element, False))


            plt.plot(daysList, averageList10, label = 'Moving Average, ' + str(element))
        
        plt.xlim((element * 1/dT, daysList[-1]))

    # plt.scatter(np.where(stock == buyList[0]), buyList[0], color = 'orange', label = 'Buy')
    # plt.scatter(sellListIndices[0], stock[sellListIndices[0]], color = 'black', label = 'Sell')
    plt.title(title)
    plt.xlabel('Time [h]')
    plt.ylabel('Price')
    
    plt.legend()
    plt.show()

    if showZ: 

        zScoreList = []

        for i in range(numberOfDays):

            zScoreList.append(CalculateZScore(stock, i, dT, dayRangeZ))

        # plot Z value 
        plt.plot(daysList, zScoreList, label = 'Z-Score, ' + str(dayRangeZ))
        plt.title('Evolution of the Z-Value')
        plt.xlabel('Time [h]')
        plt.ylabel('Z-Value')
        plt.legend()
        plt.show()



# DAYSCONSIDERED = 5


# averageList = []
# zScoreList = []
# daysList = np.arange(NUMBEROFDAYS) * 1/DT

# for i in range(NUMBEROFDAYS):

#     zScoreList.append(CalculateZScore(stock, i, DT, DAYSCONSIDERED))
#     averageList.append(CalculateMovingAverage(stock, i, DT, DAYSCONSIDERED, True))


# plt.plot(daysList, averageList, label = 'Moving Average, ' + str(DAYSCONSIDERED))

# print(type(averageList), type(zScoreList))


# plt.plot(daysList, zScoreList, label = 'Z-Score')
# plt.title('Stock Price Simulation, Moving Average')
# plt.xlabel('Hours')
# plt.ylabel('Stock Price')
# plt.legend()
# # plt.show()


# plt.show()
