import yfinance as yf
import csv
from datetime import date
import sys
class Stock:
  def __init__(self,ticker,industryAveragesDict):
    self.ticker = ticker
    self.yfData = yf.Ticker(ticker)
    self.industryAveragesDict = industryAveragesDict
  def getPoints(self):
    return stockAnalyzer(self)

  def __str__(self):
    return f"{self.ticker.upper()} ({self.industry})"

  def information(self):
    return self.yfData.info
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
  def profitMargin(self):
    try:
      return self.yfData.info['profitMargins']*100
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
      totalEquity = dict(self.yfData.balance_sheet[list(self.yfData.balance_sheet)[0]])['Total Stockholder Equity']
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

  @property
  def averagesForIndustry(self):
    try:
      returningDict = self.industryAveragesDict[self.industry]
      for key in returningDict:
        if key != "Industry Name" and key != "Yahoo Finance Equivalent":
          returningDict[key] = float(returningDict[key].strip("%"))
      return returningDict
    except:
      return {"Average PE Ratio": 20,"Average ROE":18.6,"Average Profit Margin":11}
  
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

def priceToEarningsPoints(stockObject):
	points = 0
	averagePe = stockObject.averagesForIndustry["Average PE Ratio"]
	if stockObject.forwardPeRatio and stockObject.forwardPeRatio >= 0:
		if stockObject.forwardPeRatio < averagePe - 5:
			points += 10
		elif stockObject.forwardPeRatio < averagePe - 4:
			points += 8
		elif stockObject.forwardPeRatio < averagePe - 3:
			points += 6
		elif stockObject.forwardPeRatio < averagePe - 2:
			points += 4
		elif stockObject.forwardPeRatio < averagePe - 1:
			points += 2
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

def returnOnEquityPoints(stockObject):
	points = 0
	averageROE = stockObject.averagesForIndustry["Average ROE"]
	if stockObject.returnOnEquity:
		if stockObject.returnOnEquity - averageROE >= 0:
			points = int((stockObject.returnOnEquity - averageROE) * 0.5)
			if points >= 10:
				return 10
			else:
				return points
	return points
def revenueGrowthRatePoints(stockObject):
  points = 0
  if stockObject.fourYearRevenueGrowthRate:
    if stockObject.fourYearRevenueGrowthRate >= 40:
      points += 10
    else:
      points += int(stockObject.fourYearRevenueGrowthRate) * 0.25
  return points

def operatingCashflowPoints(stockObject):
  points = 0
  if stockObject.operatingCashflow:
    if stockObject.operatingCashflow > 0:
      points += 10
  return points

def interestCoverageRatioPoints(stockObject):
  points = 0
  try:
    if stockObject.interestCoverageRatio:
      if stockObject.interestCoverageRatio >= 10:
        points += 10
      else:
        points += int(stockObject.interestCoverageRatio)
  except:
    return points
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

def profitMarginPoints(stockObject):
  points = 0
  try:
    averageProfitMargin = stockObject.averagesForIndustry["Average Profit Margin"]
    if stockObject.profitMargin:
      if stockObject.profitMargin - averageProfitMargin >= 0:
        if int(stockObject.profitMargin-averageProfitMargin)*0.5 >= 5:
          points += 5
        elif int(stockObject.profitMargin-averageProfitMargin)*0.5 > 0:
          points += int(stockObject.profitMargin-averageProfitMargin)*0.5
  except:
    return points
  return points

def priceToBookPoints(stockObject):
  points = 0
  if stockObject.priceToBook and stockObject.priceToBook > 0:
    if stockObject.priceToBook < 1:
      points += 5
    else:
      if stockObject.priceToBook <= 10:
        points += (5-(0.5*int(stockObject.priceToBook)))
  return points

def marketCapPoints(stockObject):
  points = 0
  if stockObject.marketCap:
    if stockObject.marketCap > 10000000000:
      points += 5
    elif stockObject.marketCap > 2000000000:
      points += 4
    elif stockObject.marketCap > 300000000:
      points += 2
  return points

def stockAnalyzer(stockObject):
  totalPoints = 0
  totalPoints += netIncomePoints(stockObject)
  totalPoints += priceToEarningsPoints(stockObject)
  totalPoints += currentRatioPoints(stockObject)
  totalPoints += returnOnEquityPoints(stockObject)
  totalPoints += revenueGrowthRatePoints(stockObject)
  totalPoints += operatingCashflowPoints(stockObject)
  totalPoints += interestCoverageRatioPoints(stockObject)
  totalPoints += dividendPoints(stockObject)
  totalPoints += profitMarginPoints(stockObject)
  totalPoints += priceToBookPoints(stockObject)
  totalPoints += marketCapPoints(stockObject)
  return totalPoints

def individualStockScore(Ticker):
  s1 = Stock(Ticker)
  return f"{s1}: {stockAnalyzer(s1)}"

def run():
  with open('NYSE.csv','r') as nyse, open('NASDAQ.csv','r') as nasdaq,open("pedatafinal.csv","r") as data:
    nyseReader = csv.DictReader(nyse)
    nasdaqReader = csv.DictReader(nasdaq)
    reader = list(csv.DictReader(data))
    dict_final_pe_data = {i["Yahoo Finance Equivalent"]:i for i in reader}
    allStocks = sorted([stock['Ticker'] for stock in nyseReader] + [stock['Symbol'] for stock in nasdaqReader])
    scoringList = []
    for stock in allStocks:
      stockObj = Stock(stock,dict_final_pe_data)
      stockScore = stockAnalyzer(stockObj)
      print(f"{stockObj}: {stockScore}")
      scoringList.append((stockObj,stockScore))
    scoringList = sorted(scoringList, key = lambda x: x[1], reverse = True)
    with open(f'{date.today()}-Output.txt','w') as output:
      for val in scoringList:
        output.write(f"{val[0]}: {val[1]}\n")
    sys.exit()
if __name__ == "__main__":
  run()