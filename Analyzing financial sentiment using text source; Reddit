#!/usr/bin/env python
# coding: utf-8

# In[2]:


#In this code, I used the praw api to crawl reddit and then the nltk.sentiment.vader package to return the article sentiment.
#The point of focus was r/CanadianInvestor (we wanted to see how canadians were feeling about the current financial market)
#Then I made a basic UI using tkinter to display the financial sentiment
import praw
import pandas as pd
import numpy as np
import string


# In[3]:


from IPython import display
import math
from pprint import pprint
import pandas as pd
import numpy as np
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='darkgrid', context='talk', palette='Dark2')


# In[4]:


reddit = praw.Reddit(
    client_id = 'YKD_KjZh0FVzg_JO9jOzRA',
    client_secret='mT3c3E-o9lh8JQwy3awrhKKZAf351Q',
    user_agent="testscript by u/mgfd25",
)



# In[5]:


lines = []
def get_reddit(x):    
    for submission in reddit.subreddit(x).top(limit=None):
        lines.append(submission.title)
    return lines


# In[6]:


on_list = ['CanadianInvestor', 'PersonalFinanceCanada', 'Ontario', 'Toronto', 'Ottawa']
qb_list = ['CanadianInvestor', 'PersonalFinanceCanada', 'Quebec', 'montreal']
bc_list = ['CanadianInvestor', 'PersonalFinanceCanada', 'britishcolumbia','vancouver' ]


# In[7]:


y = []
for sub in on_list:
    y.append(get_reddit(sub))


# In[8]:


flat = [val for sublist in y for val in sublist]


# In[9]:


q = []
for sub in qb_list:
    q.append(get_reddit(sub))


# In[10]:


flatq = [val for sublist in q for val in sublist]


# In[11]:


b = []
for sub in bc_list:
    b.append(get_reddit(sub))


# In[12]:


flatb = [val for sublist in b for val in sublist]


# In[13]:


from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk.corpus import stopwords
nltk.download('vader_lexicon')

sia = SIA()
results = []

for line in flat:
    pol_score = sia.polarity_scores(line)
    pol_score['headline'] = line
    results.append(pol_score)

pprint(results[:3], width=100)


# In[14]:


nltk.download('vader_lexicon')

siaq = SIA()
resultsq = []

for line in flatq:
    pol_score = siaq.polarity_scores(line)
    pol_score['headline'] = line
    resultsq.append(pol_score)

pprint(resultsq[:3], width=100)


# In[15]:


nltk.download('vader_lexicon')

siab = SIA()
resultsb = []

for line in flatb:
    pol_score = siab.polarity_scores(line)
    pol_score['headline'] = line
    resultsb.append(pol_score)

pprint(resultsb[:3], width=100)


# In[16]:


#Compound scores sentiment: Ranges from -1 (Extremely negative) to +1 (Extremely Positive)
df = pd.DataFrame.from_records(results)
dfq = pd.DataFrame.from_records(resultsq)
dfb = pd.DataFrame.from_records(resultsb)


# In[17]:


df['label'] = 0
df.loc[df['compound'] > 0.05, 'label'] = 1
df.loc[df['compound'] < -0.05, 'label'] = -1


# In[18]:


dfq['label'] = 0
dfq.loc[dfq['compound'] > 0.05, 'label'] = 1
dfq.loc[dfq['compound'] < -0.05, 'label'] = -1


# In[19]:


dfb['label'] = 0
dfb.loc[dfb['compound'] > 0.05, 'label'] = 1
dfb.loc[dfb['compound'] < -0.05, 'label'] = -1


# In[36]:


print("Positive headlines:\n")
pprint(list(df[df['label'] == 1].headline)[:40], width=200)

print("\nNegative headlines:\n")
pprint(list(df[df['label'] == -1].headline)[:20], width=200)


# In[37]:


ON_Neutral = df.label.value_counts()[0]
ON_Pos = df.label.value_counts()[1]
ON_Neg = df.label.value_counts()[-1]

QB_Neutral = dfq.label.value_counts()[0]
QB_Pos = dfq.label.value_counts()[1]
QB_Neg = dfq.label.value_counts()[-1]

