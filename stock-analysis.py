# Data analysis libraries
import pandas as pd
import numpy as np

# Statistical analysis libraries
from scipy import stats
from scipy.stats import skew
from scipy.stats import kurtosis

# SQLite capability libraries
import sqlite3
from sqlite3 import Error


# Function: create connection to SQLite database
def createConnection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error:
        print(Error)
    return conn

# Function: connect to SQLite database
def sqlConnect():
    try:
        conn = sqlite3.connect(':memory:')
        print('Connection is established: Database is created in memory')
    except Error:
        print(Error)
    return conn

# Function: insert a row of historical stock data in the SQLite table
def sqlInsert(conn, entities):
    cursor = con.cursor()
    cursor.execute('INSERT INTO stocks(ticker, avg_annual_return, annual_volatility, skew, kurtosis) VALUES(?,?,?,?,?)', entities)
    con.commit()

# Connect to the SQLite database
con = createConnection('mydatabase.db')
cursor = con.cursor()
sqlConnect()

# Create SQLite table
cursor.execute('CREATE TABLE stocks(ticker text PRIMARY KEY, avg_annual_return real, annual_volatility real, skew real, kurtosis real)')
con.commit()

# Names of stock tickers in portfolio
stockPort = ['AAPL', 'AMZN', 'FB', 'GE', 'JPM', 'MSFT', 'TSLA', 'V']

def stockAnalysis(ticker):
    tickerFile = ticker + '.csv'
    data = pd.read_csv(tickerFile, parse_dates=['Date']) #import historical data in pandas dataframe
    data = data.sort_values(by='Date')
    data.set_index('Date', inplace=True)

    data['Returns'] = data['Adj Close'].pct_change() #create a column of daily returns
    returns = data['Returns'].dropna() #remove entries with N/A data

    # Statistical stock data based on daily returns
    avgDailyReturn = np.mean(returns)
    avgAnnualReturn = ((1 + avgDailyReturn)**252)-1
    stdDev = np.std(returns)
    annualVolatility = stdDev * np.sqrt(252)
    stockSkew = skew(returns)
    stockKurtosis = kurtosis(returns)

    # Stock data to be inserted into database table
    dataEntry = (ticker, avgAnnualReturn, annualVolatility, stockSkew, stockKurtosis)

    return dataEntry

# For every stock ticker in portfolio, perform stock analysis and load the results in the SQLite table
for stock in stockPort:
    stockData = stockAnalysis(stock)
    sqlInsert(con, stockData)

# Print all rows in the SQLite table
cursor.execute('SELECT * FROM stocks')
rows = cursor.fetchall()
for row in rows:
    print(row)
