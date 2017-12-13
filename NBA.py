# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 20:18:34 2017

@author: Edison Song
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys
import os
import datetime

def crawler_csv(date, team):
    #Daily weather data
#    date="20171211"
#    team="MIA@MEM"
    url ="https://www.cbssports.com/nba/gametracker/boxscore/NBA_{0}_{1}/".format(date, team)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    body = soup.find_all('tr', {'class': 'total-row'})
    namelist = ["Guest", "Home"]
    dic = {} 
    for i in range(len(body)):
        temp = body[i].find_all('td',{'class': 'number-element'})
        p=[]
        for strtmp in temp[0:]:
            strtmp = strtmp.string
            p.append(strtmp)
        dic[namelist[i]] = p
    value=[]
    for i in namelist:
        FG, FGTotal = dic[i][8].split("/")
        threePT,threePTTotal = dic[i][9].split("/")
        FT, FTTotal = dic[i][10].split("/")
        newlist = [FG, FGTotal, threePT,threePTTotal, FT, FTTotal]
        for j in range(8):
            value.append(int(dic[i][j]))
        for k in newlist:
            value.append(int(k))
        value.append(int(dic[i][-2]))
    parameter = ["GUESTMIN","GUESTPTS","GUESTREB","GUESTAST","GUESTSTL","GUESTBLK","GUESTTO","GUESTPF","GUESTFG","GUESTFGTotal","GUEST3PT","GUEST3PTTotal","GUESTFT","GUESTFTTotal","GUESTFPTS","HOMEMIN","HOMEPTS","HOMEREB","HOMEAST","HOMESTL","HOMEBLK","HOMETO","HOMEPF","HOMEFG","HOMEFGTotal","HOME3PT","HOME3PTTotal","HOMEFT","HOMEFTTotal","HOMEFPTS"]
    tv = [value]    
    file = pd.DataFrame(tv, columns=parameter)
    file.to_csv(date+"_"+team+".csv", index = False)

def crawler_nocsv(date, team):
    #Daily weather data
#    date="20171211"
#    team="MIA@MEM"
    url ="https://www.cbssports.com/nba/gametracker/boxscore/NBA_{0}_{1}/".format(date, team)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    body = soup.find_all('tr', {'class': 'total-row'})
    namelist = ["Guest", "Home"]
    dic = {} 
    for i in range(len(body)):
        temp = body[i].find_all('td',{'class': 'number-element'})
        p=[]
        for strtmp in temp[0:]:
            strtmp = strtmp.string
            p.append(strtmp)
        dic[namelist[i]] = p
    value=[]
    for i in namelist:
        FG, FGTotal = dic[i][8].split("/")
        threePT,threePTTotal = dic[i][9].split("/")
        FT, FTTotal = dic[i][10].split("/")
        newlist = [FG, FGTotal, threePT,threePTTotal, FT, FTTotal]
        for j in range(8):
            value.append(int(dic[i][j]))
        for k in newlist:
            value.append(int(k))
        value.append(int(dic[i][-2]))
    return value
    
def crawler_schedule(team):
    #team="SA"
    fullname = {"ATL":"atlanta-hawks","BOS":"boston-celtics","BKN":"brooklyn-nets","CHA":"charlotte-hornets","CHI":"chicago-bulls","CLE":"cleveland-cavaliers","DAL":"dallas-mavericks","DEN":"denver-nuggets","DET":"detroit-pistons","GS":"golden-state-warriors","HOU":"houston-rockets","IND":"indiana-pacers","LAC":"los-angeles-clippers","LAL":"los-angeles-lakers","MEM":"memphis-grizzlies","MIA":"miami-heat","MIL":"milwaukee-bucks","MIN":"minnesota-timberwolves","NO":"new-orleans-pelicans","NY":"new-york-knicks","OKC":"oklahoma-city-thunder","ORL":"orlando-magic","PHI":"philadelphia-76ers","PHO":"phoenix-suns","POR":"portland-trail-blazers","SAC":"sacramento-kings","SA":"san-antonio-spurs","TOR":"toronto-raptors","UTA":"utah-jazz","WAS":"washington-wizards"}
    url = "https://www.cbssports.com/nba/teams/schedule/{0}/{1}/".format(team,fullname[team])
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    body = soup.find_all('table',{'class': 'data'})
    f1 = body[1].find_all('tr',{'class': 'row1'})
    f2 = body[1].find_all('tr',{'class': 'row2'})
    schedule=[]
    for temp in f1:
        f = temp.find_all('td')
        p = []
        for strtmp in f[0:2]:
            strtmp = strtmp.string
            p.append(strtmp)
        schedule.append(p)
    for temp in f2:
        f = temp.find_all('td')
        p = []
        for strtmp in f[0:2]:
            strtmp = strtmp.string
            p.append(strtmp)
        schedule.append(p)
    return schedule

def crawler_TeamData(team):
    today = datetime.date.today()
    days = datetime.timedelta(days = 0)
    schedule = crawler_schedule(team)
    strmonth = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    nextyear = ["01","02","03","04","05","06","07"]
    newschedule=[]
    tdf = []
    for i in schedule:
        mon = i[0][0:3]
        mon = strmonth[mon]
        day = i[0][-2:]
        temp = i[1]
        if ' ' in day:
            day = day.replace(' ', '0')
        if mon in nextyear:
            d = '2018'+mon+day
        else:
            d = '2017'+mon+day
        if temp[0] == '@':
            t = team+temp
        else:
            t = temp+'@'+team
        newschedule.append([d,t])
    for k in newschedule:
        h = today - datetime.date(int(k[0][0:4]),int(k[0][4:6]),int(k[0][6:]))
        if h >= days:
            try:
                tv = crawler_nocsv(k[0], k[1])
                tdf.append(tv)
            except:
                pass
            
    parameter = ["GUESTMIN","GUESTPTS","GUESTREB","GUESTAST","GUESTSTL","GUESTBLK","GUESTTO","GUESTPF","GUESTFG","GUESTFGTotal","GUEST3PT","GUEST3PTTotal","GUESTFT","GUESTFTTotal","GUESTFPTS","HOMEMIN","HOMEPTS","HOMEREB","HOMEAST","HOMESTL","HOMEBLK","HOMETO","HOMEPF","HOMEFG","HOMEFGTotal","HOME3PT","HOME3PTTotal","HOMEFT","HOMEFTTotal","HOMEFPTS"]
    df = pd.DataFrame(tdf, columns=parameter)        
    df.to_csv(str(today.year)+str(today.month)+str(today.day)+"_"+team+".csv", index = False)


def crawler_TeamData_nocsv(team):
    today = datetime.date.today()
    days = datetime.timedelta(days = 0)
    schedule = crawler_schedule(team)
    strmonth = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    nextyear = ["01","02","03","04","05","06","07"]
    newschedule=[]
    tdf = []
    for i in schedule:
        mon = i[0][0:3]
        mon = strmonth[mon]
        day = i[0][-2:]
        temp = i[1]
        if ' ' in day:
            day = day.replace(' ', '0')
        if mon in nextyear:
            d = '2018'+mon+day
        else:
            d = '2017'+mon+day
        if temp[0] == '@':
            t = team+temp
        else:
            t = temp+'@'+team
        newschedule.append([d,t])
    for k in newschedule:
        h = today - datetime.date(int(k[0][0:4]),int(k[0][4:6]),int(k[0][6:]))
        if h >= days:
            try:
                tv = crawler_nocsv(k[0], k[1])
                tdf.append(tv)
            except:
                pass
    return tdf

def crawler():
    today = datetime.date.today()
    fullname = ["ATL","BOS","BKN","CHA","CHI","CLE","DAL","DEN","DET","GS","HOU","IND","LAC","LAL","MEM","MIA","MIL","MIN","NO","NY","OKC","ORL","PHI","PHO","POR","SAC","SA","TOR","UTA","WAS"]
    df = []
    for i in fullname:
        tdf = crawler_TeamData_nocsv(i)
        df = df + tdf
    parameter = ["GUESTMIN","GUESTPTS","GUESTREB","GUESTAST","GUESTSTL","GUESTBLK","GUESTTO","GUESTPF","GUESTFG","GUESTFGTotal","GUEST3PT","GUEST3PTTotal","GUESTFT","GUESTFTTotal","GUESTFPTS","HOMEMIN","HOMEPTS","HOMEREB","HOMEAST","HOMESTL","HOMEBLK","HOMETO","HOMEPF","HOMEFG","HOMEFGTotal","HOME3PT","HOME3PTTotal","HOMEFT","HOMEFTTotal","HOMEFPTS"]
    df = pd.DataFrame(df, columns=parameter)        
    df.to_csv(str(today.year)+str(today.month)+str(today.day)+".csv", index = False)
    

#if __name__ == '__main__':
#    team = str(sys.argv[1])
#    print(team)
#    crawler_TeamData(team)
    
if __name__ == '__main__':
    crawler()
