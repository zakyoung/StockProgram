This is the data weighting system used in the stock program. The data will be weighted out of 
100 points and some metrics will have a higher weight than others. The goal of the program is to identify undervalued stocks by evaluating the metrics of every stock on the NYSE and NASDAQ with possibly other exchanges being added over time. I will alter the weights over time depending on what stocks I end up getting based on differenent weights.

1. Net income over a 4 year period: Here we are looking that their net income is going by a healthy consistent growth rate(15 points)(implemented)
  - 0.25 points for every 1% net income growth rate up to 11 points
  - 4 points if the net income is positive

2. Pe based on industy: Since we are looking for value stocks we have to try to find earnings that are cheap based on the rest of the industry averages(15 points)(Need to implement the points calculator still)
  - 2.5 points for every 1 point under the industry average so if the industry average pe is 20 and our stock has a 14 pe you would have the max amount of points.

3. Current Ratio: The equation for current ratio is current assets / liabilities. The current ratio is a liquidy ratio that shows if a company has enough liquidity to cover their current obligations(10 points)(implemented)
  - 0 points if under 1
  - 2 points if >= 1
  - 4 points if over 1.5
  - 6 points if over 2
  - 8 points if over 2.5
  - 10 points if over 3

4. Return on assets: This shows how well a company is using their assets to create revenue. We will look at this as how their ROA compares to historical averages in the industy(10 points)(Need to implement the points calculator still)
  - 0 points if under industry average
  - 0.5 points for every 1 % over the industry average up to ten points

5. revnue growth over a 4 year period: Here we also want to make sure that companies are not just more profitable but also they are increasing their revenue in a consistent manor.(10 points)(implemented)
  - 0.25 points for every 1% revnue growth rate

6.Positive operating cashflow: This is either True or False and we will use this to make sure that the company is actually bringing in money and that it is not using accounting tactics to fluff data(10 points)(implemented)
  - 0 points if False
  - 10 points if True

7. Ebit/Company interest expense: Im not sure if this is a legitamate ratio or not but in theory this should show if a company is able to cover there interest payments and the higher this number is the better.(10 points)(implemented)
  - 0 points if it is under 1
  - 1 point for every 1 percent over 1(max 10)

8. Dividend and a reasonable payout ratio: This is a personal preference but I prefer companies that pay dividends. I have it weighted lower because I also dont want to weed out companys that might be on the verge of being able to develop a dividend and may have high growth potential.(10 points)(implemented)
  - 1 point for every % dividend up to 5
  - 5 points for a payout ratio under 30% and -1 points for every 10% over 30 
  
  except for reits which have to pay out 90% of earnings so as long as reits are under 95% they will get 5 points Will implement this in a later version

9. Profit margin based on industry: We are looking or companys that have a higher profit margin compared to other companys in the industry(5 points)(still need)
  - 0 If the companys profit margin is under the industry average
  - 0.5 points for every 1 % higher profit margin compared to industry average up to ten percent

10. Price to book ratio: This shows the value of the assets that you are getting when you purchase the company(5 points)
  - 5 points if under 1
  - -0.5 points for every 1 increase over 1 so a price to book of 2 would give 4.5 points 

