# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 20:18:34 2017
@author: Edison Song
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
#import sys
#import os
import datetime
class NBA_crawler():
    
###---------------------------------------------------------------------------------------------------------------------------------------------------###
    
    def game2csv(date, team):
#        Daily weather data
#        date="20171211"
#        team="MIA@MEM"
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
        
###---------------------------------------------------------------------------------------------------------------------------------------------------###
        
    def game(date, team):
#        Daily weather data
#        date="20171211"
#        team="MIA@MEM"
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
    
###---------------------------------------------------------------------------------------------------------------------------------------------------###

    def schedule(team):
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
    
###---------------------------------------------------------------------------------------------------------------------------------------------------###
        
    def tenday(team, aaa):
        today = datetime.date.today()
        days = datetime.timedelta(days = 0)
        tendays = datetime.timedelta(days = 10)
        schedule = NBA_crawler.schedule(team)
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
            if h >= days and h <= tendays:
                te = k[1].split("@")
                try:
                    if te[0] == team:
                        tv = NBA_crawler.game(k[0], k[1])
                        tdf.append(tv[0:15])
                    else:
                        tv = NBA_crawler.game(k[0], k[1])
                        tdf.append(tv[15:-1])
                except:
                    pass
        df = []
        for i in range(0,14):
            su = 0
            for j in range(len(tdf)):
                su = tdf[j][i] + su
            df.append(su/len(tdf))
        del df[0]
        del df[0]
        df = str(df).replace('[','')
        df = df.replace(']','')
        filename = aaa +"_teamtenday.txt"
        with open(filename, "w") as f:
            f.write(df)
            
###---------------------------------------------------------------------------------------------------------------------------------------------------### 
            
    def TeamData2csv(team):
        today = datetime.date.today()
        days = datetime.timedelta(days = 0)
        schedule = NBA_crawler.schedule(team)
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
                    tv = NBA_crawler.game(k[0], k[1])
                    tdf.append(tv)
                except:
                    pass
                
        parameter = ["GUESTMIN","GUESTPTS","GUESTREB","GUESTAST","GUESTSTL","GUESTBLK","GUESTTO","GUESTPF","GUESTFG","GUESTFGTotal","GUEST3PT","GUEST3PTTotal","GUESTFT","GUESTFTTotal","GUESTFPTS","HOMEMIN","HOMEPTS","HOMEREB","HOMEAST","HOMESTL","HOMEBLK","HOMETO","HOMEPF","HOMEFG","HOMEFGTotal","HOME3PT","HOME3PTTotal","HOMEFT","HOMEFTTotal","HOMEFPTS"]
        df = pd.DataFrame(tdf, columns=parameter)        
        df.to_csv(str(today.year)+str(today.month)+str(today.day)+"_"+team+".csv", index = False)
        
###---------------------------------------------------------------------------------------------------------------------------------------------------###    
    
    def TeamData(team):
        today = datetime.date.today()
        days = datetime.timedelta(days = 0)
        schedule = NBA_crawler.schedule(team)
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
                    tv = NBA_crawler.game(k[0], k[1])
                    tdf.append(tv)
                except:
                    pass
        return tdf
    
###---------------------------------------------------------------------------------------------------------------------------------------------------###    

    def crawler():
        today = datetime.date.today()
        fullname = ["ATL","BOS","BKN","CHA","CHI","CLE","DAL","DEN","DET","GS","HOU","IND","LAC","LAL","MEM","MIA","MIL","MIN","NO","NY","OKC","ORL","PHI","PHO","POR","SAC","SA","TOR","UTA","WAS"]
        df = []
        for i in fullname:
            tdf = NBA_crawler.TeamData(i)
            df = df + tdf
        parameter = ["GUESTMIN","GUESTPTS","GUESTREB","GUESTAST","GUESTSTL","GUESTBLK","GUESTTO","GUESTPF","GUESTFG","GUESTFGTotal","GUEST3PT","GUEST3PTTotal","GUESTFT","GUESTFTTotal","GUESTFPTS","HOMEMIN","HOMEPTS","HOMEREB","HOMEAST","HOMESTL","HOMEBLK","HOMETO","HOMEPF","HOMEFG","HOMEFGTotal","HOME3PT","HOME3PTTotal","HOMEFT","HOMEFTTotal","HOMEFPTS"]
        df = pd.DataFrame(df, columns=parameter)
        df.drop(["GUESTMIN","GUESTFPTS","HOMEMIN","HOMEFPTS"], axis=1)        
        df.to_csv(str(today.year)+str(today.month)+str(today.day)+".csv", index = False)
        
