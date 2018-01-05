# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 13:50:38 2018

@author: H124036822
"""

from bs4 import BeautifulSoup
import requests
import time
def us():
    url = "https://cex.io/btc-usd"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    body = soup.find_all('div', {'class': 'market-pair-row market-pair-row-value'})
    lis = []
    for i in body:
        k = i.find_all('span')
        li = []
        for j in k:
            li.append(j.string)
        lis.append(li)
    for i in lis:
        if i[0] == 'BTC/USD':
           btc = 0.01070521*float(i[1])
        elif i[0] == 'ETH/USD':
            eth = 0.52222000*float(i[1])
        elif i[0] == 'BCH/USD':
            bch = 0.07449677*float(i[1])
        elif i[0] == 'XRP/USD':
            xrp = 150.000000*float(i[1])
        elif i[0] == 'ZEC/USD':
            zec = 0.10000000*float(i[1])
    total = btc+eth+bch+xrp+zec
	
    print('Total: '+str(total)+'\n')
    print('BTC: '+str(int(btc/total*100))+'%')
    print('ETH: '+str(int(eth/total*100))+'%')
    print('BCH: '+str(int(bch/total*100))+'%')
    print('XRP: '+str(int(xrp/total*100))+'%')
    print('ZEC: '+str(int(zec/total*100))+'%')

if __name__ == '__main__':
	while True:
		us()
		time.sleep(180)