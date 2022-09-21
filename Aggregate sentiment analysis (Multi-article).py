#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Assignment-4:-Sentiment-Anaysis" data-toc-modified-id="Assignment-4:-Sentiment-Anaysis-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Assignment 4: Sentiment Anaysis</a></span></li><li><span><a href="#Sample-code" data-toc-modified-id="Sample-code-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Sample code</a></span><ul class="toc-item"><li><span><a href="#Economic-Sentiment-Analysis" data-toc-modified-id="Economic-Sentiment-Analysis-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>Economic Sentiment Analysis</a></span><ul class="toc-item"><li><span><a href="#Company-Sentiment-Anlaysis" data-toc-modified-id="Company-Sentiment-Anlaysis-2.1.1"><span class="toc-item-num">2.1.1&nbsp;&nbsp;</span>Company Sentiment Anlaysis</a></span></li></ul></li></ul></li><li><span><a href="#----Assignment-Begins-Here----" data-toc-modified-id="----Assignment-Begins-Here-----3"><span class="toc-item-num">3&nbsp;&nbsp;</span>--- Assignment Begins Here ---</a></span><ul class="toc-item"><li><span><a href="#Select-20-different-articles-and-store-them-in-Python-list-or-any-iterable-object-of-your-choice.-I-recommend-that-you-use-a-unique-source." data-toc-modified-id="Select-20-different-articles-and-store-them-in-Python-list-or-any-iterable-object-of-your-choice.-I-recommend-that-you-use-a-unique-source.-3.1"><span class="toc-item-num">3.1&nbsp;&nbsp;</span>Select 20 different articles and store them in Python list or any iterable object of your choice. I recommend that you use a unique source.</a></span></li><li><span><a href="#Compute-the-sentiment-score-for-each-article,-store-your-results-in-a-pandas-DataFrame-where-the-index-is-the-date-and-the-column-stores-the-sentiment-score" data-toc-modified-id="Compute-the-sentiment-score-for-each-article,-store-your-results-in-a-pandas-DataFrame-where-the-index-is-the-date-and-the-column-stores-the-sentiment-score-3.2"><span class="toc-item-num">3.2&nbsp;&nbsp;</span>Compute the sentiment score for each article, store your results in a pandas DataFrame where the index is the date and the column stores the sentiment score</a></span></li><li><span><a href="#Plot-your-sentiment-scores" data-toc-modified-id="Plot-your-sentiment-scores-3.3"><span class="toc-item-num">3.3&nbsp;&nbsp;</span>Plot your sentiment scores</a></span></li><li><span><a href="#Add-a-new-column-to-the-DataFrame-containing--the-stock-prices-and-returns-on-that-day-using-Yahoo-Finance" data-toc-modified-id="Add-a-new-column-to-the-DataFrame-containing--the-stock-prices-and-returns-on-that-day-using-Yahoo-Finance-3.4"><span class="toc-item-num">3.4&nbsp;&nbsp;</span>Add a new column to the DataFrame containing  the stock prices and returns on that day using Yahoo Finance</a></span></li><li><span><a href="#Question:--Can-sentiment-explain/correlated-with-your-daily-returns?-To-do-so,-run-a-regression-of-your-daily-returns-on-the-market-return,-one-day-lag-return,-and-the-sentiment-score." data-toc-modified-id="Question:--Can-sentiment-explain/correlated-with-your-daily-returns?-To-do-so,-run-a-regression-of-your-daily-returns-on-the-market-return,-one-day-lag-return,-and-the-sentiment-score.-3.5"><span class="toc-item-num">3.5&nbsp;&nbsp;</span>Question:  Can sentiment explain/correlated with your daily returns? To do so, run a regression of your daily returns on the market return, one day-lag return, and the sentiment score.</a></span></li></ul></li></ul></div>

# # Assignment 4: Sentiment Anaysis
# 
# - **Name:** Peter Silong Li
# - **Student ID:** 10049214544
# - **Section: ** 1
# 
# ** Grading:** This is a pass or fail assignment worth 3% towards your final grade.
# 
# ** You must provide a *clean* code.** Make sure the grader can follow each step of your analysis. Put comments to describe what you are doing (Using MARKDOWN or using #). Remove any lines of code that is not necessary. If you struggle on a question, that is OK, as long you show all the steps that you have taken and describe what is not working. *If your code is not clean and it is hard for the grader to understand what you are doing, you will fail.*
# 
# ** SUBMISSION of ASSIGNMENT ** 
# 
# ** You must print your code output. ** Save the Jupyter code in PDF. To do so, click on File->Download as->PDF. Or you can do, File->Print Preview.
# 
# -- Remove all the sample code. Keep your code only. Make sure you code works fully, from start to finish with no error message. In other words, if you close Jupyter, re-open your code, and press the PLAY button, does your code work fully with no error message? 
# 
# 
# **Objectives:**
#     - Conduct Textual Analysis
#     - Introduction to web crawling
#     - A trading strategy from sentiment
#   
# 
# 

# In[76]:


get_ipython().system('pip install yfinance')
import pandas as pd
import urllib.request
import requests
import string
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import yfinance as yf
get_ipython().run_line_magic('matplotlib', 'inline')


# In[86]:


# Load the Loughran and McDonald dictionnary
lm = pd.read_excel('C:\\Users\lipet\Desktop\mgdf40\Assignment_4\LM_Master_Dictionary.xlsx')

# get the lists of positive/negative words
lmpos = list(lm[lm.Positive!=0]['Word'])
lmneg = list(lm[lm.Negative!=0]['Word'])


# In[84]:


# this section of the notebook will contains helper classes/functions
# for web crawling

from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def get_article_body(article_url, body_html_element):
    """ This is a helper function that provides us with the body of an article
    article_url is the link to the article
    body_html_element is where the article body is stored
        news websites usually wrap their story's body in <p> tags which stand for paragraph
        to find out which tag the website you chose uses, you need to inspect the page (ctrl+shift+i)
    """
        
    # get the story
    page = requests.get(article_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # get all the text within the html element <p>
    # each paragraph will be an element of the returned list
    # note that what we got here is in HTML
    html_text = soup.find_all(body_html_element)
    
    # convert HTML to regular string
    stripped_text = []
    for t in html_text:
        t = strip_tags(str(t))
        stripped_text.append(t)
    
    return " ".join(stripped_text)


# In[ ]:


# load the stories. This file contains links to news articles about the U.S economy
nyt = pd.read_csv('NYT_20141001_20171231_us_and_unemployment.csv')
nyt = nyt[['date', 'url']]
nyt['date'] = pd.to_datetime(nyt['date'])


# In[83]:


# !!!!!Important!!!!!!:
# if this cell below is not running for you, it could be because the nltk data is not installed in your PC
# to fix this, uncomment the two lines of code in this cell and install corpus

import nltk
nltk.download('stopwords')
#nltk.download_shell() #<-- alternative solution if the prior line did not work


# In[91]:


# in these lists, we store the date, number of words, 
# number of positive words and number of negative words in each article

dates = []
nwords = []
nneg = []
npos = []

# in this block of code, we extract informations from each article to fill up
# the lists above
for index, article in nyt.iterrows():
       
    # let's use the helper function to provide us with the article body
    # New York Times wraps their body in the <p> HTML element. The website you use might be different
    article_body = get_article_body(article_url = article['url'], body_html_element = 'p')
    
    # convert all words to lower case
    article_body = article_body.lower()
    
    # remove non-letters (i.e., $ %)
    natural_lang_data = ''.join([x for x in article_body if x in string.ascii_letters + '\'- '])
    
    # before processing the natural language data, we need to remove stop words.
    # stop words are words like: about, that, this, and, or, etc...
    natural_lang_data = [x for x in natural_lang_data.split() if x not in stopwords.words('english')]
    
    # finally, we store the following data: 
    nwords.append(len(natural_lang_data)) # number of words
    npos.append(len([i for i in natural_lang_data if i.upper() in lmpos]))  # number of positive words
    nneg.append(len([i for i in natural_lang_data if i.upper() in lmneg]))  # number of negative words
    dates.append(article['date']) # the date


# In[92]:


# let's store our lists in a table:
sent = pd.DataFrame(data={'nwords':nwords, 'npos':npos, 'nneg':nneg}, index=dates)
sent.head()


# In[ ]:


# let's add a new column that stores the sentitment. See the code for the formula
sent['sent'] = (sent['npos'] - sent['nneg']) / sent['nwords']


# In[ ]:


# as you can see, news are mostly negative... That's what sells!
sent['sent'].plot()
plt.ylabel('sentiment score')
plt.axhline(0, c='r', ls='--')


# ### Company Sentiment Anlaysis

# In[ ]:


# My article of choice: 'Unfit' Uber loses London license over safety failures
url = "https://www.reuters.com/article/us-uber-britain-idUKKBN1XZ0VL"
neg_article_date = '2019-11-25'

# get the body text
article_body = get_article_body(article_url = url, body_html_element = 'p')

# convert all words to lower case
article_body = article_body.lower()

# remove non-letters (i.e., $ %)
natural_lang_data = ''.join([x for x in article_body if x in string.ascii_letters + '\'- '])

# remove stop words.
natural_lang_data = [x for x in natural_lang_data.split() if x not in stopwords.words('english')]
natural_lang_data.remove('-')

# process the data and get the sentiment
nwords = len(natural_lang_data) # number of dd
npos = len([i for i in natural_lang_data if i.upper() in lmpos])  # number of positive words
nneg = len([i for i in natural_lang_data if i.upper() in lmneg])  # number of negative words
sentiment_score = (npos - nneg) / nwords


# In[ ]:


print(sentiment_score)


# In[ ]:


# the sentiment is negative. Let's see how the stock performed around this dd
uber_returns['2019-11-20':'2019-11-30'].plot(kind='bar', title='Uber Daily Returns')
# Uber stock dropped by a little over 1% after this newsdddd


# # --- Assignment Begins Here ---
# You were hired to work as a Quantitative Analyst at prominent high-frequency trading firm (HFT).
# Your task is to find out whether trading on sentiment works or not. To show this, you are required to select 20 articles on 20 different days about a stock or an etf of your choice. You will then compute the sentiment score from each article.
# Since this is a prominent HFT firm, assume that your computer is the first to read the article and that you can trade on that news before anyone else.
# 
# Note: We list some steps here for you to follow if you would like. However, we encourage you to be creative and approach this in your own way :) 

# ## Select 20 different articles and store them in Python list or any iterable object of your choice. I recommend that you use a unique source. 
# Have a list that stores HTML articles = ['article1.com', 'article2.com', 'article3.com'...]
# 
# Example of news source: https://www.reuters.com/
# 
# You can choose macroeconomic news (e.g., monetary, etc.) or news for a given stock.

# In[82]:


#Loading 20 Apple Articles from CSV 
df = pd.read_csv('C:\\Users\\lipet\\Desktop\\mgdf40\\Assignment_4\\Article_list.csv')
df = df[['date','URL']]
df['date'] = pd.to_datetime(df['date'])
df


# ## Compute the sentiment score for each article, store your results in a pandas DataFrame where the index is the date and the column stores the sentiment score 

# In[88]:


dates = []
nwords = []
nneg = []
npos = []

for index, article in df.iterrows():
    article_body = get_article_body(article_url = url, body_html_element = 'p')

# convert all words to lower case
    article_body = article_body.lower()

# remove non-letters (i.e., $ %)
    natural_lang_data = ''.join([x for x in article_body if x in string.ascii_letters + '\'- '])

# remove stop words.
    natural_lang_data = [x for x in natural_lang_data.split() if x not in stopwords.words('english')]
    nwords.append(len(natural_lang_data))
    npos.append(len([i for i in natural_lang_data if i.upper() in lmpos]))  # number of positive words
    nneg.append(len([i for i in natural_lang_data if i.upper() in lmneg]))  # number of negative words
    dates.append(article['date'])



# In[89]:


#Making a table 
sentiment =  pd.DataFrame(data={'nwords':nwords, 'npos':npos, 'nneg':nneg}, index = dates)
sentiment


# In[90]:


sentiment['sentiment'] = (sentiment['npos']- sentiment['nneg']) / sentiment['nwords']
sentiment


# ## Plot your sentiment scores

# In[97]:


sentiment['sentiment'].plot()
plt.ylabel('sentiment score')
plt.axhline(0, c='r', ls='--')


# ## Add a new column to the DataFrame containing  the stock prices and returns on that day using Yahoo Finance
# *Note:* If the news you have chosen are macroeconomic news, you can use the broad stock market return.

# In[78]:


#I will use apple stock for this assignment
stock = ['AAPL']
benchmark = ['SPY']
data = {}
for s in stock + benchmark: 
        data[s] = yf.download(s, start = '2018-01-01', end = '2022-02-19', progress = False)
data
#creating dataframe
prc = pd.DataFrame()
for s in stock + benchmark:
    tmp = data[s][['Adj Close']]
    tmp.columns = [s]
    prc = pd.concat([prc, tmp], axis =1)
    prc = prc[prc.index.weekday <5]
prc


# ## Question:  Can sentiment explain/correlated with your daily returns? To do so, run a regression of your daily returns on the market return, one day-lag return, and the sentiment score.
# 
# $Ret_t = \alpha + \beta_1 R^M_t + \beta_2 Ret_{t-1} + \beta_3 Sent_t + \varepsilon_t$

# In[95]:


#To do this, we add AAPL return, SPY return, AAPL lag return, AAPL sentiment score
prc['AAPL_Return'] = prc['AAPL'].pct_change()
prc['SPY_Return'] = prc['SPY'].pct_change()
prc['AAPL_Lag_Return'] = prc['AAPL_Return'].shift()
prc['AAPL_Sentiment'] = sentiment['sentiment']
prc


# In[96]:


reg = smf.ols('AAPL_Return', data = prc).fit()
reg.summary()


# In[ ]:




