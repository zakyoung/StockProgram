import yfinance as yf
data = yf.Ticker('AAPL')
print(data.info['dividendYield'])