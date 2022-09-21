#!/usr/bin/env python
# coding: utf-8

# # MGFD25 Assignment 2: 
# ## Predicting Loan Defaults with a Machine Learning Credit Model

# During the coding class, I showed you the basic analytic process from beginning to end, using the simplified Lending Club dataset from Kaggle.  For your assignment, you will repeat the analytic process for a larger dataset, provided by the book “Machine Learning in Business: An introduction to the world of data science” by Prof. John C. Hull.  Use this Jupyter Notebook to import the dataset(Download the dataset [HERE](https://www-2.rotman.utoronto.ca/~hull/MLThirdEditionFiles/lending_clubFull_Data_Set.xlsx) and the data descriptions [HERE](https://www-2.rotman.utoronto.ca/~hull/MLThirdEditionFiles/LendingClubLogisticRegression/lendingclub_datadictionary.xlsx)).  Follow the steps provided in the notebook and answer the following questions within the Notebook in Markdown format.  You are required to submit the completed notebook file with the outputs to Quercus by the due date. 

# ## Part 1: Data exploration (45%)

# ### Let's import the data file (2%)

# In[ ]:


# First we will import Panadas and other useful libraries
import os
import numpy as np
import pandas as pd


# In[ ]:


# Let's read the data file into a Pandas dataframe


# ### Initial Exploration (8%)
# 
# Data exploration is a very critical step in developing your predicting model.  This exercise allows us to get familiar with the dataset and relate it to the business problem that we are trying to solve.
# 
# In the assignment notebook, show the function and its output for:
# 1.	Taking a sneak peek at the first few rows of the dataset.
# 2.	Finding out the total rows and columns of the dataset.
# 3.	Showing a list of column names.
# 4.	Showing the different data type at each column(attributes).

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


#Add more cells if needed


# ### Univariate Analysis (20%)
# I only went over 3 features in my example code.  With the bigger dataset, repeat the steps to review all features and the target.  You will repeat the univariate analysis to get familiar with the all the features and the target.
# 
# Select up to 10 features that you think are critical for the model to produce promising predictions.  For each feature, briefly describe the data based on questions below(if applicable).  I accept point-form and please type your answers as “Markdown” within the notebook.
# Here are some questions that you'll ask when you are going through each column:
# * What is the data type of this feature?
# * Are there missing or duplicated data?
# * How is the data distributed? Are there any interesting patterns? Skewness?
# * Are there data outliers?
# * Is the data balanced?

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


#Add more cells if needed


# ### Bivariate Analysis (15%)
# Create a correlation matrix and a pair scatter plot for the 10 features you have selected.
# 
# By looking at the heatmap and the scatterplot, what conclusion can you draw? Are there any high/low correlations that jump out? Do they make sense? We will incorporate this thinking into our next stage in 'Feature selection'. Note that only continuous variables are shown. We can also incorporate categorical variables into the scatter plot, but we'll have to do some data transformation. We will do that in the Data cleaning part, and you may re-run the scatter plot after the transformation.
# 
# Use “Markdown” and type within the notebook, list out 5 observations that you think are interesting and stood out.  
# 

# In[ ]:





# In[ ]:


#Add more cells if needed


# ## Part 2: Data Preparation (20%)

# ### Data Cleaning (15%)

# This is the part where we make changes to the dataset so that it can feed nicely into the Machine Learning Models. Data cleaning usually involves at least one of the below processes: Dealing with inconsistent recording
# * Removing unwanted observations
# * Removing duplicates
# * Investigating outliers
# * Dealing with missing items
# 
# Use “Markdown” and type within the notebook.  Walk me through what you’ve done to prepare your dataset for the next step.  There is no right or wrong answer here.  Your grade will be based upon the reasons for such action and the clarity of communication.

# In[ ]:





# In[ ]:


#Add more cells if needed


# ### Splitting data into training data and test data (5%)
# Before we feed the clean dataset into the model, we will split the dataset into training data and testing data. The ML model will train on the training dataset and we will observe the model accuracy by feeding test data into the model for predicted targets.
# 
# In general, we will split the dataset 70/30. 70% of data will be used as training data and 30% for testing.
# 
# Show your code and the total counts of instances(observations) from the training set and the test set.
# 

# In[ ]:





# In[ ]:





# In[ ]:


#Add more cells if needed


# ## Part 3: Create your own prediction model (35%)

# ### Modelling (5%)
# In the coding class, I showed you how data could be cleaned and organized.  The data is then used in a decision tree classifier.  As you can see in my example, the result is quite disappointing, with only 27% specificity.  You may try different machine learning models here, but you’ll only need to submit one.

# In[ ]:





# In[ ]:





# ### Evaluation (15%)
# Show the confusion matrix and the value for sensitivity and specificity.  Briefly describe your model performance.  Are you satisfied with the model you have selected?  If not, explain what may cause the underperformance and how would you suggest improving it.

# In[ ]:





# In[ ]:





# ### Improving the Model (15%)
# Feature selection is a process of selecting a subset of features to use in model training, aka subset selection. Instead of feeding all the features into the model, can you try different subsets of features and see whether you can improve the model's predictive performance?
# Here are some hints for you to try:
# * If two features are highly correlated, some algorithms will perform badly. Try to remove one and keep the other
# * Include new features that were not included previously
# * Remove useless features
# * Remove features with zero variance or low variance
# * Remove features that are not at all correlated with target
# * Try combinations of the above or combinations of different subsets
# 
# Run the ML model with at least 3 different feature selections combinations. Show your code and model performance for each trial.
# 
# *Please note that your specificity can only be improved by feature selections and feature engineering.
# 
# **OR you may attempt to finetune the parameters of [decision trees](https://scikit-learn.org/stable/modules/tree.html)  or even try [other ML models](https://scikit-learn.org/stable/supervised_learning.html).  However, this is outside of the scope of this course.
# 

# In[ ]:





# In[ ]:




