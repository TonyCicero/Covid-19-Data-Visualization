import json
import requests
import time
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os
from ftpUpload import*

url = "https://api.covidtracking.com/v1/us/daily.json"
response = requests.get(url)
data = response.json()

timeFormat = "%Y%m%d"
dates=[]
pos=[]
death=[]
tests=[]
posRate=[]


script_dir = os.path.dirname(__file__)
results_dir = os.path.join(script_dir, "US/")
if not os.path.isdir(results_dir):
    os.makedirs(results_dir)

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



for day in data:
    dates.append(datetime.datetime.strptime(str(day["date"]),timeFormat))
    if(day['positiveIncrease']==None or day['positiveIncrease']==0 ):
         pos.append(0)
    else:
         pos.append(day['positiveIncrease'])

    if(day['deathIncrease']==None or day['deathIncrease']==0):
         death.append(0)
    else:
         death.append(day['deathIncrease'])

    if (day['totalTestResultsIncrease'] == None or day['totalTestResultsIncrease'] == 0):
        tests.append(0)
        posRate.append(0)
    else:
        tests.append(day['totalTestResultsIncrease'])
        posRate.append(day['positiveIncrease']/day['totalTestResultsIncrease'])

fig=plt.figure(figsize=(16,12))
ax,ax2,ax3,ax4=fig.subplots(4,1,sharex=True)
ax.bar(dates,pos, width=1, color='Gold', label = 'Cases')
ax.plot(dates, roll_avg(pos), color='DarkOrange', label = 'Cases 7-day Average')
ax3.plot(dates, roll_avg(posRate), color='orange', label = 'Positivity Rate 7-day Average')
ax3.bar(dates,posRate, width=1, color='Bisque', label = 'Positivity Rate')
ax2.bar(dates,death, width=1, color='salmon', label = 'Deaths')
ax2.plot(dates, roll_avg(death), color='red', label = 'Deaths 7-day Average')
ax4.plot(dates, roll_avg(tests), color='green', label = 'Tests 7-day Average')
ax4.bar(dates,tests, width=1, color='DarkSeaGreen', label = 'Tests')
#ax2.set_axisbelow(True)
#ax.set_ylim([0,0.2])
ax4.set_xlabel('Date')
ax4.set_ylabel('Tests')
ax3.set_xlabel('Date')
ax3.set_ylabel('Positivity Rate')
ax2.set_xlabel('Date')
ax2.set_ylabel('Deaths')
ax2.set_xlabel('Date')
ax.set_xlabel('Date')
ax.set_ylabel('Cases')
ax.set_title('US Covid-19')
myFmt = mdates.DateFormatter('%m-%d-%Y')
ax.xaxis.set_major_formatter(myFmt)
ax2.xaxis.set_major_formatter(myFmt)
ax3.xaxis.set_major_formatter(myFmt)
ax4.xaxis.set_major_formatter(myFmt)
ax.legend()
ax2.legend()
ax3.legend()
ax4.legend()
ax.yaxis.grid(color='gray', linestyle='dashed')
ax2.yaxis.grid(color='gray', linestyle='dashed')
ax3.yaxis.grid(color='gray', linestyle='dashed')
ax4.yaxis.grid(color='gray', linestyle='dashed')

fig.text(0.85, 0.00, 'Last 7-Day Positivity Rate: {0}%\n7-Day avg Cases: {1}\n7-Day avg Deaths:{2}'
             .format(round(avg(posRate)*100,2),round(avg(pos),2),round(avg(death),2)),
             fontsize=10, color='black',
             ha='left', va='bottom', alpha=0.9)
fig.text(0.0, 0.0, 'Created By Tony Cicero\nData Source: The COVID Tracking Project',fontsize=18, color='gray',ha='left', va='bottom', alpha=0.5)
plt.savefig('{0}/Covid-19_US.png'.format(results_dir))
plt.plot()
#plt.show()
sendFile(results_dir+"Covid-19_US.png","/US/Covid-19_US.png")
