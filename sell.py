# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 08:26:34 2018

@author: H124036822
"""
import os
os.chdir("D:\\Python36\\python\\NBA")
import cex
import time
import datetime

auth = cex.sign(apikey, secret, userid)

if __name__ ==  '__main__':
    cost = float(input("Cost Price: "))
    amt = float(input("Amount: "))
    re = float(input("%: "))*0.01
    print("Start")
    eth=cex.price("ETH")
    sellP=0
    
    price=[]
    
    while(True):
        print("Watching@")
#Sell
        if float(eth.last_price()['lprice'])>cost*(1.004+re):
            print("Over Cost!")
            price.append(float(eth.last_price()['lprice']))
            if len(price) >= 4:
                if (((price[-3]-price[-4])>0) & ((price[-2]-price[-3])>0) & ((price[-1]-price[-2])>0)):
                    print("Over three 10min-K!!")
                    price2=[price[-1]]
                    while(True):
                        print("Watching@2")
                        price2.append(float(eth.last_price()['lprice']))
                        if len(price2) >= 2:
                            if(((price2[-1]-price2[-2])<0) & ((price2[-2]-price2[-1])/price2[-2]>0.006)):
                                sellP = float(eth.last_price()['lprice'])-0.01
                                cex.private(auth.auth_request()).order_sell("ETH", "USD", amt, sellP)
                                print("Order Place! Time: {0}".format(datetime.date.today().strftime('%Y%m%d-%H:%M:%S"')))
                                break;
                        time.sleep(300)
                del price[0]
        else:
            price=[]
        if sellP>0:
            break;
        time.sleep(600)
