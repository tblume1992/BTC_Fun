# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 19:15:33 2018

@author: t-blu
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
period = 120
price_change_window = 120
price_change_threshold = .2

#Import BTC Historical 1 minute Prices
'''Path to File Downloaded from Kaggle'''
master_link = pd.read_csv(PATH,  delimiter=',')
#Calculate Price Change during window
master_link['Difference'] = master_link['Weighted_Price'].diff(price_change_window)/master_link['Weighted_Price']
#Pull only values that are larger or equal to the price change threshold
master_link['Binary'] = np.where(master_link['Difference']>= price_change_threshold, 1,0)
#Create a binary on whether the threshold was met
binary_list = master_link.loc[master_link['Binary'] == 1].index.values
#Ensure that we only use price changes which have enough observations in the window
binary_list = binary_list[binary_list > period] 
#Build empty df to add data too
trend = pd.DataFrame(np.zeros((period, 1)))
#Loop to build a dataset of periods in which the price change was met 
count = 0
while count < len(binary_list):
    look = master_link.loc[:binary_list[count]]
    hourly_trend = look.tail(period)
    hourly_difference = pd.DataFrame(hourly_trend['Difference'])
    
    trend = [trend, hourly_difference]
    trend = np.column_stack(trend)
    trend = pd.DataFrame(trend)
    count += 1
#Drop first column of 0s
trend = trend.drop(trend.columns[0], axis=1)
#Replace a random outlier with 0
trend.replace(to_replace=-19715.5, value=0, inplace=True)
#plot all of periods...this graph can be a lot!
plt.figure(); trend.plot(legend=False);
#Transpose to get ready for clustering
trend = np.transpose(trend)
#Cluster...don't kill me for using kmeans Sam, I had the code handy in another script
#Didn't use an elbow plot or anything just because I was satisfied enough with the results
Kmeans = (KMeans(n_clusters= 4, init='k-means++', max_iter = 300).fit(trend))
#Add cluster grouping and get cluster averages
Labels = Kmeans.labels_
trend = np.transpose(trend)
trend.columns = [Labels]
averages = trend.mean(axis=1, level=0)
#Plot cluster profiles
plt.figure(); averages.plot(legend=False);
#Depends on the parameters but most big jumps seem to come from either breakout news or after large dips



