# -*- coding: utf-8 -*-

import pandas as pd
import calendar
import matplotlib.pyplot as plt
import calmap
import numpy as np
from sklearn.linear_model import LinearRegression
from .models import Victims, Police_victim

def dbplot():
    
    data = pd.read_excel("C:\\Users\\user\\Desktop\\death_criminal.xlsx")
    data2 = pd.read_excel("C:\\Users\\user\\Desktop\\death_police.xlsx")

    #state = data['State']
    state_data = Victims.objects.all()
    state_list =[]
    for i in state_data:
        state_list = i.state
    state = pd.DataFrame(state_list)

    state_list = list(set(state))
    state_list_count = {}
    state_list_prob = {}

    for i in state_list:
        state_list_count[i]=0

    for i in range(0,len(data)):
        state_data = data['State'][i]
        if state_data in state_list:
            state_list_count[state_data]+=1
        
    for i, j in state_list_count.items():
        state_list_prob[i]=j/len(data)

    state_list_count2=sorted(state_list_count.items(), reverse=True, key=lambda item: item[1])
    x=[]
    y=[]
    for i in range(0,20):
        x.append(state_list_count2[i][0])
        y.append(state_list_count2[i][1])
    plt.figure(figsize=(10,5))
    plt.bar(x[0:20],y[0:20], color='red')
    plt.xlabel('state')
    plt.savefig('C:/Users/user/Desktop/dbproject/dbwebprograming/rip_floyd/static/img/plot1.png')

    ##날짜 그래프

    col1 = 'Date of Incident (month/day/year)'
    date_list = list(set(data[col1]))
    date_count = {}

    for i in range(0, len(data)):
        date_data = data[col1][i]
        if date_data in date_count:
            date_count[date_data] += 1
        else:
            date_count[date_data] = 1
            
    days=list(date_count.keys())
    happens=list(date_count.values())
    events = pd.Series(happens, index=days)

    calmap.calendarplot(events)
    plt.savefig('C:/Users/user/Desktop/dbproject/dbwebprograming/rip_floyd/static/img/plot2.png')
    ##인종별
    racial_list = list(set(data["Victim's race"]))
    racial_list_count = {}
    for i in range(0,len(data)):
        racial_data = data["Victim's race"][i]
        if racial_data in racial_list_count:
            racial_list_count[racial_data]+=1
        else:
            racial_list_count[racial_data]=1

    plt.figure(figsize=(10,5))
    plt.bar(list(racial_list_count.keys())[0:4],list(racial_list_count.values())[0:4], color='red')
    plt.xlabel('Racial')
    plt.savefig('C:/Users/user/Desktop/dbproject/dbwebprograming/rip_floyd/static/img/plot3.png')

    ##경찰들 순직사건 주별로
    
    police_list_count={}
    for i in range(0, len(data2)):
        data2['state'][i]=data2['state'][i].split(', ')[1]
        
    for i in range(0, len(data2)):
        info=data2['state'][i]
        if info in police_list_count:
            police_list_count[info]+=1
        else:
            police_list_count[info]=1

    police_list_count2=sorted(police_list_count.items(), reverse=True, key=lambda item: item[1])
    x2=[]
    y2=[]
    for i in range(0,20):
        x2.append(police_list_count2[i][0])
        y2.append(police_list_count2[i][1])



    plt.figure(figsize=(10,5))
    plt.bar(x2[0:20], y2[0:20], color='red')
    plt.xlabel('State')
    plt.savefig('C:/Users/user/Desktop/dbproject/dbwebprograming/rip_floyd/static/img/plot4.png')
            
    ##경찰들의 총기순직사건과 범죄자들의 과잉진압 사건 회귀분석

    x1_value=[]  #state별 범죄사망자
    x2_value=[]  #state별 경찰사망자
    for i in state_list:
        x1_value.append(state_list_count.get(i))
        x2_value.append(police_list_count.get(i))
        
    reg_x1 = pd.DataFrame(x1_value, index=state_list, columns=['events'])
    reg_x2 = pd.DataFrame(x2_value, index=state_list, columns=['events'])    
    reg_x2=reg_x2.fillna(0)
    reg=LinearRegression()
    reg.fit(reg_x1,reg_x2)    

    r2=reg.score(reg_x1,reg_x2)
    y_pred=reg.predict(reg_x1)

    plt.scatter(reg_x1,reg_x2)
    plt.plot(reg_x1,y_pred)
    plt.savefig('C:/Users/user/Desktop/dbproject/dbwebprograming/rip_floyd/static/img/plot5.png')

dbplot()