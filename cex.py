# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 23:56:06 2018

@author: Edison Song
"""

import requests
import json

import hmac
import hashlib
import datetime

def currency_limits():
    url="https://cex.io/api/currency_limits"
    resp = requests.get(url)
    json_data = json.loads(resp.text)
    if (json_data['ok']=='ok'):
        json_data = json_data['data']['pairs']
        return json_data
    else:
        return json_data
def ticker(s1,s2):
    url="https://cex.io/api/ticker/{0}/{1}".format(s1,s2)
    resp = requests.get(url)
    if resp.ok:
        json_data = json.loads(resp.text)
        return json_data
    else:
        return "Error"
        
def ticker_all(s1="USD",s2=""):
    if s2 =="":
        url="https://cex.io/api/tickers/{0}".format(s1)
    else:
        url="https://cex.io/api/tickers/{0}/{1}".format(s1,s2)
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

def last_price(s1,s2):
    url="https://cex.io/api/last_price/{0}/{1}".format(s1,s2)
    resp = requests.get(url)
    if resp.ok:
        json_data = json.loads(resp.text)
        return json_data
    else:
        return "Error"
        
def last_allprice(s1="USD",s2="",s3=""):
    url="https://cex.io/api/last_prices/{0}/{1}/{2}".format(s1,s2,s3)
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
def create_signature(key, secret):  # (string key, string secret) 
    timestamp = int(datetime.datetime.now().timestamp())  # UNIX timestamp in seconds
    string = "{0}{1}".format(timestamp, key)
    return timestamp, hmac.new(secret.encode(), string.encode(), hashlib.sha256).hexdigest()

def auth_request(key, secret):
    timestamp, signature = create_signature(key, secret)
    data=json.loads(json.dumps({'key': key, 'signature': signature, 'nonce': timestamp}))
    return data

def acc(key,secret):
    url="https://cex.io/api/balance/"
    resp = requests.post(url, json.dumps(auth_request(key, secret)))
    return resp.text

data = currency_limits()

dd = ticker_all()

d = last_price('BTC','USD')

kk = acc('9qp1v0GQL0RXtWfUO24y1TkmWQ' )

