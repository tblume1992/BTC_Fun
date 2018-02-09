# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 11:54:12 2018

@author: t-blu
"""
import pandas as pd
data = pd.read_csv('C:\\Users\\t-blu\\Downloads\\btc_fun.csv',  delimiter=',')
trend = data[['Timestamp','Weighted_Price']]