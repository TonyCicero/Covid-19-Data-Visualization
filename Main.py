import json
import requests
import time
import datetime
import USData as US
import StateData as State
import ftpUpload as ftp

timeFormat = "%Y%m%d"
url = "https://api.covidtracking.com/v1/us/daily.json"
date = datetime.datetime.now().strftime(timeFormat)
dataDate =''

def check():
    global dataDate
    print("Local Date: " + date)
    response = requests.get(url)
    data = response.json()
    dataDate = str(data[0]['date'])
    print ("Data Date: "+dataDate)

def main():
    check()
    while(date != dataDate):
        print ("Data Not Ready")
        time.sleep(5*60)
        check()
    print ("ok")
    ftp.connect()
    US.USMain()
    State.StateMain()

if __name__ == "__main__":
    main()
