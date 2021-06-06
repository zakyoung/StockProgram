import yfinance as yf
import csv
with open('NYSE.csv','r') as nyse, open('NASDAQ.csv','r') as nasdaq:
  nyseReader = csv.DictReader(nyse)
  for stock in nyseReader:
    stock = stock['Ticker']
    stockData = yf.Ticker(f"{stock}")
    print(stockData.cashflow[list(stockData.cashflow)[0]]["Total Cash From Operating Activities"])
    print(stock)