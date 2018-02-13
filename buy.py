# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 16:52:46 2018

@author: Edison Song
"""

import os
os.chdir("D:\\Python36\\python\\NBA")
import cex
import time
import datetime

class Strategy(object):
    def __init__(self, amt, auth, cost, re, symbol):
        self.syb = cex.price(symbol)
        self.amt = amt
        self.auth = auth
        self.cost = cost
        self.re = re
        self.symbol = symbol
    def buy(self):
        price=[]
        stop=0
        while(True):
            print("Watching@buy: {0}".format(symbol))
            if (stop==0):
#                k=0
#                for i in range(10):
#                    k = k+float(syb.last_price()['lprice'])
#                    time.sleep(60)
#                avg=k/10
                OC = []
                for i in range(2):
                    OC.append(float(syb.last_price()['lprice']))
                    time.sleep(599)
                if (OC[1] - OC[0])>0:
                    OC.append("G")
                else:
                    OC.append("R")
                    
#                avg=float(syb.last_price()['lprice'])
                if float(OC[1])<(cost*re/2):
                    price.append(OC)
                    if len(price) >= 3:
                        if ((price[-3][-1]=="R") & (price[-2][-1]=="R") & ((price[-1][-1])=="R")):
                            print("Over three 10min-K!!")
                            price2=[price[-1]]
                            while(True):
                                print("Watching@buy2: {0}".format(symbol))
#                                k2=0
#                                for i in range(10):
#                                    k2 = k2+float(syb.last_price()['lprice'])
#                                    time.sleep(60)
#                                avg2=k2/10
                                OC2 = []
                                for i in range(2):
                                    OC2.append(float(syb.last_price()['lprice']))
                                    time.sleep(599)
                                if (OC2[1] - OC2[0])>0:
                                    OC.append("G")
                                else:
                                    OC.append("R")
#                                avg2=float(syb.last_price()['lprice'])
                                price2.append(OC2)
                                if len(price2) >= 2:
                                    if((price2[-1][2]=="G") & ((price2[-1][1]-price2[-2][1])/price2[-2][1]>0.006)):
                                        buyP = float(syb.last_price()['lprice'])-0.01
                                        cex.private(auth.auth_request()).order_buy(symbol, "USD", amt, buyP)
                                        print("Order Place! Time: {0}".format(datetime.datetime.now().strftime('%Y%m%d-%H:%M:%S"')))
                                        print(buyP)
                                        stop=1
                                        break
#                                    elif (price2[-1]>price[-2]):
#                                        break
                                    del price2[0]
                        del price[0]
            elif(stop==1):
                break
    
    def sell(self):
        price=[]
        stop=0
        while(True):
            print("Watching@sell: {0}".format(symbol))
            if (stop==0):
#                k=0
#                for i in range(10):
#                    k = k+float(syb.last_price()['lprice'])
#                    time.sleep(60)
#                avg=k/10
                OC = []
                for i in range(2):
                    OC.append(float(syb.last_price()['lprice']))
                    time.sleep(599)
                if (OC[1] - OC[0])>0:
                    OC.append("G")
                else:
                    OC.append("R")
#                avg=float(syb.last_price()['lprice'])
                if float(OC[1])>(cost*(re+0.005)):
                    price.append(OC)
                    if len(price) >= 3:
                        if ((price[-3][2]=="G") & (price[-2][2]=="G") & (price[-1][2]=="G")):
                            print("Over three 10min-K!!")
                            price2=[price[-1]]
                            while(True):
                                print("Watching@sell2: {0}".format(symbol))
#                                k2=0
#                                for i in range(10):
#                                    k2 = k2+float(syb.last_price()['lprice'])
#                                    time.sleep(60)
#                                avg2=k2/10
                                OC2 = []
                                for i in range(2):
                                    OC2.append(float(syb.last_price()['lprice']))
                                    time.sleep(599)
#                                avg2=float(syb.last_price()['lprice'])
                                price2.append(OC2)
                                if len(price2) >= 2:
                                    if((price2[-1][2]=="R") & (price2[-2][1]-price2[-1][1])/price2[-2][1]>0.006):
                                        sellP = float(syb.last_price()['lprice'])+0.01
                                        cex.private(auth.auth_request()).order_sell(symbol, "USD", amt, sellP)
                                        print("Order Place! Time: {0}".format(datetime.datetime.now().strftime('%Y%m%d-%H:%M:%S"')))
                                        print(sellP)
                                        stop=1
                                        return sellP
#                                    elif (price2[-1]>price[-2]):
#                                        break
                                    del price2[0]
                        del price[0]
            elif(stop==1):
                break

if __name__ ==  '__main__':
    symbol = input("Symbol: ")
    cost = float(input("Cost Price: ")) #sell
    amt = float(input("Amount: "))
    re = (float(input("%: "))*0.01+1)       #sell
    fuc = input("buy/sell first: ")
    if fuc=="sell":
        mt = 1
    elif fuc == "buy":
        mt = 2
    else:
        mt=0.5
    print("Start")
    syb=cex.price(symbol)
    high=float(syb.ticker()["high"])
    low=float(syb.ticker()["low"])
    

    auth = cex.sign(apikey, secret, userid)
    
    while(True):
        if (mt%2)==1:
            cost = Strategy(amt, auth, cost, re, symbol).sell()
            mt+=1
        elif (mt%2)==0:
            cost = Strategy(amt, auth, cost, re, symbol).buy()
            mt+=1
        else:
            fuc = input("buy/sell first, Please: ")
            if fuc=="sell":
                mt = 1
            elif fuc == "buy":
                mt = 2
            else:
                mt=0.5
        print("Times: {0}".format(mt))
