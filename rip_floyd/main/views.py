from django.shortcuts import render
import pandas as pd
import calendar
import matplotlib.pyplot as plt
import calmap
import numpy as np
import urllib.request
from .models import Victims, Police_victim,News
from sklearn.linear_model import LinearRegression
from . import news_crawl
import threading
from datetime import datetime

# Create your views here.


def main(request):

    
    data = pd.DataFrame(list(Victims.objects.all().values()))
    data2 = pd.DataFrame(list(Police_victim.objects.all().values()))

    state = data['state']
    
    state_list = list(set(state))
    state_list_count = {}
    state_list_prob = {}

    for i in state_list:
        state_list_count[i]=0

    for i in range(0,len(data)):
        state_data = data['state'][i]
        if state_data in state_list:
            state_list_count[state_data]+=1
        
    for i, j in state_list_count.items():
        state_list_prob[i]=j/len(data)

    state_list_count2=sorted(state_list_count.items(), reverse=True, key=lambda item: item[1])
    x=[]
    y=[]
    for i in range(0,40):
        x.append(state_list_count2[i][0])
        y.append(state_list_count2[i][1])
    plt.figure(figsize=(10,5))
    plt.bar(x[0:40],y[0:40], color='red')
    plt.ylabel("Number of criminal's death")
    plt.xlabel('state')
    plt.savefig('C:/Users/acepi/Desktop/dbproject/dbwebprograming/rip_floyd/static/img/plot1.png')

    ##날짜 그래프

    # col1 = 'date'
    # date_list = list(set(data[col1]))
    # date_count = {}

    # for i in range(0, len(data)):
    #     date_data = data[col1][i]
    #     if date_data in date_count:
    #         date_count[date_data] += 1
    #     else:
    #         date_count[date_data] = 1
            
    # days=list(date_count.keys())
    # happens=list(date_count.values())
    # events = pd.Series(happens, index=days)

    # calmap.yearplot(events, year=2015)
    # plt.savefig('C:/Users/user/Desktop/dbproject/dbwebprograming/rip_floyd/static/img/plot2.png')

    ##인종별
    racial_list = list(set(data["race"]))
    racial_list_count = {}
    racial_unarmed_count = []
    white_count = 0
    unknown_count = 0
    black_count = 0
    hispanic_count = 0
    pacific_count = 0
    asian_count = 0

    for i in range(0,len(data)):
        racial_data = data["race"][i]
        if racial_data in racial_list_count:
            racial_list_count[racial_data]+=1
        else:
            racial_list_count[racial_data]=1

    for i in range(0, len(data)):
        if data["race"][i] == "White" and data["unarmed"][i] == "Unarmed":
            white_count += 1
        elif data["race"][i] == "Unknown race" and data["unarmed"][i] == "Unarmed":
            unknown_count += 1
        elif data["race"][i] == "Black" and data["unarmed"][i] == "Unarmed":
            black_count += 1
        elif data["race"][i] == "Hispanic" and data["unarmed"][i] == "Unarmed":
            hispanic_count += 1
        elif data["race"][i] == "Pacific Islander" and data["unarmed"][i] == "Unarmed":
            pacific_count += 1
        elif data["race"][i] == "Asian" and data["unarmed"][i] == "Unarmed":
            asian_count += 1

    racial_unarmed_list = [white_count,unknown_count,black_count,hispanic_count,pacific_count,asian_count]
    prob_list=[]
    for i in range(0,6):
        prob_list.append(racial_unarmed_list[i]/list(racial_list_count.values())[i])
    

    plt.figure(figsize=(10,5))
    plt.bar(list(racial_list_count.keys())[0:6],prob_list[0:6], color='red')
    plt.xlabel('Racial')
    plt.ylabel("number of criminal death's who unarmed by racial")
    plt.savefig('C:/Users/acepi/Desktop/dbproject/dbwebprograming/rip_floyd/static/img/plot3.png')

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
    plt.ylabel("number of police's death")
    plt.savefig('C:/Users/acepi/Desktop/dbproject/dbwebprograming/rip_floyd/static/img/plot4.png')
            
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

   
    y_pred=reg.predict(reg_x1)
    plt.xlabel('number of criminal deaths')
    plt.ylabel('number of police deaths')
    plt.scatter(reg_x1,reg_x2)
    plt.plot(reg_x1,y_pred)

    plt.savefig('C:/Users/acepi/Desktop/dbproject/dbwebprograming/rip_floyd/static/img/plot5.png')

    
    return render(request,'main.html')

def crawl(request):
    
    news_list = news_crawl.croller()
    now = datetime.now()
    now_time = now.strftime("%Y-%m-%d-%H")

    for i in news_list: 
        django_news = News()
        django_news.title = i.title
        django_news.timestamp = i.time_stamp
        django_news.img_url = i.img_url
        django_news.article_url = i.article_url
        django_news.save()
    all_news = News.objects.all()
    context = {'news':all_news, 'now':now_time}
    return render(request,'main.html', context)

