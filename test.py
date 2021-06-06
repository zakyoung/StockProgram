import yfinance as yf
import csv
with open('NYSE.csv','r') as nyse, open('NASDAQ.csv','r') as nasdaq:
  nyseReader = ['aapl']
  for stock in nyseReader:
    stockData = yf.Ticker(f"{stock}")
    print(dict(stockData.financials[list(stockData.financials)[0]]))