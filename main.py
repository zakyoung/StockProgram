import yfinance as yf
class Stock:
  def __init__(self,ticker):
    self.ticker = ticker
    self.yfData = yf.Ticker(ticker).info
  @property
  def sector(self):
    return self.yfData['sector']
  @property
  def payoutRatio(self):
    try:
      return self.yfData['payoutRatio'] * 100
    except:
      return 'Stock does not pay a dividend'
  @property
  def priceToBook(self):
    return self.yfData['priceToBook']
  @property
  def marketCap(self):
    return self.yfData['marketCap']
  @property
  def currentDividendRate(self):
    return self.yfData['dividendRate']
  @property
  def priorYearDividendRate(self):
    return self.yfData['trailingAnnualDividendRate']
  @property
  def DividendGrowthRate(self):
    try:
      return ((self.currentDividendRate-self.priorYearDividendRate)/self.priorYearDividendRate) * 100
    except:
      return "Calculation not possible"
  @property
  def fiftyTwoWeekHigh(self):
    return self.yfData['fiftyTwoWeekHigh']
  @property
  def fiftyTwoWeekLow(self):
    return self.yfData['fiftyTwoWeekLow']
  @property
  def previousClose(self):
    return self.yfData['previousClose']
  @property
  def trailingPeRatio(self):
    return self.yfData['trailingPE']
  @property
  def forwardPeRatio(self):
    return self.yfData['forwardPE']

