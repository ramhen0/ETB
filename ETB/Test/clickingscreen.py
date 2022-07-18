import pyautogui as pg
import time
import pywhatkit as kt



#print(pg.size())
# 2665,44 are the coordinates to close the google chrome
'''
pg.moveTo(473,27,duration=1)
pg.moveRel(473,0,duration=1)
pg.moveRel(473,0,duration=1)
pg.moveRel(473,0,duration=1)
'''
time.sleep(3)

kt.search("https://www.nhl.com/stats/teams?reportType=season&seasonFrom=20212022&seasonTo=20212022&gameType=2&filter=gamesPlayed,gte,1&sort=goalsForPerGame&page=0&pageSize=50")
time.sleep(3)
pg.click(775,534,duration=1)
time.sleep(5)
pg.click(2599,1310,duration=1)
time.sleep(5)
pg.click(624,1135,duration=1)
time.sleep(3)
pg.click(321,1187,duration=1)
time.sleep(2)
# clicks the home
pg.click(191,1352,duration=1)
# clicks get stats
time.sleep(3)
pg.click(223,1560,duration=1)
time.sleep(3)
# clicks so that it can scroll
pg.click(2715,1061,duration=1)
time.sleep(1)
# downloads the home file
pg.click(2618,378,duration=1)
time.sleep(1)

pg.click(2721,371,duration=1)
time.sleep(1)
# click for road options
pg.click(334,1194,duration=1)
time.sleep(1)
# click road
pg.click(153,1424,duration=1)
time.sleep(1)
# click get stats
pg.click(155,1559,duration=1)
time.sleep(1)
# click the scroll bar
pg.click(2716,1118,duration=1)
time.sleep(1)
# click export to download away
pg.click(2601,369,duration=1)
time.sleep(2)
