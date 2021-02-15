import requests
from datetime import date

def matches():
    # today = date.today()
    # l = str(today).split('-')
    # time = l[0]+l[1]+l[2]
    # url = "https://prod-public-api.livescore.com/v1/api/react/date/soccer/{}/4.00".format(time)

    # data = requests.get(url).json()
    # items = data['Stages']
    # data = items[0]['Events']
    url = "https://prod-public-api.livescore.com/v1/api/react/stage/soccer/england/premier-league/4.00"
    data = requests.get(url).json()
    items = data['Stages'][0]['Events']
    start = 233
    finish = 260
    return items[start:finish]

def odds():
    url = "https://1-xbahis09095.com/LineFeed/Get1x2_VZip?sports=1&champs=88637&count=50&lng=en&tf=2200000&tz=4&mode=4&country=231&partner=7&getEmpty=true&countryOnly=true"
    data = requests.get(url).json()
    items = data['Value']
    return items
    # for i in items:
	#     print(i['O1']+' - '+i['O2']+' W1:'+str(i['E'][0]['C'])+' Draw:'+str(i['E'][1]['C'])+' W2:'+str(i['E'][2]['C']))

def standings():
    url = "https://prod-public-api.livescore.com/v1/api/react/stage/soccer/england/premier-league/4.00"

    data = requests.get(url).json()
    items = data['Stages'][0]['LeagueTable']['L'][0]['Tables'][0]['team']
    return items