#!/usr/bin/env python
# coding: utf-8

# In[209]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import statsmodels.formula.api as smf
get_ipython().run_line_magic('matplotlib', 'inline')


# In[187]:


pwd


# In[188]:


trying= pd.read_excel('Q-5.xlsx', sheet_name= 'clean', index_col=0, parse_dates=True)
trying


# In[189]:


data= trying[trying.columns[11:18]]
pd.DataFrame(data)


# In[190]:


data.info()


# In[191]:


data['Vix Price']=pd.to_numeric(data['Vix Price'].astype(str).str.strip(),errors='coerce')
data['sentiment']=pd.to_numeric(data['sentiment'].astype(str).str.strip(),errors='coerce')
data.info()


# In[192]:


data["Vix Price"].hist(color="k", alpha=0.5, bins=50)


# In[193]:


data["sentiment"].hist(color="k", alpha=0.5, bins=50)


# In[194]:


data["Unemployment"].hist(color="k", alpha=0.5, bins=50)


# In[195]:


data["inflation"].hist(color="k", alpha=0.5, bins=50)


# In[196]:


data['Chg_inflation']=data['inflation'].diff()
data['Chg_sentiment']=data['sentiment'].diff()
data['Chg_Vix']=data['Vix Price'].diff()


# In[197]:


data


# In[198]:


timeSelector = data.columns[1]
timeSelector


# In[199]:


grouped_data = data.groupby([timeSelector])


# In[200]:


T0 = data.loc[data[timeSelector]==0,"Chg_Vix"]
T1 = data.loc[data[timeSelector]==1,"Chg_Vix"]
Ts1 = data.loc[data[timeSelector]==-1,"Chg_Vix"]
T5 = data.loc[data[timeSelector]==5,"Chg_Vix"]
Ts5 = data.loc[data[timeSelector]==-5,"Chg_Vix"]

T0_Ts5 = T0-Ts5
Ts1_T0=Ts1-T0
T1_T5 = T1-T5


# In[201]:


T0 = data.loc[data[timeSelector]==0,"Chg_inflation"]
T1 = data.loc[data[timeSelector]==1,"Chg_inflation"]
Ts1 = data.loc[data[timeSelector]==-1,"Chg_inflation"]
T5 = data.loc[data[timeSelector]==5,"Chg_inflation"]
Ts5 = data.loc[data[timeSelector]==-5,"Chg_inflation"]

InT0_Ts5 = T0-Ts5
InTs1_T0=Ts1-T0
InT1_T5 = T1-T5


# In[202]:


T0 = data.loc[data[timeSelector]==0,"Chg_sentiment"]
T1 = data.loc[data[timeSelector]==1,"Chg_sentiment"]
Ts1 = data.loc[data[timeSelector]==-1,"Chg_sentiment"]
T5 = data.loc[data[timeSelector]==5,"Chg_sentiment"]
Ts5 = data.loc[data[timeSelector]==-5,"Chg_sentiment"]
seT0_Ts5 = T0-Ts5
seTs1_T0=Ts1-T0
seT1_T5 = T1-T5


# In[203]:


T0 = data.loc[data[timeSelector]==0,"Unemployment"]
T1 = data.loc[data[timeSelector]==1,"Unemployment"]
Ts1 = data.loc[data[timeSelector]==-1,"Unemployment"]
T5 = data.loc[data[timeSelector]==5,"Unemployment"]
Ts5 = data.loc[data[timeSelector]==-5,"Unemployment"]

UnT0_Ts5 = T0-Ts5
UnTs1_T0=Ts1-T0
UnT1_T5 = T1-T5


# In[206]:


vix_df= pd.concat([T0_Ts5, Ts1_T0,T1_T5], axis=1)
inf_df=pd.concat([InT0_Ts5, InTs1_T0,InT1_T5], axis=1)
sent_df=pd.concat([seT0_Ts5, seTs1_T0,seT1_T5], axis=1)
uem_df=pd.concat([UnT0_Ts5, UnTs1_T0,UnT1_T5], axis=1)
Dataset1= pd.concat([InT0_Ts5,seT0_Ts5,UnT0_Ts5,T0_Ts5 ], axis=1)
Dataset2= pd.concat([InTs1_T0,seTs1_T0,UnTs1_T0,Ts1_T0], axis=1)
Dataset3= pd.concat([InT1_T5,seT1_T5,UnT1_T5,T1_T5], axis=1)


# In[216]:


reg1= smf.ols('T0_Ts5~ InT0_Ts5+seT0_Ts5+UnT0_Ts5+InT0_Ts5:seT0_Ts5+seT0_Ts5:UnT0_Ts5',data= Dataset1).fit()
reg1.summary()


# In[217]:


reg2= smf.ols('Ts1_T0~ UnTs1_T0+seTs1_T0+InTs1_T0+InTs1_T0:seTs1_T0+seTs1_T0:UnTs1_T0',data= Dataset1).fit()
reg2.summary()


# In[218]:


reg3= smf.ols('T1_T5~ UnT1_T5+seT1_T5+InT1_T5+InT1_T5:seT1_T5+seT1_T5:UnT1_T5',data= Dataset1).fit()
reg3.summary()