BC_Neutral = dfb.label.value_counts()[0]
BC_Pos = dfb.label.value_counts()[1]
BC_Neg = dfb.label.value_counts()[-1]


# In[22]:


#on_overall = "Ontario Neutral score " + df.label.value_counts()[0] +  " Ontario Positive Score " + df.label.value_counts()[1] + "Ontario Negative Score" + df.label.value_counts()[2] 
ON_Overall=(f"Ontario neutral score {ON_Neutral}, Ontario positive score {ON_Pos}, Ontario negative score {ON_Neg}")

QB_Overall=(f"Quebec neutral score {QB_Neutral}, Quebec positive score {QB_Pos}, Quebec negative score {QB_Neg}")

BC_Overall=(f"BC neutral score {BC_Neutral}, BC positive score {BC_Pos}, BC negative score {BC_Neg}")
#print(df.label.value_counts(normalize=True) * 100)


# In[23]:


df['label'].hist(bins=5)
plt.show()


# In[24]:


# from tkinter import *
# from tkinter.ttk import Combobox
# window=Tk()
# lbl=Label(window, text="Select your target province and the program will begin the sentiment analysis.", fg='red', font=("Helvetica", 8))
# lbl.place(x=60, y=50)
# lbl2=Label(window, text="Welcome, TD FTP M&A Advisor", fg='red', font=("Helvetica", 16))
# lbl2.place(x=60, y=10)
# var = StringVar()
# var.set("one")
# data=("Ontario", "Quebec", "British Columbia")
# cb=Combobox(window, values=data)
# cb.place(x=60, y=150)

# lb=Listbox(window, height=5, selectmode='multiple')
# for num in data:
#     lb.insert(END,num)
# lb.place(x=250, y=150)

# #Button widget function
# btn=Button(window, text="Enter", fg='blue')
# btn.place(x=80, y=200)

# window.title('Hello Python')
# window.geometry("500x400+10+10")
# window.mainloop()


# In[41]:


from tkinter import *
from tkinter.ttk import Combobox
from tkinter import ttk
import tkinter as tk

root = tk.Tk()
window=root
lbl=Label(window, text="Select your target province and the program will begin the sentiment analysis.", fg='red', font=("Helvetica", 8))
lbl.place(x=60, y=300)
lbl2=Label(window, text="Welcome, TD FTP M&A Advisor", fg='red', font=("Helvetica", 16))
lbl2.place(x=60, y=100)
lbl3=Label(window,text='Retail Sentiment Analysis Prototype', fg = 'red', font=("Helvetica", 16))
lbl3.place(x=60,y=50)

def select(option):
    on_list = ['CanadianInvestor', 'PersonalFinanceCanada', 'Ontario', 'Toronto', 'Ottawa']
    qb_list = ['CanadianInvestor', 'PersonalFinanceCanada', 'Quebec', 'montreal', 'quebec']
    bc_list = ['CanadianInvestor', 'PersonalFinanceCanada', ]
    
    
    # Toplevel object which will
    # be treated as a new window
    newWindow = Toplevel(root)
 
    # sets the title of the
    # Toplevel widget
    if option == 'ON':
        newWindow.title("Ontario Sentiment")
        Label(newWindow,
          text =ON_Overall).pack()
    if option == 'QC':
        newWindow.title("Quebec Sentiment")
        Label(newWindow,
          text = QB_Overall).pack()
    if option == 'BC':
        newWindow.title("British Columbia Sentiment")
        Label(newWindow,
          text = BC_Overall).pack()
        
    # sets the geometry of toplevel
    newWindow.geometry("500x500")
 


ttk.Button(root, text='ON', command=lambda: select('ON')).place(x=200, y=200)
ttk.Button(root, text='QC',command=lambda: select('QC')).place(x=200, y=225)
ttk.Button(root, text='BC', command=lambda: select('BC')).place(x=200, y=250)

window.geometry("500x400+10+10")
root.mainloop()


# In[64]:


from tkinter import *
from PIL import Image, ImageTk

root = tk.Toplevel()
root.title("Title")

img = Image.open('ree.jpg')
bg = ImageTk.PhotoImage(img)

lbl = Label(root, image=bg)
lbl.place(x=0, y=0)

mainloop() 


# In[46]:


pwd


# In[ ]:




