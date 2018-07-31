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
            btc = 0.05370521*float(i[1])
            b_btc = (float(i[1])-6266.865102)*0.05370521
            h_btc = (float(i[1])/6266.865102)
        elif i[0] == 'ETH/USD':
            eth = 2.26722000*float(i[1])
            b_eth = (float(i[1])-603.1431086)* 2.66022000
            h_eth = (float(i[1])/603.1431086)
        elif i[0] == 'BCH/USD':
            bch = 0.07449677*float(i[1])
            b_bch = (float(i[1])-3709.556)*0.07449677
            h_bch = (float(i[1])/3709.556)
        elif i[0] == 'XRP/USD':
            xrp = 260.000000*float(i[1])
            b_xrp = (float(i[1])-1.230573)*260.000000
            h_xrp = (float(i[1])/1.230573)
        elif i[0] == 'ZEC/USD':
            zec = 0.63993760*float(i[1])
            b_zec = (float(i[1])-544.5940901)*0.66194298
            h_zec = (float(i[1])/544.5940901)
    total = btc+eth+bch+xrp+zec
    b_total = b_btc+b_eth+b_bch+b_xrp+b_zec
    
	
    print('Total: '+str(total)+'\n')
    print('BTC: '+str(int(btc/total*100))+'%')
    print('ETH: '+str(int(eth/total*100))+'%')
    print('BCH: '+str(int(bch/total*100))+'%')
    print('XRP: '+str(int(xrp/total*100))+'%')
    print('ZEC: '+str(int(zec/total*100))+'%')
    print('Balance Total: '+str(b_total)+'\n')
    print('Balance BTC: '+str(b_btc))
    print('Balance BTC: '+str(int((h_btc-1)*100))+'%\n')
    print('Balance ETH: '+str(b_eth))
    print('Balance ETH: '+str(int((h_eth-1)*100))+'%\n')
    print('Balance BCH: '+str(b_bch))
    print('Balance BCH: '+str(int((h_bch-1)*100))+'%\n')
    print('Balance XRP: '+str(b_xrp))
    print('Balance XRP: '+str(int((h_xrp-1)*100))+'%\n')
    print('Balance ZEC: '+str(b_zec))
    print('Balance ZEC: '+str(int((h_zec-1)*100))+'%\n')

if __name__ == '__main__':
    while True:
        ss = input("Search:")
        if ss =="Y":
            us()
            #time.sleep(180)