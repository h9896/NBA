# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 09:30:20 2018

@author: H124036822
"""

import os
os.chdir("D:\\Python36\\python\\NBA")
import cex
import datetime

data={}
today=datetime.date.today()
eth=cex.price("ETH")
with open('eth.txt', 'w') as f:
    for i in range(1,31):
        days = datetime.timedelta(days = i)
        nam = (today-days).strftime('%Y%m%d')
        data = eth.OHCVL(nam,"min")
        date = str(data[0])
        data = "{"+date+":"+data[1]+"}\n"
        f.write(data)
        