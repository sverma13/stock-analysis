import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.stats import skew
from scipy.stats import kurtosis

import sqlite3
from sqlite3 import Error

def createConnection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error:
        print(Error)
    return conn

def sqlConnect():
    try:
        conn = sqlite3.connect(":memory:")
        print("Connection is established: Database is created in memory")
    except Error:
        print(Error)
    return conn

def sqlInsert(conn, entities):
    cursor = con.cursor()
    cursor.execute("INSERT INTO stocks(ticker, avg_annual_return, annual_volatility, skew, kurtosis) VALUES(?,?,?,?,?)", entities)
    con.commit()

con = createConnection("mydatabase.db")
cursor = con.cursor()
sqlConnect()
cursor.execute("CREATE TABLE stocks(ticker text PRIMARY KEY, avg_annual_return real, annual_volatility real, skew real, kurtosis real)")
con.commit()

stockPort = ['AAPL', 'AMZN', 'FB', 'GE', 'JPM', 'MSFT', 'TSLA', 'V']

def stockAnalysis(ticker):
    tickerFile = ticker + ".csv"
    data = pd.read_csv(tickerFile, parse_dates=['Date'])
    data = data.sort_values(by='Date')
    data.set_index('Date', inplace=True)

    data["Returns"] = data["Adj Close"].pct_change()
    returns = data["Returns"].dropna()

    avgDailyReturn = np.mean(returns)
    avgAnnualReturn = ((1 + avgDailyReturn)**252)-1
    stdDev = np.std(returns)
    #variance = stdDev **2
    annualVolatility = stdDev * np.sqrt(252)
    stockSkew = skew(returns)
    stockKurtosis = kurtosis(returns)

    dataEntry = (ticker, avgAnnualReturn, annualVolatility, stockSkew, stockKurtosis)

    return dataEntry

for stock in stockPort:
    stockData = stockAnalysis(stock)
    sqlInsert(con, stockData)

cursor.execute("SELECT * FROM stocks")
rows = cursor.fetchall()
for row in rows:
    print(row)