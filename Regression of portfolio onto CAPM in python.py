#!/usr/bin/env python
# coding: utf-8

# Peter Silong Li
# 1004921454
# LEC01
# 
# # Assignment questions:
# 
# 1. Choose 5 stocks in the CRSP dataset (different from the one used below). Make sure these stocks existed on the first trading day of the year 2000. Your analysis begins from January 2000 to 2018. **Do not pick the same stocks used in the sample code.** I want to see the code on how you selected the 5 stocks, similar to df = crsp[crsp['TICKER'].isin(['MSFT', 'AAPL', 'IBM', 'AMZN', 'FB'])].
# 2. With your 5 stocks, construct an equal-weighted portfolio and calculate the monthly returns and plot the returns.
# 3. Test the CAPM on your portfolio. You must do:
# $R_{t}-RF_t = \alpha + \beta R_{M,t}-RF_t + \varepsilon_t$ as a regression. 
# Hint: Merge the Fama-French data to your return dataframe of your portfolio. $R_{t}-RF_t$ this is the excess return of your portfolio and $R_{M,t}-RF_t$ the excess return of the market in Fama-French. Can the CAPM model fully explain your returns?
# 4. Redo 2,3 for a value-weighted portfolio
# 5. Compare the returns of your equal- and value-weighted portfolios. Why do you think they differ?

# ## Choose 5 stocks in the CRSP dataset (different from the one used below). Make sure these stocks existed on the first trading day of the year 2000. **Do not pick the same stocks used in the sample code.** I want to see the code on how you select the 5 stocks, similar to df = crsp[crsp['TICKER'].isin(['MSFT', 'AAPL', 'IBM', 'AMZN', 'FB'])].

# In[30]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import statsmodels.formula.api as smf
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')

crsp = pd.read_csv('C:\\Users\\lipet\\Desktop\\mgdf40\\data.gz')
# format date in pandas datetime
crsp['date'] = pd.to_datetime(crsp['date'], format='%Y/%m/%d')
# create a new column for the market cap
# This number of shares outstanding * the price of the stock
crsp['MCAP'] = crsp["SHROUT"] * crsp["PRC"]
# The dates in CRSP are at the end of the month of the last trading day (not essentially the last calendar day)
# We will push all the dates in CRSP to the end of the month
crsp['date'] = crsp['date'] + pd.offsets.MonthEnd(0)

#picking the 5 stocks
select_tickers = ['T','ORCL','SUNW','TROW','HON']
select_crsp = crsp[(crsp['TICKER'].isin(select_tickers)) & (crsp["date"] >= '2000-01-01')]


# ## 2. With your 5 stocks, construct an equal-weighted portfolio and calculate the portfolio monthly returns and plot the returns.

# In[42]:


# load the fama-french data
ff = pd.read_csv('C:\\Users\\lipet\\Desktop\\mgdf40\\dataFactors.csv')

# we have to format the date
ff['date'] = pd.to_datetime(ff.date, format='%Y%m')

# again, let's push the date to the end of the calendar month
ff['date'] = ff['date'] + pd.offsets.MonthEnd(0)

# The issue with the fama-french data is that the returns are in %!!! So we have to divide by 100
ff[['Mkt-RF', 'SMB', 'HML', 'RF']] = ff[['Mkt-RF', 'SMB', 'HML', 'RF']] / 100
# or ff[['Mkt-RF', 'SMB', 'HML', 'RF']] /= 100 for short

# This time we have to rename Mkt-RF variable for EXMKT - we cannot have a minus sign in the name when running OLS
ff = ff.rename(columns={'Mkt-RF':'EXMKT'})
# merge the fama-french data with crsp on the date column
# the "how" is to say that we a match on the left side only
crsp = pd.merge(crsp, ff, on='date', how='left')
#crsp['EXRET'] = crsp["RET"] - crsp["RF"]
#select_crsp = select_crsp.pivot(columns='TICKER', values='RET', index='date')

ew_port = 1 + select_crsp
#assign $1 dollar investment at beginning of the portfolio formation
ew_port.loc[pd.to_datetime('1999-12-31')] = 1 
ew_port = ew_port.sort_index()
ew_port
#Step 2: Cumalative product down each column 
ew_port = ew_port.cumprod()
ew_port = ew_port.fillna(method='ffill')
ew_port['portfolio_value'] = ew_port.sum(axis=1)
#preview
ew_port
#step 4 getting returns on each month for portfolio 
ew_port['portfolio_return'] = ew_port['portfolio_value'].pct_change()
# plotting the portfolio returns
ew_port['portfolio_return'].plot(figsize=(13,3))
# money made in dollars by buying this portfolio 
plt.figure()
ew_port['portfolio_value'].plot()
plt.ylabel('Portfolio performance in $')


# ## 3. Test the CAPM on your portfolio. You must do:
# $R_{t}-RF_t = \alpha + \beta R_{M,t}-RF_t + \varepsilon_t$ is the regression. 
# Hint: Merge the Fama-French data to your return dataframe of your portfolio. $R_{t}-RF_t$ this is the excess return of your portfolio and $R_{M,t}-RF_t$ the excess return of the market in Fama-French. 
# * Report the $\alpha$ and $\beta$ of your regression *
# Can the CAPM model fully explain your returns?

# In[ ]:


crsp 
ew_port_2 = select_crap.pivot(columns='TICKER', values = 'RF', index = 'date')
ew_port_2
#use a pivot table to extrat monthly export
ew_port_3 = select_crap.pivot(columns ='TICKERS', values = 'EXMKT', index='date')
ew_port_3

#run the regression for the equal-weighted portfolio (EXret and Exmkt)
reg = snf.ols('EKRET-EXMKT'), data=ew_port).fit()
reg.summary()


# ## 4. Redo 2,3 for a value-weighted portfolio

# In[52]:


#Famafrench merged in previous Question
#picking the 5 stocks
select_tickers = ['T','ORCL','SUNW','TROW','HON']
select_crsp = crsp[(crsp['TICKER'].isin(select_tickers)) & (crsp["date"] >= '2000-01-01')]
select_crsp
#pivot 
ew_port_B = select_crsp.pivot(columns='TICKER', values ='RF', index='date')
ew_port_B
#extract monthly EXMKT from data 
ew_port_c = select_crsp.pivot(columns='TICKER', values = 'EXMKT', index = 'date')
ew_port_c
#add monthly RF to equal weighted portfolio
ew_port['RF'] = ew_port_B['CPB']
#finding monthly exret and adding as column
ew_port['EXRET'] = ew_port["portfolio_return"] - ew_port["RF"]
#add monthly exmkt and as column
ew_port['EXMKT'] = ew_port_c["CPB"]
ew_port


# ## 5. Compare the returns of your equal- and value-weighted portfolios. Why do you think they differ? Give me your best guess.

# In[ ]:


#The returns of the equal weighted and value weighted portfolios are almost equal 
#they differ based on the weights given to the different stocks
#where equal weighted portfolio assigns 20% to each of the 5 stocks
#value weighted portflio assigns varying weights to each of the 5 stocks, eg: 15%, 25%, 20% , 20%, 20% 
#returns will therefore vary over time 

