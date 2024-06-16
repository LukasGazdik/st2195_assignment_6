#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 18:44:36 2024

@author: lukasgazdik
"""

import os
os.chdir("/Users/lukasgazdik/Documents/MyDirectoryPy/MyProject/Assignments/6")

print(os.getcwd())

#Read and review fx and speeches csv files

import pandas as pd

fx = pd.read_csv('fx.csv', na_values =['-'])

#Remove NaA Values

fx.dropna(inplace=True)

print(fx.head)

#When reading speeches csv file it is important to add that values are separate by "|" rathern than "," into the code

speeches = pd.read_csv('speeches.csv', sep = '|')

#Replace "|" with ","

print(speeches.head)

#Remove NaA Values

speeches.dropna(inplace=True)

#Review column titles only 

print(fx.columns.tolist())
print(speeches.columns.tolist())

#Remove columns titled other than date and contents in speeches dataframe and order by date

speeches = speeches[['date','contents']]
speeches = speeches.groupby("date")['contents'].apply(lambda x: " ".join(x.astype(str))).reset_index()
print(speeches.head)
print(speeches.columns.tolist())

#Remove column TIME PERIOD in fx dataframe

fx = fx[['DATE','US dollar/Euro (EXR.D.USD.EUR.SP00.A)']]

#Rename fx dataframe columns

fx.columns = ["date","exchange_rate"]


#Merge the data frames based on date column

merged_df = pd.merge(fx, speeches, on ='date', how = 'left')

#Review merged dataframe 

print(merged_df.head)

#Data type check

merged_df.dtypes

#Standardise the data format for date column

merged_df['date'] = pd.to_datetime(merged_df['date'])

#Rearrange by date column

merged_df = merged_df.sort_values(by='date', ascending=False)

#Set index as date column

merged_df.set_index('date', inplace = True)

#Plot data 

merged_df.plot()

#Look up an exchange rate higher than 1

merged_df[merged_df.exchange_rate > 1.0]

#Data frame insight 

merged_df.describe()

#Look up missing data

merged_df.isna().sum()

#Fill in the exchange rate with the latest information available

merged_df.fillna(method='bfill', inplace=True)

#An exchange rate return calculation 

merged_df['return'] = (merged_df.exchange_rate.diff(-1)/merged_df.exchange_rate)*100

#Return 0 if exchange rate greater than 0.5% and 1 otherwise

merged_df['good_news'] = (merged_df['return'] > 0.5).astype(int)

#Add variable "good_news" and "bad_news"

merged_df['good_news'] = (merged_df['return'] > 0.5).astype(int)
merged_df['bad_news'] = (merged_df['return'] < -0.5).astype(int)

#Date frame insight

merged_df.describe()

#Remove NaA 

merged_df.dropna(inplace=True)
merged_df.isna().sum()

#Scan and separate contents related to good and bad news 

good_contents = merged_df.contents[merged_df.good_news == 1].str.cat(sep=' ')
bad_contents = merged_df.contents[merged_df.bad_news == 1].str.cat(sep=' ')

#Load the most common stop words listed in the txt file 
stop_words = set(pd.read_csv("stopwords.txt", header=None).iloc[:,0].tolist())

#Scan for the most common words excluding stop words associated with good and bad news 

import string
import collections

def get_word_freq(contents, stop_words, num_words):
    freq = dict()

    for word in contents.split():
        word = word.strip(string.punctuation+'-')
        word = word.lower()
        if word not in stop_words and len(word):
            if word in freq:
                freq[word] += 1
            else:
                freq[word] = 1
                
    freq = dict(sorted(freq.items(), key = lambda item: -item[1]))
    return list(freq.keys())[:num_words]

good_indicators = get_word_freq(good_contents, stop_words, num_words = 20)
bad_indicators = get_word_freq(bad_contents, stop_words, num_words = 20)

good_indicators

bad_indicators