###---------------------------------------------------------------------------------------------------------------------------------------------------###
        
    def stats(team, aaa):
#        https://www.cbssports.com/nba/teams/stats/SA/san-antonio-spur
#        team="SA"
        fullname = {"ATL":"atlanta-hawks","BOS":"boston-celtics","BKN":"brooklyn-nets","CHA":"charlotte-hornets","CHI":"chicago-bulls","CLE":"cleveland-cavaliers","DAL":"dallas-mavericks","DEN":"denver-nuggets","DET":"detroit-pistons","GS":"golden-state-warriors","HOU":"houston-rockets","IND":"indiana-pacers","LAC":"los-angeles-clippers","LAL":"los-angeles-lakers","MEM":"memphis-grizzlies","MIA":"miami-heat","MIL":"milwaukee-bucks","MIN":"minnesota-timberwolves","NO":"new-orleans-pelicans","NY":"new-york-knicks","OKC":"oklahoma-city-thunder","ORL":"orlando-magic","PHI":"philadelphia-76ers","PHO":"phoenix-suns","POR":"portland-trail-blazers","SAC":"sacramento-kings","SA":"san-antonio-spurs","TOR":"toronto-raptors","UTA":"utah-jazz","WAS":"washington-wizards"}
        
        url = "https://www.cbssports.com/nba/teams/stats/{0}/{1}/".format(team,fullname[team])
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'lxml')
        body = soup.find_all('tr',{'class': 'row2'})
        body2 = soup.find_all('tr',{'class': 'row1'})
        total=[]
        opp = []
        for i in body:
            try:
                f = i.find_all('b')
                if f[0].string =="Totals":
                    tmp = [] 
                    for temp in f[1:]:
                        temp = temp.string
                        tmp.append(temp)
                    total.append(tmp)
                elif f[0].string == "Opponents":
                    tmp = [] 
                    for temp in f[1:]:
                        temp = temp.string
                        tmp.append(temp)
                    opp.append(tmp)
            except:
                pass
        for i in body2:
            try:
                f = i.find_all('b')
                if f[0].string == "Opponents":
                    tmp = [] 
                    for temp in f[1:]:
                        temp = temp.string
                        tmp.append(temp)
                    opp.append(tmp)
                elif f[0].string =="Totals":
                    tmp = [] 
                    for temp in f[1:]:
                        temp = temp.string
                        tmp.append(temp)
                    total.append(tmp)
            except:
                pass
        total0_1 = total[0]
        totalall = total[1]
        opp0_1 = opp[0]
        oppall = opp[1]
    
        much =int(totalall[0])
        x = [float(total0_1[6]), float(total0_1[7]), float(total0_1[8]), float(total0_1[9]), float(total0_1[10]), float(total0_1[11]), float(total0_1[1])*0.01*float(totalall[1])/much, float(totalall[1])/much, float(total0_1[2])*0.01*float(totalall[2])/much, float(totalall[2])/much, float(total0_1[3])*0.01*float(totalall[3])/much, float(totalall[3])/much]
        y = [float(opp0_1[6]), float(opp0_1[7]), float(opp0_1[8]), float(opp0_1[9]), float(opp0_1[10]), float(opp0_1[11]), float(opp0_1[1])*0.01*float(oppall[1])/much, float(oppall[1])/much, float(opp0_1[2])*0.01*float(oppall[2])/much, float(oppall[2])/much, float(opp0_1[3])*0.01*float(oppall[3])/much, float(oppall[3])/much]
        x = str(x).replace('[','')
        x = x.replace(']','')
        y = str(y).replace('[','')
        y = y.replace(']','')
        file = x +"\n"+y
        filename = aaa + "_teamstat.txt"
        with open(filename, "w") as f:
            f.write(file)
            
###---------------------------------------------------------------------------------------------------------------------------------------------------###

if __name__ == '__main__':
    NBA_crawler.stats("SA")
