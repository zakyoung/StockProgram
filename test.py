import yfinance as yf
import csv
with open('NYSE.csv','r') as nyse, open('NASDAQ.csv','r') as nasdaq:
  nyseReader = csv.DictReader(nyse)
  nasdaqReader = csv.DictReader(nasdaq)
  sectorSet = set()
  stocks = [stock['Ticker'] for stock in nyseReader] + [stock['Symbol'] for stock in nasdaqReader]
  for stock in stocks:
    print(stock)
    try:
      stockData = yf.Ticker(f"{stock}")
      sectorSet.add(stockData.info['industry'])
    except:
      continue
  print(sectorSet)
  with open('allSectors.txt','w') as writer:
    for sector in sectorSet:
      writer.write(sector)