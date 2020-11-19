import json
import requests
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from ftpUpload import *

states =[
             'AL','AK','AS','AZ','AR','CA','CO','CT','DE','DC','FL','GA',
             'GU','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA',
             'MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND',
             'MP','OH','OK','OR','PA','PR','RI','SC','SD','TN','TX','UT',
             'VT','VI','VA','WA','WV','WI','WY'
            ]



#average of last n days
def avg(a, n=7):
    x =0
    for i in range(n):
        x = x+ a[i]
    return x/n


def roll_avg(a, n=7) :
    a=np.flip(a)
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    ret[n-1:] = ret[n-1:]/n
    ret[:n-1]=a[:n-1]
    return np.flip(ret)


def get_data(state,d1,d2):
    global calls
    global cpm
    global startTime
    global data
    time.sleep(1)
    url = "https://api.covidtracking.com/v1/states/{0}/daily.json".format(state)
    response = requests.get(url)
    data = response.json()

    for day in data:
        
        dates.append(datetime.datetime.strptime(str(day["date"]),timeFormat))
        pos.append(day[d1])
        neg.append(day[d2])
        tot = day['totalTestResultsIncrease']
        tests.append(tot)
        if(tot > 0):
            posRate.append((day['positiveIncrease']/tot)*100)
        else:
            posRate.append(0)

def plot_data(state,L1,L2):

    fig=plt.figure(figsize=(16,8))
    ax,ax2=fig.subplots(2,1,sharex=True)
    #ax.scatter(dates, pos,s=1, color='b', label = L1)
    #ax.scatter(dates, neg,s=1, color='r', label = L2)
    #ax.bar(dates,tests, width=1, color='lime', label = 'Tests')
    ax.bar(dates,pos, width=1, color='cornflowerblue', label = L1)
    ax2.bar(dates,neg, width=1, color='salmon', label = L2)
    #ax.bar(dates,posRate, width=1, color='yellow', label = 'Positivity Rate')
    #ax.plot(dates, roll_avg(posRate), color='orange', label = 'Positivity Rate 7-day Average')
    #ax.plot(dates, roll_avg(tests), color='g', label = '{0} 7-day Average'.format('Tests'))
    #ax2.plot(dates, roll_avg(tests), color='g', label = '{0} 7-day Average'.format('Tests'))
    ax.plot(dates, roll_avg(pos), color='b', label = '{0} 7-day Average'.format(L1))
    ax2.plot(dates, roll_avg(neg), color='r', label = '{0} 7-day Average'.format(L2))
    ax.set_xlabel('Date')
    ax.set_ylabel('Cases')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Deaths')
    #ax.set_ylim(200, 2500)  # outliers only
    #ax2.set_ylim(0, 100)  # most of the data
    ax.legend()
    ax2.legend()
    ax.yaxis.grid(color='gray', linestyle='dashed')
    ax2.yaxis.grid(color='gray', linestyle='dashed')
    
    fig.text(0.85, 0.00, 'Last 7-Day Positivity Rate: {0}\n7-Day avg Cases: {1}\n7-Day avg Deaths:{2}'
             .format(round(avg(posRate),2),round(avg(pos),2),round(avg(neg),2)),
         fontsize=10, color='black',
         ha='left', va='bottom', alpha=0.9)
    ax.set_title('Covid-19 {0} {1}'.format(title,state.upper()))
    myFmt = mdates.DateFormatter('%m-%d-%Y')
    ax.xaxis.set_major_formatter(myFmt)
    ax2.xaxis.set_major_formatter(myFmt)
    
    fig.text(0.0, 0.0, 'Created By Tony Cicero\nData Source: The COVID Tracking Project',
         fontsize=18, color='gray',
         ha='left', va='bottom', alpha=0.5)
    plt.subplots_adjust(left=0.05, bottom=.1, right=.95, top=0.95, wspace=0, hspace=0)
    #plt.savefig('Images/Covid-19_{0}_{1}_{2}.png'.format(title,state.upper(),dates[0].strftime(timeFormat)))
    plt.savefig('{0}/Covid-19_State.png'.format(results_dir))
    plt.plot()
    #plt.show()
    plt.close()

for st in states:
    print("Current State: " + st)
    state=st
    dates =[]
    pos =[]
    neg =[]
    posRate=[]
    tests=[]

    timeFormat = "%Y%m%d"
    title="Daily Cases & Deaths"


    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, "States/{0}/".format(state.upper()))

    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)

    print("Getting Data")
    get_data(state,"positiveIncrease","deathIncrease")
    print("Creating Graph")
    plot_data(state,"Daily Positive","Daily Deaths")
    print("Uploading File")
    sendFile(results_dir+"Covid-19_State.png","/States/{0}/Covid-19_State.png".format(state))
    print("Done State: " + st)

