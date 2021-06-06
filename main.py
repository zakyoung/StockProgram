import yfinance as yf
import csv
class Stock:
  def __init__(self,ticker):
    self.ticker = ticker
    self.yfData = yf.Ticker(ticker)
  def __str__(self):
    return self.ticker
  __repr__ = __str__
  @property
  def sector(self):
    return self.yfData.info['sector']
  @property
  def payoutRatio(self):
    try:
      return self.yfData.info['payoutRatio'] * 100
    except:
      return 'Stock does not pay a dividend'
  @property
  def priceToBook(self):
    return self.yfData.info['priceToBook']
  @property
  def marketCap(self):
    return self.yfData.info['marketCap']
  @property
  def currentDividendRate(self):
    return self.yfData.info['dividendRate']
  @property
  def priorYearDividendRate(self):
    return self.yfData.info['trailingAnnualDividendRate']
  @property
  def DividendGrowthRate(self):
    try:
      return ((self.currentDividendRate-self.priorYearDividendRate)/self.priorYearDividendRate) * 100
    except:
      return "Calculation not possible"
  @property
  def fiveYearAvgDividendRate(self):
    return self.yfData.info['fiveYearAvgDividendRate']
  @property
  def fiftyTwoWeekHigh(self):
    return self.yfData.info['fiftyTwoWeekHigh']
  @property
  def fiftyTwoWeekLow(self):
    return self.yfData.info['fiftyTwoWeekLow']
  @property
  def previousClose(self):
    return self.yfData.info['previousClose']
  @property
  def trailingPeRatio(self):
    return self.yfData.info['trailingPE']
  @property
  def forwardPeRatio(self):
    return self.yfData.info['forwardPE']
  @property
  def fourYearEarnings(self):
    try:
      return dict(self.yfData.earnings['Earnings'])
    except:
      return None
  @property
  def fourYearRevenue(self):
    try:
      return dict(self.yfData.earnings['Revenue'])
    except:
      return None
  @property
  def currentRatio(self):
    """
    This is the MRQ current ratio and since the yfData dict doesnt have a key for current ratio 
    we must Calculate it using Total current assets / Total current Liabilities
    """
    stockData = self.yfData
    needed_data = dict(stockData.balance_sheet[list(stockData.balance_sheet)[0]])
    try:
      current_ratio = needed_data['Total Current Assets']/needed_data['Total Current Liabilities']
      return current_ratio
    except:
      return None
  @property
  def operatingCashflow(self):
    stockData = self.yfData
    try:
      return stockData.cashflow[list(stockData.cashflow)[0]]["Total Cash From Operating Activities"]
    except:
      return None
  @property
  def returnOnAssets(self):
    """
    For return on assets we use the equation earnings/total Assets 
    """
    stockData = self.yfData
    try:
      mostRecentYear = list(self.fourYearEarnings.keys())[-1]
      earnings = self.fourYearEarnings[mostRecentYear]
      totalAssets = dict(stockData.balance_sheet[list(stockData.balance_sheet)[0]])['Total Assets']
      return (earnings/totalAssets)*100
    except:
      return None
  @property
  def interestCoverageRatio(self):
    stockData = self.yfData
    try:
      dataDictinary = dict(stockData.financials[list(stockData.financials)[0]])
      print(dataDictinary)
      ebit = dataDictinary['Ebit']
      interestExpense = dataDictinary['Interest Expense']
      if interestExpense != 0:
        print(ebit)
        print(interestExpense)
        return abs(ebit/interestExpense)
      else:
        return "No interest expense"
    except:
      return None
def run():
  with open('NYSE.csv','r') as nyse, open('NASDAQ.csv','r') as nasdaq:
    nyseReader = csv.DictReader(nyse)
    nasdaqReader = csv.DictReader(nasdaq)
    allStocks = sorted([stock['Ticker'] for stock in nyseReader] + [stock['Symbol'] for stock in nasdaqReader])
if __name__ == "__main__":
  run()