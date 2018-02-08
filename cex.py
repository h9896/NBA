# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 23:56:06 2018

@author: Edison Song
"""

import requests
import json

import hmac
import hashlib
import time

class sign(object):
    def __init__(self, key, secret, userid):
        self.__username = userid
        self.__api_key = key
        self.__api_secret = secret
        
    def create_signature(self):  # (string key, string secret) 
        tamp = '{:.10f}'.format(time.time() * 1000).split('.')[0]
        string = tamp+self.__username+self.__api_key
        return tamp, hmac.new(self.__api_secret.encode(), string.encode(), digestmod=hashlib.sha256).hexdigest().upper()
    
    def auth_request(self):
        data={}
        stamp, signature = self.create_signature()
        data.update({'key': self.__api_key, 'signature': signature, 'nonce': stamp})
        return data

class price(object):
    def __init__(self, s1, s2 = "USD", s3=""):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
    def currency_limits(self):
        url="https://cex.io/api/currency_limits"
        resp = requests.get(url)
        json_data = json.loads(resp.text)
        if (json_data['ok']=='ok'):
            json_data = json_data['data']['pairs']
            return json_data
        else:
            return json_data
    def ticker(self):
        url="https://cex.io/api/ticker/{0}/{1}".format(self.s1,self.s2)
        resp = requests.get(url)
        if resp.ok:
            json_data = json.loads(resp.text)
            return json_data
        else:
            return "Error"
            
    def ticker_all(self):
        if self.s2 =="":
            url="https://cex.io/api/tickers/{0}".format(self.s1)
        else:
            url="https://cex.io/api/tickers/{0}/{1}".format(self.s1,self.s2)
        resp = requests.get(url)
        if resp.ok:
            json_data = json.loads(resp.text)
            if (json_data['ok']=='ok'):
                json_data = json_data['data']
                return json_data
            else:
                return json_data
        else:
            return "Error"
    
    def last_price(self):
        url="https://cex.io/api/last_price/{0}/{1}".format(self.s1,self.s2)
        resp = requests.get(url)
        if resp.ok:
            json_data = json.loads(resp.text)
            return json_data
        else:
            return "Error"
            
    def last_allprice(self):
        url="https://cex.io/api/last_prices/{0}/{1}/{2}".format(self.s1,self.s2,self.s3)
        resp = requests.get(url)
        if resp.ok:
            json_data = json.loads(resp.text)
            if (json_data['ok']=='ok'):
                json_data = json_data['data']
                return json_data
            else:
                return json_data
        else:
            return "Error"
            
    def OHCVL(self, date, size=""):
        url = "https://cex.io/api/ohlcv/hd/{0}/{1}/{2}".format(date,self.s1,self.s2)
        resp = requests.get(url)       
        if size == "hour":
            si = "1h"
        elif size == "day":
            si = "1d"
        else:
            si = "1m"
        if resp.ok:
            json_data = json.loads(resp.text)
            return json_data["time"], json_data["data"+si]
        else:
            return "Error"
            
class private(object):
    def __init__(self, auth):
        self.auth = auth
        
    def acc(self):
        url="https://cex.io/api/balance/"
        resp = requests.post(url, data=self.auth)
        return resp.text
        
    def order_buy(self, s1, s2, amount, price):
        url = "https://cex.io/api/place_order/{0}/{1}".format(s1,s2)
        orderplace=self.auth
        orderplace["type"]="buy"
        orderplace["amount"]=float(amount)
        orderplace["price"]=float(price)
        resp = requests.post(url, data=orderplace)
        return resp.text
        
    def order_sell(self, s1, s2, amount, price):
        url = "https://cex.io/api/place_order/{0}/{1}".format(s1,s2)
        orderplace=self.auth
        orderplace["type"]="sell"
        orderplace["amount"]=float(amount)
        orderplace["price"]=float(price)
        resp = requests.post(url, data=orderplace)
        return resp.text
