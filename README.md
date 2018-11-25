# Title: Monte Carlo Simulation in S&P 500 stock price data

## Team Member(s):
Alice Bhopalwala, Sumedh Hegde

# Monte Carlo Simulation Scenario & Purpose:
In an ideal world, a stock price, at any given point of time, will always try to be close to or reach towards the mean of the entire data; unless an external event occurs to disrupt that behaviour. In real world, we can compare such events to company decisions, news, product launches, etc. To analyse this behaviour, we have used monte carlo simulation to predict ten different ways the closing price of a stock could move in the future. Our target is to obtain this trend for all the companies and analyze if the hypothesis generated from an ideal world scenerio would fit the real world actual data.
More info on S&P 500 companies: https://en.wikipedia.org/wiki/List_of_S%26P_500_companies

## Simulation's variables of uncertainty
In order to make a model that does justice with the observation of the hypothesis, we decided to predict a fifth of the points we originally had, which means we predicted 250 points where we had approx 1250 points for each stock. For further accuracy, these 250 points have been predicted 10 different times to assist with better analysis. 
To predict closing vlaue of the stock prices for the next 250 points, we had to calculate the noise between price at (t) time and price at (t-1) time. The noise is then multiplied to stock price at (t) time to get the stock price at (t+1) time.

## Hypothesis before running the simulation:
Hypothesis: If The mean (x) of the latest 1/5th (approx 250 points) of the points at hand is less than the over all mean (all points, approx 1250) (y) then it is more likely for the mean (z) of the next 250 predicted points to be greater than x (as reasoning given above, to be closer to the mean of the entire data)
Vice versa, if the mean (x) of the latest 1/5th (approx 250 points) of the points at hand is greater than the over all average (y) then it is more likely for the mean (z) of the next 250 predicted points to be less than x.

Alternative Hypothesis: This ideal world hypothesis is not applicable in the real world.

## Analytical Summary of your findings: (e.g. Did you adjust the scenario based on previous simulation outcomes?  What are the management decisions one could make from your simulation's output, etc.)

## Instructions on how to use the program:

## All Sources Used:
https://datascienceplus.com/how-to-apply-monte-carlo-simulation-to-forecast-stock-prices-using-python/
https://www.kaggle.com/camnugent/sandp500
