#!/usr/bin/env python
# coding: utf-8

# # Individual Assignment 1 
# 
# Due date: on Jan 31, 2022
# 
# ** Grading:** This is a pass or fail assignment. 
# 
# ** You must provide a *clean* code.** Make sure the grader can follow each step of your analysis. Put comments to describe what you are doing (Using MARKDOWN or using #). Remove any lines of code that is not necessary. If you struggle on a question, that is OK, as long you show all the steps that you have taken and describe what is not working. *If your code is not clean and it is hard for the grader to understand what you are doing, you will fail.*
# 
# ** SUBMISSION of ASSIGNMENT ** 
# 
# ** Must submit your assignments to two places:
# (1) Save the Jupyter code in PDF. To do so, click on File->Download as->PDF. OR do download as "HTML". This is to be uploaded to Crowdmarks (I will receive an email with a link to upload the assignment)
# (2) Upload your .ipynb file (Jupyter code file) to Quercus in the assignment section.
# 
# -- Remove all the sample code that I provide to you. Keep your code only. Make sure your code works fully, from start to finish with no error message. In other words, if you close Jupyter, re-open your code, and press the PLAY button, does your code work fully with no error message? 

# # Manipulating and visualizing financial data with CRSP and Fama-French
# - PETER SILONG LI
# - 1004921454
# - LEC 01 
# 

# # Sample code
# 
# Assignment questions are below the sample code

# In[42]:


select_crsp.plot()


# --------------------------------------------------------------------------------------------
# # Assignment questions begin here:
# 
# 1. Choose 5 stocks in the CRSP dataset (different from the one used below). Make sure these stocks existed on the first trading day of the year 2000. Your analysis begins from January 2000 to December 2017. **Do not pick the same stocks used in the sample code.** I want to see the code on how you selected the 5 stocks, similar to df = crsp[crsp['TICKER'].isin(['MSFT', 'AAPL', 'IBM', 'AMZN', 'FB'])].
# 2. Provide the summary statistics table (mean, std, min, max) and the 10th, 25th, 50th, 75th, 90th percentiles of your 5 stock returns.
# 3. Plot a bar graph showing the mean and standard deviation of each stock returns.
# 4. If you invest in each stocks $1, which stock generated the highest return today? Plot the buy-and-hold returns for all your stocks. Make sure the dates are on the x-axis.
# 6. Plot the buy-and-hold **abnormal** returns (BHAR) for all your stocks. To do this, you substract from the buy-and-hold return of the stock the buy-and-hold market return.
# 
# 7. Did any of your stock outperformed the market if you have invested in the stock at the initial date? Base your decision on the BHAR.
# 7. What is the Sharpe ratio of the market and the five chosen stocks? Which one has the largest Sharpe ratio?
# 

# ## Choose 5 stocks and start your data in 2000 (remove any data before January 2000). Do not pick the same stocks used in the sample code.

# In[85]:


#Loading packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Loading crsp data into Pandas Dataframe from my directory
#I changed the name of the CRSPSP500 file to 'data' for simplicity
crsp = pd.read_csv('C:\\Users\\lipet\\Desktop\\mgdf40\\data.gz')

# Formatting date in pandas date time
crsp['date'] = pd.to_datetime(crsp['date'], format ='%Y-%m-%d')

#Keeping data only from Jan 1, 2000 to Dec 31, 2017
crsp = crsp[crsp['date'].between('2000-01-01','2017-12-31')]

#printing crsp to see which stocks exist in date range
print(crsp.head(10))
print(crsp.tail(10))

#picking the 5 stocks
select_tickers = ['T','ORCL','SUNW','TROW','HON']
select_crsp = crsp[crsp['TICKER'].isin(select_tickers)]



# ## Provide the summary statistics of the returns (mean, std, min, max) and the 10th, 25th, 50th, 75th, 90th percentiles of your 5 stock returns.

# In[89]:


#reshaping table to plot returns
select_crsp =select_crsp[['RET','TICKER','date']]
select_crsp = select_crsp.pivot(columns='TICKER', values='RET', index='date')
select_crsp

#displaying the 10th, 25th, 50th, 75th, 90th percentiles of 5 stock returns
select_stats = select_crsp.describe(percentiles=[.1,.25,.5,.75,.9])
print(select_stats)

#only displaying mean std min and max
select_stats.loc[["mean","std","min","max"]]




# ## Plot a bar graph showing the mean and standard deviation of each stock returns.

# In[90]:


#Plotting bar
select_stats.T[['mean','std']].plot.bar()


# ## If you invest in each stocks $1, which stock generated the highest return today? Plot the buy-and-hold returns. Make sure the dates are on the x-axis.

# In[97]:


#plotting graph
select_crsp = select_crsp['2000-01-01':]
select_crsp_inv_grth = (select_crsp + 1).cumprod()
select_crsp_inv_grth.loc[pd.to_datetime("2017-12-29")]
select_crsp_inv_grth.sort_index(inplace=True)
select_crsp_inv_grth.plot()


# #### Plot the buy-and-hold **abnormal** returns (BHAR) of all your stocks. 

# In[187]:


#Loading Fama French, changed csv to dataFactors for simplicity
ff = pd.read_csv('C:\\Users\\lipet\\Desktop\\mgdf40\\dataFactors.csv')


#convertin fama-french return data to decimals
ff[['Mkt-RF','SMB','HML','RF']] =  ff[['Mkt-RF', 'SMB', 'HML','RF']] / 100

select_crsp = crsp[crsp["TICKER"].isin(['T','ORCL','SUNW','TROW','HON'])]
select_crsp = select_crsp.sort_values(by=['PERMNO', 'date'])
select_crsp = select_crsp[select_crsp['date']>'2000-01-01']

# get the gross returns
select_crsp['gRET'] = 1 + select_crsp['RET']
select_crsp['gMkt'] = 1 + (select_crsp['Mkt-RF'] + select_crsp['RF']) # 'Mkt-RF' is the market excess returns


# get the cumulative product of the gross returns
select_crsp['prod_gRet'] = select_crsp.groupby(['PERMNO'])['gRET'].cumprod()
select_crsp['prod_gMkt'] = select_crsp.groupby(['PERMNO'])['gMkt'].cumprod()

# get the bhar
select_crsp['bhar'] = select_crsp['prod_gRet'] - select_crsp['prod_gMkt']
select_crsp = select_crsp.pivot(columns='TICKER', values='bhar', index='date') 

select_crsp.plot()


# ## Did any of your stocks outperformed the market if you have invested in the stock at the initial date? Base your decision on the BHAR.

# In[188]:


select_crsp['bhar'] = select_crsp['prod_gRet'] - select_crsp['prod_gMkt']


# ## 7. What is the Sharpe ratio of the market and the five chosen stocks? Which one has the largest Sharpe ratio?

# In[109]:


select_stats.loc["Sharpe Ratio"] = select_stats.loc["mean"]/select_stats.loc["std"]
select_stats
largest_ratio = max(select_stats.loc["Sharpe Ratio"])
print(largest_ratio)


# In[ ]:




