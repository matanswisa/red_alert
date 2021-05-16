import requests
import json
import datetime
import time

def orderText(text):
    return " ".join([txt[::-1] for txt in text.split(" ")][::-1])

def filterAlertsByDateTime(alerts):
    # currentTime[0] represents hours , index [1] represents minutes
    # for now im saving 5 minutes less than the current time.
    alerts_after_filter = []
    currentTime = splitTimeObj(datetime.datetime.now())
    currentDate = splitDateObj(datetime.datetime.now())
    for alert in alerts:
        alertDateTime = convertToDateTimeObj(alert["alertDate"])
        alertTime = splitTimeObj(alertDateTime)
        alertDate = splitDateObj(alertDateTime)
        if compareTimes(alertTime,currentTime) and compareDates(alertDate,currentDate):
            alert["data"] = orderText(alert["data"])
            alert["title"] = orderText(alert["title"])
            alerts_after_filter.append(alert)
    return alerts_after_filter

def compareTimes(alertTime,currentTime):
    return (alertTime[0] == currentTime[0] and alertTime[1] == currentTime[1])

def compareDates(alertDate,currentDate):
    return alertDate[0] == currentDate[0] and alertDate[1] == currentDate[1] and alertDate[2] == currentDate[2]

def convertToDateTimeObj(alertDate):
    return datetime.datetime.strptime(alertDate, '%Y-%m-%d %H:%M:%S')

def splitTimeObj(dateTimeObj):
    return [int(num) for num in str(dateTimeObj.time()).split(':')[0:2]]

def splitDateObj(dateTimeObj):
    return [int(num) for num in str(dateTimeObj.date()).split('-')]

def saveRecentAlerts(alerts):
    alerts_result = filterAlertsByDateTime(alerts)
    with open('alertsHistory.json','w' , encoding='utf8') as file:
        json.dump(alerts_result,file, ensure_ascii=False)

def readRecentAlerts():
    data = []
    with open('alertsHistory.json','r' , encoding='utf8') as file:
        data = json.load(file)
    return data

def printAlerts(alerts):
    if alerts:
        print(datetime.datetime.now().time())
        for alert in alerts:
            print(alert['data'])
    
def getAlerts():
    json_data = [] 
    while True:            
        r = requests.get("https://www.oref.org.il/WarningMessages/History/AlertsHistory.json")
        if not r.text:
            break
        json_data = json.loads(r.text)
        result = filterAlertsByDateTime(json_data)
        print("Alerts:")
        printAlerts(result)
        time.sleep(3)
getAlerts()