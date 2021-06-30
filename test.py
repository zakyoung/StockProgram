import yfinance as yf
stockData = yf.Ticker('INTC')
print(dict(stockData.balance_sheet[list(stockData.balance_sheet)[0]])['Total Stockholder Equity'])