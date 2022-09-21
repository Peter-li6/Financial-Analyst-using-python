#!/usr/bin/env python
# coding: utf-8

# # MGFD25 Assignment 1: 
# ## Building your first FinTech App - The stock price notifciation app

# Quandl is a data API specialized in providing economics and financial data.  We will be using the EOD (End of Day) feed from the Toronto Stock Exchange.  To access Quandl’s Python API, you will need to install the “Quandl Python package” first.  If the "Quandl Python package is installed correctly, you shall be able to run the following line to import:

# ## Part 1 Retriving EOD Stock data 

# ### import libraries

# In[1]:


import pandas as pd
import quandl


# To start using the service, you will need to provide your **assigned API key**.  This is to ensure that you are the authorized person to access this data.  Please note that there is a limit of how much data you can retrieve.  Under normal circumstances you shall not have to worry about hitting the limit.  Please beware of coding errors that may lead to excessive traffic, your account can be blocked.
# 
# Again, this API key is unique for each person and you must not share this key.  Whenever you are uploading your code to a shared environment, the best practice is to mask the API Key.  Meaning you don't type it out so people can see it, you'll use something called the "Environment variables", which we'll cover in later section.

# ### Use %env to create environment variables

# In[ ]:


get_ipython().run_line_magic('env', 'quandl_key = #put your api key here')
get_ipython().run_line_magic('env', 'twilio_sid = #put your own credential here')
get_ipython().run_line_magic('env', 'twilio_token = #put your own credential here')


# ### Quandl demo code
# see full documentation here: https://www.quandl.com/data/XTSE-Toronto-Stock-Exchange-Prices/documentation?anchor=sample-data

# #### Filter by a date or range of dates

# In[ ]:


#you see I used the stored environment var instead of the acutal key code here:
quandl.ApiConfig.api_key = get_ipython().run_line_magic('env', 'quandl_key ')
ticker = 'XTSE/ABX'
data = quandl.get(ticker, start_date='2021-11-30', end_date='2022-12-31')
display(data)


# In[ ]:


# examining the dataframe
type(data)
data.info
data.shape
data.columns
data.index # index defaults to start at 0


# ![image.png](attachment:image.png)

# In[ ]:


# slicing examples
data.iloc[-5:, :]


# #### Select output columns (change index number to retrieve only that column)

# In[ ]:


# change index number to retrieve only that column
data = quandl.get(ticker, start_date='2020-11-30', end_date='2020-12-31', column_index = 4)
display(data)


# In[ ]:


# Pandas df vs series
type(data)
close = data['Close']
close
type(close)


# ### Retrive data for mulitple stocks

# In[ ]:


tickers = ['XTSE/BMO', 'XTSE/CM', 'XTSE/RY', 'XTSE/NA', 'XTSE/TD']
type(ticker)


# In[ ]:


data = quandl.get(tickers, start_date='2020-12-28', end_date='2020-12-31', column_index = 4)
display(data)


# #### Import a list of tickers

# In[ ]:


pwd


# In[ ]:


cd ~/Downloads


# In[ ]:


df = pd.read_csv('tsx60.csv')
display(df)


# In[ ]:


type(df)


# In[ ]:


tickers = df.iloc[:,0].to_list()
print(tickers)


# In[ ]:


type(tickers)


# In[ ]:


data = quandl.get(tickers, start_date='2020-12-30', end_date='2020-12-31', column_index = 4)
display(data)


# ### Finding daily return

# In[ ]:


from datetime import datetime, time
last_tday = datetime.today()
prev_bday = last_tday-pd.tseries.offsets.BDay(1)
print(prev_bday)

data = quandl.get(tickers, start_date=prev_bday, end_date=last_tday, column_index = 4)
display(data)
# please note that data may return blank when the closing price of the day is not yet available.


# On trading days, the TSX opens at 9:30am and closes at 4:00pm.  Given that some data providers may delay their data feed as much as 15 mins, we will program our app to capture the closing value at 4:15pm to be safe.

# In[ ]:


# We import the datatime package so we can use some datetime functions.  
# In this example, we will need the function .today to get today's date.
now = datetime.now()

# assume the market will close at 4pm and data will become available at 16:15 the day of
market_close_time = now.replace(hour=16, minute=15, second=0, microsecond=0)

# If the script is run after 16:15, last_tday is today
if now > market_close_time:
    last_tday = datetime.today()
    last_tday_minus1 = last_tday-pd.tseries.offsets.BDay(1)

#otherwise, last_tday is the previous business day
else:
    last_tday = datetime.today()-pd.tseries.offsets.BDay(1)
    last_tday_minus1 = last_tday-pd.tseries.offsets.BDay(1)

data = quandl.get(tickers, start_date=last_tday_minus1, end_date=last_tday, column_index = 4)
display(data)


# #### Calculate performance

# In[ ]:


pct_change = (data.iloc[1,:] - data.iloc[0,:])/data.iloc[0,:]
print(pct_change)


# #### Top 3 Gainers

# In[ ]:


gainers = pct_change[pct_change>0]
gainers.nlargest(3)


# #### Top 3 Losers

# In[ ]:


losers = pct_change[pct_change<0]
losers.nsmallest(3)


# ### 10 Most actively traded stocks
# The output should inlcude the tickers of the top 10 stocks with their trading volumnn of the day.
# Please sort the volumn from high to low.

# In[ ]:


# your turn to code here:


# ## Adding SMS Notifications

# Twilio is an amazing communication plug-in that can take your app to a new level.  You can send SNS, email, voice or even video messages to your subscribers.  Trial accounts are free to use and you can register here: https://www.twilio.com/try-twilio
# You shall receive $15 credit once signed up, and that shall be sufficient for you to complete your prototype.
# 
# There is Twilio Helper Library which you must first download.  Again, I will suggest you to install this package through the Anaconda Environment.  You shall be able to run the code below once the package is installed successfully.

# In[ ]:


from twilio.rest import Client

# Your Account SID and Auth Token from twilio.com/console
# I masked it using environment variable 
account_sid = get_ipython().run_line_magic('env', 'twilio_sid ')
auth_token = get_ipython().run_line_magic('env', 'twilio_token')

client = Client(account_sid, auth_token)
name = "Jane Smith 987654321"
quote = name + "\nToday's market recap - " + last_tday.strftime('%Y-%m-%d') + "\nTop 3 losers\n" + str(losers.nsmallest(3)) + "Top 3 gainers" + str(gainers.nsmallest(3))

message = client.messages.create(
    to="+1647xxxxxxx", #change this number to your verified phone number
    from_="+19378882929", #change this number to your trial twilio phone number
    body = quote)

print(message.sid)


# Now you know how to create the code to display the EOD stock data.  The next step is to deploy the above code onto a cloud server.  Please note that this will be out of the scope of this class.  However, if you are eager to make this a working protogype, there are a few ways to do this.  You can either [run the python script in AWS EC2](https://medium.com/@praneeth.jm/running-python-scripts-on-an-aws-ec2-instance-8c01f9ee7b2f) and schedule it with code, or try AWS Lambda.  AWS Lambda is called severless, and is the newer way of running scripts based on events.  You may also want to consider [containerizing(using Docker)](https://runnable.com/docker/python/dockerize-your-python-application) the script and [deploy it into AWS.](https://aws.amazon.com/getting-started/hands-on/deploy-docker-containers/)
# 
# There are probably simpler and better ways to deploy this as well.  I encourage you to explore and try things out.

# ## Part 2 Generating trading signals

# ### TA-Lib
# TA-Lib is an open-sourced library that consists of over 150 technical trading strategies.  This library is very popular among financial software developers.  You are going to pick out some strategies to try.  See http://mrjbq7.github.io/ta-lib/index.html for more information about this Python library.
# 
# #### Installation
# Similar to the other Python packages that you've installed earlier.  In the command line, type 
# ```$ pip install TA-Lib```
# 
# If you experience trouble during installation, this article may help: [How to install Ta-Lib in Python](https://blog.quantinsti.com/install-ta-lib-python/#macos)
# 

# #### Impoart TA-Lib library

# In[ ]:


import talib
import numpy


# In[ ]:


ticker = 'XTSE/BMO'
data = quandl.get(ticker, start_date='2020-12-31', end_date='2022-1-07', column_index = 4)
display(data)


# In[ ]:


type(data)


# In[ ]:


# close = data.iloc[:,0].to_numpy()
close = data['Close'].values


# In[ ]:


close


# In[ ]:


type(close)


# ### Using RSI as an example

# In[ ]:


from talib import RSI
output = RSI(close, timeperiod=14)
print(output)


# In[ ]:


output[-1]


# ### Plotting the RSI

# #### importing the plotting library

# In[ ]:


import matplotlib.pyplot as plt


# In[ ]:


plt.plot(output)
plt.axhline(y=30, color='r', linestyle='-')
plt.axhline(y=70, color='b', linestyle='-')


# In[ ]:


plt.plot(data)


# ### Using MACD as an example

# In[ ]:


from talib import MACD
macd, macdsignal, macdhist = MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)


# In[ ]:


macdhist[-1]


# In[ ]:


plt.plot(macd)

plt.plot(macdsignal)


# ### Real-time stock data
# 
# https://www.alphavantage.co/
# 
# ### Other technical indicators
# http://mrjbq7.github.io/ta-lib/func_groups/momentum_indicators.html
# 
