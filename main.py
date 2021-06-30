import yfinance as yf
import csv
class Stock:
  def __init__(self,ticker):
    self.ticker = ticker
    self.yfData = yf.Ticker(ticker)
    self.__points = None
  def getPoints(self):
    return self.__points

  def setPoints(self,points):
    self.__points = points

  def __str__(self):
    return f"{self.ticker.upper()} ({self.industry})"

  __repr__ = __str__

  @property
  def industry(self):
    try:
      return self.yfData.info['industry']
    except:
      return None

  @property
  def payoutRatio(self):
    try:
      return self.yfData.info['payoutRatio'] * 100
    except:
      return None

  @property
  def priceToBook(self):
    try:
      return self.yfData.info['priceToBook']
    except:
      return None

  @property
  def marketCap(self):
    try:
      return self.yfData.info['marketCap']
    except:
      return None

  @property
  def currentDividendRate(self):
    try:
      return self.yfData.info['dividendRate']
    except:
      return None

  @property
  def priorYearDividendRate(self):
    try:
      return self.yfData.info['trailingAnnualDividendRate']
    except:
      return None

  @property
  def DividendGrowthRate(self):
    try:
      return ((self.currentDividendRate-self.priorYearDividendRate)/self.priorYearDividendRate) * 100
    except:
      return None

  @property
  def fiveYearAvgDividendYield(self):
    try:
      return self.yfData.info['fiveYearAvgDividendYield']
    except:
      return None

  @property
  def fiftyTwoWeekHigh(self):
    try:
      return self.yfData.info['fiftyTwoWeekHigh']
    except:
      return None

  @property
  def fiftyTwoWeekLow(self):
    try:
      return self.yfData.info['fiftyTwoWeekLow']
    except:
      return None

  @property
  def previousClose(self):
    try:
      return self.yfData.info['previousClose']
    except:
      return None

  @property
  def trailingPeRatio(self):
    try:
      return self.yfData.info['trailingPE']
    except:
      return None
  
  @property
  def forwardPeRatio(self):
    try:
      return self.yfData.info['forwardPE']
    except:
      return None

  @property
  def fourYearEarnings(self):
    try:
      return dict(self.yfData.earnings['Earnings'])
    except:
      return None
  @property
  def mostRecentYearsEarnings(self):
    try:
      return list(self.yfData.earnings['Earnings'])[-1]
    except:
      return None
  @property
  def fourYearEarningsGrowthRate(self):
    try:
      earnings = list(self.yfData.earnings['Earnings'])
      if len(earnings) <= 1:
        return None
      else:
        index = 0
        growth_rates = []
        while index < len(earnings)-1:
          growth_rates.append(((earnings[index+1]-earnings[index])/earnings[index])*100)
          index += 1
        return sum(growth_rates)/(len(earnings)-1)
    except:
      return None

  @property
  def fourYearRevenue(self):
    try:
      return dict(self.yfData.earnings['Revenue'])
    except:
      return None

  @property
  def fourYearRevenueGrowthRate(self):
    try:
      revenue = list(self.yfData.earnings['Revenue'])
      if len(revenue) <= 1:
        return None
      else:
        index = 0
        growth_rates = []
        while index < len(revenue)-1:
          growth_rates.append(((revenue[index+1]-revenue[index])/revenue[index])*100)
          index += 1
        return sum(growth_rates)/(len(revenue)-1)
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
  def returnOnEquity(self):
    try:
      mostRecentYear = list(self.fourYearEarnings.keys())[-1]
      earnings = self.fourYearEarnings[mostRecentYear]
      print(earnings)
      totalEquity = dict(self.yfData.balance_sheet[list(self.yfData.balance_sheet)[0]])['Total Stockholder Equity']
      print(totalEquity)
      return (earnings/totalEquity)*100
    except:
      return None
  @property
  def interestCoverageRatio(self):
    stockData = self.yfData
    try:
      dataDictinary = dict(stockData.financials[list(stockData.financials)[0]])
      ebit = dataDictinary['Ebit']
      interestExpense = dataDictinary['Interest Expense']
      if interestExpense != 0:
        return abs(ebit/interestExpense)
      else:
        return "No interest expense"
    except:
      return None

class IndustryAverages:
  def __init__(self):
    pass

def netIncomePoints(stockObject):
  points = 0
  if stockObject.mostRecentYearsEarnings != None:
    if stockObject.mostRecentYearsEarnings > 0:
      points += 4
  if stockObject.fourYearEarningsGrowthRate:
    if stockObject.fourYearEarningsGrowthRate >= 0:
      growth_rate_points =  int(stockObject.fourYearEarningsGrowthRate) * 0.25
      if growth_rate_points >= 11:
        points += 11
      else:
        points += growth_rate_points
  return points

def currentRatioPoints(stockObject):
  points = 0
  if stockObject.currentRatio:
    if stockObject.currentRatio < 1:
      points += 0
    elif stockObject.currentRatio < 1.5:
      points += 2
    elif stockObject.currentRatio < 2:
      points += 4
    elif stockObject.currentRatio < 2.5: 
      points += 6
    elif stockObject.currentRatio < 3:
      points += 8
    else:
      points += 10
  return points

def revenueGrowthRatePoints(stockObject):
  points = 0
  if stockObject.fourYearRevenueGrowthRate:
    if stockObject.fourYearRevenueGrowthRate >= 40:
      points += 10
    else:
      points += int(stockObject.fourYearRevenueGrowthRate) * 0.25
  return points

def operatingCashflow(stockObject):
  points = 0
  if stockObject.operatingCashflow:
    if stockObject.operatingCashflow > 0:
      points += 10
  return points

def interestCoverageRatioPoints(stockObject):
  points = 0
  if stockObject.interestCoverageRatio:
    if stockObject.interestCoverageRatio >= 10:
      points += 10
    else:
      points += int(stockObject.interestCoverageRatio)
  return points

def dividendPoints(stockObject):
  points = 0
  if stockObject.fiveYearAvgDividendYield:
    if stockObject.fiveYearAvgDividendYield >=5:
      points+=5
    else:
      points += int(stockObject.fiveYearAvgDividendYield)
  if stockObject.payoutRatio:
    if stockObject.payoutRatio < 30:
      points += 5
    elif stockObject.payoutRatio < 40:
      points += 4
    elif stockObject.payoutRatio < 50:
      points += 3
    elif stockObject.payoutRatio < 60:
      points += 2
    elif stockObject.payoutRatio < 70:
      points += 1
  return points

def priceToBookPoints(stockObject):
  points = 0
  if stockObject.priceToBook:
    if stockObject.priceToBook < 1:
      points += 5
    else:
      if stockObject.priceToBook <= 10:
        points += (5-(0.5*int(stockObject.priceToBook)))
  return points
    
def stockAnalyzer(stockObject):
  totalPoints = 0
  totalPoints += netIncomePoints(stockObject)
  #Need to implement the Pe based on industry once I get the pe data formated
  totalPoints += currentRatioPoints(stockObject)
  #Need to implement the return on Assets once I get the data formatted
  totalPoints += revenueGrowthRatePoints(stockObject)
  totalPoints += operatingCashflow(stockObject)
  totalPoints += interestCoverageRatioPoints(stockObject)
  totalPoints += dividendPoints(stockObject)
  #Need to implement the profit margin data

def run():
  with open('NYSE.csv','r') as nyse, open('NASDAQ.csv','r') as nasdaq:
    nyseReader = csv.DictReader(nyse)
    nasdaqReader = csv.DictReader(nasdaq)
    allStocks = sorted([stock['Ticker'] for stock in nyseReader] + [stock['Symbol'] for stock in nasdaqReader])
    s1 = Stock('INTC')
if __name__ == "__main__":
  run()