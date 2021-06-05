import yfinance as yf
import csv
with open('NYSE.csv','r') as nyse, open('NASDAQ.csv','r') as nasdaq:
  nyseReader = csv.DictReader(nyse)
  for stock in nyseReader:
    stock = stock['Ticker']
    stockData = yf.Ticker(f"{stock}")
    needed_data = dict(stockData.balance_sheet[list(stockData.balance_sheet)[0]])
    try:
      current_ratio = needed_data['Total Current Assets']/needed_data['Total Current Liabilities']
    except:
      print('None')