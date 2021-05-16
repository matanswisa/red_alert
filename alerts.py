import requests
import json
import datetime
import time

ids_list = []

def orderText(text):
    return " ".join([txt[::-1] for txt in text.split(" ")][::-1])

def printAlerts(alerts):
    if alerts:
        current_alert_id = alerts['id']
        if current_alert_id in ids_list:
            return None
        places = alerts['data']
        print('All recent alerts at time {0}:'.format(datetime.datetime.now()))
        for place in places:
            print(orderText(place))
        ids_list.append(alerts['id'])
                  
def getAlerts():
    while True:            
        r = requests.get("https://www.oref.org.il/WarningMessages/alert/alerts.json",
            headers={'X-Requested-With': 'XMLHttpRequest','Referer': 'https://www.oref.org.il/12402-he/Pakar.aspx'})
        if r.text:
            result = r.json()
            printAlerts(result)
        time.sleep(0.5)

getAlerts()
