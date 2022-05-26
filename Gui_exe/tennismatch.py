import scrapy
import tweepy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from shutil import which
from win32com.client import Dispatch
import time 
from datetime import datetime
import mysql.connector
from gameratings import get_gameratings1,get_gameratings2,get_gameratings3,get_gameratings4,get_gameratings5
import difflib
import sys, os
import csv
import numpy as np
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


import sys
input_file = sys.argv[1]
output_file = sys.argv[2]
print(input_file)
print(output_file)

match_array = []

# algemene selenium gegevens
chrome_options = Options()
chrome_options.headless = True
chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# haal live wedstrijden op
driver.get("https://www.tennis24.com/")
time.sleep(1)

server = 0
herladen = 0
qs = 1
refresh = 0 
haalodds = 200

driver2 = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

while True:
    
    if herladen > 100:
        try:
            #goto tab tomorrow
            path = "//div[@id='live-table']/div[1]/div[2]/div/div[3]/div"
            element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, path)))
            element.click()
            time.sleep(3)
            datumtmp = resp.xpath("//div[@id='live-table']/div[1]/div[2]/div/div[2]/text()").get()
            print(datumtmp)
            haalodds = 200
            print("GOOD: Matches Tomorrow")          
        except Exception as e:
            print("ERROR: Matches Tomorrow")
            print(e)   

    try:
        # def parse(self, response):
        # time.sleep(1)
        html = driver.page_source
        resp = Selector(text=html)

        i = 1

        for row in resp.xpath("//div[@class='sportName tennis']/div"):        

            tmp  = resp.xpath(f"(//div[@class='sportName tennis'])/div[{i}]/@class").get()

            if "header" in tmp:
                sort = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div/div/span/text()").get()
                level = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div/div/span[2]/text()").get()

                temploc = level[:9]
                tempcheck = "Davis Cup" 
                tempcheck2 = "Billie Je"

                if sort == "CHALLENGER MEN - SINGLES" or (sort == "ATP - SINGLES" and temploc != tempcheck)  or (sort == "WTA - SINGLES" and temploc != tempcheck2) or sort == "CHALLENGER WOMEN - SINGLES":

                    tourn = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div/div/span[1]/text()").get()
                    postourn = level.find('60')

                    # sort
                    y = sort.split(' ')
                    cat = y[0]

                    # gender
                    gendertmp = sort.find('Women')

                    if gendertmp > 0 or sort == "WTA - SINGLES":
                        gender = "Women"
                    else:
                        gender = "Men"

                    # location
                    locationtmp = level.find('(')
                    if locationtmp > 0:
                        location = level[:locationtmp-1]
                    else:
                        location = ""

                    # stage
                    stagetmp = level.find('Qualification')
                    if stagetmp > 0:
                        stage = "Qualification"
                    else:
                        stage = "Main"

                    # venue
                    venuetmp = level.find('indoor')
                    if venuetmp > 0:
                        venue = "Indoor"
                    else:
                        venue = "Outdoor"

                    # ground
                    groundtmp = level.find(',')
                    if groundtmp > 0:
                        ground = level[groundtmp+2:]
                        ground = ground[:1].upper() + ground[1:]
                        groundtmp = ground.find('(')
                        if groundtmp > 0:
                            ground = ground[:groundtmp - 1]

                    else:
                        ground = ""

            else:
                temploc = level[:9]
                tempcheck = "Davis Cup" 
                tempcheck2 = "Billie Je"

                if sort == "CHALLENGER MEN - SINGLES" or (sort == "ATP - SINGLES" and temploc != tempcheck)  or (sort == "WTA - SINGLES" and temploc != tempcheck2) or sort == "CHALLENGER WOMEN - SINGLES":
                    key = resp.xpath(f"(//div[@class='sportName tennis'])/div[{i}]/@id").get()
                    key = key[-8:]

                    status = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[2]/div/text()").get()
                    if status is None:
                        status = "Scheduled"
                    elif status[0:3] == "Fin":
                        status = "Finished"
                    elif status[0:3] == "Can":
                        status = "Cancelled"
                    elif status[0:3] == "Wal":
                        status = "WalkOver"
                    elif status[0:3] == "Int":
                        status = "Interrupted"
                    elif status[0:3] == "Awa":
                        status = "Awarded"
                    else:
                        status = "Live"
                 
                    # get algemene gegevens match
                    player1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[3]/text()").get()
                    pos = player1.find('(')
                    player1 = player1[:pos]
                    
                    player2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[4]/text()").get()
                    pos = player2.find('(')
                    player2 = player2[:pos]

                    rows = driver.find_elements_by_xpath(f"(//div[@class='sportName tennis']/div[{i}])/div")

                    server = resp.xpath(f"(//div[@class='sportName tennis'])/div[{i}]/svg/@class").get()

                    if server is not None:                    
                        pos = server.find('serveHome')

                        if pos > 1:
                            server = 1
                        else:
                            server = 2
                    else:
                        server = 0

                    sets1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[5]/text()").get()
                    sets2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[6]/text()").get()

                    games1_1 = 0
                    games2_1 = 0
                    games1_2 = 0
                    games2_2 = 0
                    games1_3 = 0
                    games2_3 = 0
                    games1_4 = 0
                    games2_4 = 0
                    games1_5 = 0
                    games2_5 = 0
                    gamescore1 = 0
                    gamescore2 = 0

                    # print("Players {} - {} | Status: {}, Lengte: {}".format(player1,player2, status, len(rows)))

                    if len(rows) == 20: # Live match 5th set
                        games1_1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[7]/text()").get() 
                        games2_1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[8]/text()").get() 
                        games1_2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[9]/text()").get() 
                        games2_2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[10]/text()").get() 
                        games1_3 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[11]/text()").get() 
                        games2_3 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[12]/text()").get() 
                        games1_4 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[13]/text()").get() 
                        games2_4 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[14]/text()").get() 
                        games1_5 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[15]/text()").get() 
                        games2_5 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[16]/text()").get() 
                        gamescore1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[17]/text()").get() 
                        gamescore2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[18]/text()").get()
                    elif len(rows) == 18:
                        if status == "Live": # 4th set
                            games1_1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[7]/text()").get() 
                            games2_1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[8]/text()").get() 
                            games1_2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[9]/text()").get() 
                            games2_2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[10]/text()").get() 
                            games1_3 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[11]/text()").get() 
                            games2_3 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[12]/text()").get() 
                            games1_4 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[13]/text()").get() 
                            games2_4 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[14]/text()").get() 
                            gamescore1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[15]/text()").get() 
                            gamescore2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[16]/text()").get()
                        else: # Finished in 5 sets
                            games1_1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[7]/text()").get() 
                            games2_1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[8]/text()").get() 
                            games1_2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[9]/text()").get() 
                            games2_2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[10]/text()").get() 
                            games1_3 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[11]/text()").get() 
                            games2_3 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[12]/text()").get() 
                            games1_4 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[13]/text()").get() 
                            games2_4 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[14]/text()").get() 
                            games1_5 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[15]/text()").get() 
                            games2_5 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[16]/text()").get()
                    elif len(rows) == 16:
                        if status == "Live": # 3th set
                            games1_1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[7]/text()").get() 
                            games2_1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[8]/text()").get() 
                            games1_2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[9]/text()").get() 
                            games2_2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[10]/text()").get() 
                            games1_3 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[11]/text()").get() 
                            games2_3 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[12]/text()").get() 
                            gamescore1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[13]/text()").get() 
                            gamescore2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[14]/text()").get()
                        else: # Finished in 4 sets
                            games1_1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[7]/text()").get() 
                            games2_1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[8]/text()").get() 
                            games1_2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[9]/text()").get() 
                            games2_2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[10]/text()").get() 
                            games1_3 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[11]/text()").get() 
                            games2_3 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[12]/text()").get() 
                            games1_4 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[13]/text()").get() 
                            games2_4 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[14]/text()").get()
                    elif len(rows) == 14:
                        if status == "Live": #2nd set 
                            games1_1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[7]/text()").get() 
                            games2_1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[8]/text()").get() 
                            games1_2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[9]/text()").get() 
                            games2_2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[10]/text()").get() 
                            gamescore1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[11]/text()").get() 
                            gamescore2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[12]/text()").get()
                        else: # Finished in 3 sets
                            games1_1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[7]/text()").get() 
                            games2_1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[8]/text()").get() 
                            games1_2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[9]/text()").get() 
                            games2_2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[10]/text()").get() 
                            games1_3 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[11]/text()").get() 
                            games2_3 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[12]/text()").get()
                    elif len(rows) == 12:
                        if status == "Live": #1st set                       
                            games1_1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[7]/text()").get() 
                            games2_1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[8]/text()").get() 
                            gamescore1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[9]/text()").get()
                            gamescore2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[10]/text()").get()
                        else: # Finished in 2 sets
                            games1_1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[7]/text()").get() 
                            games2_1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[8]/text()").get() 
                            games1_2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[9]/text()").get()
                            games2_2 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[10]/text()").get()
                    elif len(rows) == 10: # Finished in 1 set
                        games1_1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[7]/text()").get() 
                        games2_1 = resp.xpath(f"(//div[@class='sportName tennis']/div[{i}])/div[8]/text()").get() 

                    # append match to list

                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")

                    ronde = 'none'
                    setgames = 0
                    totalgames = 0

                    if sets1 is None or sets1 == "-":
                        sets1 = 0

                    if sets2 is None or sets2 == "-":
                        sets2 = 0

                    if games1_1 is None:
                        games1_1 = 0

                    if games2_1 is None:
                        games2_1 = 0

                    try:
                        totalgames = int(games1_1)+int(games2_1)+int(games1_2)+int(games2_2)+int(games1_3)+int(games2_3)+int(games1_4)+int(games2_4)+int(games1_5)+int(games2_5)
                    except Exception as e:
                        print(e)

                    Rating1_1 = 0
                    Rating1_2 = 0
                    Rating2_1 = 0
                    Rating2_2 = 0
                    Rating3_1 = 0
                    Rating3_2 = 0
                    Rating4_1 = 0
                    Rating4_2 = 0
                    Rating5_1 = 0
                    Rating5_2 = 0
                    Momentum1 = 0
                    Momentum2 = 0
                    Momentum3 = 0
                    Momentum4 = 0
                    Momentum5 = 0

                    qw = 0

                    for row in match_array:
                        if key == row[0]:
                            qw = 1
                            break             

                    if qw == 0:
                        driver2.get("https://www.tennis24.com/match/"+key+"/#match-summary")
                        time.sleep(3)
                        html2 = driver2.page_source
                        resp2 = Selector(text=html2)

                        # rondetmp = resp2.xpath(f"//div[@id='detail']/div[3]/div[1]/span[2]/a/text()").get()
                        rondetmp = resp2.xpath(f"//div[@id='detail']/div[3]/div/span[2]/a/text()").get()
                        ronde = rondetmp[rondetmp.find("-",rondetmp.find(","))+2:]

                        if ronde.find("(") > 0:
                            ronde = ""

                        scheduledtime = resp2.xpath(f"//div[@id='detail']/div[4]/div[1]/div/text()").get()

                        odds1 = 0
                        odds2 = 0

                        print("NEW MATCH | Players: {} - {} | Odds: {} - {}".format(player1,player2,odds1,odds2))

                        newvalues = [key,scheduledtime,status,player1,player2,gender,cat,location,stage,ronde,ground,venue,odds1,odds2,sets1,sets2,games1_1,games2_1,games1_2,games2_2,games1_3,games2_3,games1_4,
                        games2_4,games1_5,games2_5,gamescore1,gamescore2,Rating1_1,Rating1_2,Rating2_1,Rating2_2,Rating3_1,Rating3_2,Rating4_1,
                        Rating4_2,Rating5_1,Rating5_2,Momentum1,Momentum2,Momentum3,Momentum4,Momentum5,server,totalgames,now]

                        match_array.append(newvalues)

                        with open(output_file, mode='wt', encoding='utf-8') as myfile:
                            writer = csv.writer(myfile)
                            writer.writerows(match_array)

                    # update bestaande match
                    elif qw == 1:
                        for row in match_array:
                            if key == row[0]:
                                # bepaal of total games > laatste gelogde game
                                if totalgames is not row[44] or status != row[2]:

                                    # match canceled
                                    if status == 'Cancelled' or status == 'Walkover':
                                        query = "UPDATE matches SET Status='{}' WHERE MatchKey='{}'".format(status, key)

                                        print(query)

                                    else:

                                        try:
                                            volgnumber = int(sets1) + int(sets2)

                                            if row[2] == "Finished":
                                                volgnumber = volgnumber - 1

                                            if volgnumber == 1 and int(games1_2) + int(games2_2) == 0 and row[2] != "Finished":
                                                volgnumber = 0

                                            if volgnumber == 2 and int(games1_3) + int(games2_3) == 0 and row[2] != "Finished":
                                                volgnumber = 1

                                            if volgnumber == 3 and int(games1_4) + int(games2_4) == 0 and row[2] != "Finished":
                                                volgnumber = 2

                                            if volgnumber == 4 and int(games1_5) + int(games2_5) == 0 and row[2] != "Finished":
                                                volgnumber = 3

                                            volgnumber = str(volgnumber)
                                            # print("Players: {} - {} | Volgnummer: {}".format(player1,player2,volgnumber))
                                        except Exception as e:
                                            print(e)

                                        # haal gameratings set1 op
                                        try:
                                            setgames = int(games1_1) + int(games2_1)
                                        except Exception as e:
                                            print(e)
                                    
                                        if volgnumber == 0:
                                            time.sleep(3)
                                                                        
                                        driver2.get("https://www.tennis24.com/match/"+key+"/#match-summary/point-by-point/0")
                                        time.sleep(3)
                                        html2 = driver2.page_source
                                        resp2 = Selector(text=html2)

                                        Rating1_1, Rating1_2, Momentum1, Server, ScheduledTime, GameNum, Point2point = get_gameratings1(resp2)

                                        if Point2point == 1:
                                                            
                                            if (GameNum < setgames or Server == 0) and int(GameNum) + int(setgames) < 25:
                                                print("ERROR: {} - {} | GameNum {}, SetGames {} | Server: {}, Rating: {} - {}, Status: {}".format(player1, player2, GameNum, setgames, server, Rating1_1, Rating1_2, status))
                                                # haal gameratings op
                                                if volgnumber == 0:
                                                    time.sleep(3)

                                                driver2.get("https://www.tennis24.com/match/"+key+"/#match-summary/point-by-point/0")
                                                time.sleep(3)
                                                html2 = driver2.page_source
                                                resp2 = Selector(text=html2)

                                                Rating1_1, Rating1_2, Momentum1, Server, ScheduledTime, GameNum, Point2point = get_gameratings1(resp2)
                                                                
                                            if (GameNum < setgames or Server == 0) and int(GameNum) + int(setgames) < 25:
                                                print("GameNum: {} | setgames {}, Server {}".format(GameNum,setgames,Server))
                                                print("ERROR: {} - {} | GameNum {}, SetGames {} | Server: {}, Rating: {} - {}, Status: {}".format(player1, player2, GameNum, setgames, server, Rating1_1, Rating1_2, status))
                                                # haal gameratings op
                                                if volgnumber == 0:
                                                    time.sleep(3)

                                                driver2.get("https://www.tennis24.com/match/"+key+"/#match-summary/point-by-point/0")
                                                time.sleep(3)
                                                html2 = driver2.page_source
                                                resp2 = Selector(text=html2)

                                                Rating1_1, Rating1_2, Momentum1, Server, ScheduledTime, GameNum, Point2point = get_gameratings1(resp2)

                                            if int(volgnumber) > 0:
                                                # haal gameratings set2 op
                                                setgames = int(games1_2) + int(games2_2)
                                            
                                                if volgnumber == 1:
                                                    time.sleep(3)
                                                                                
                                                driver2.get("https://www.tennis24.com/match/"+key+"/#match-summary/point-by-point/1")
                                                time.sleep(3)
                                                html2 = driver2.page_source
                                                resp2 = Selector(text=html2)

                                                Rating2_1,Rating2_2,Momentum2,Server,GameNum = get_gameratings2(resp2)
                                                                    
                                                if (GameNum < setgames or Server == 0) and int(GameNum) + int(setgames) < 25:
                                                    print("ERROR: {} - {} | GameNum {}, SetGames {} | Server: {}, Rating: {} - {}, Status: {}".format(player1, player2, GameNum, setgames, server, Rating1_1, Rating1_2, status))
                                                    # haal gameratings op
                                                    if volgnumber == 1:
                                                        time.sleep(3)

                                                    driver2.get("https://www.tennis24.com/match/"+key+"/#match-summary/point-by-point/1")
                                                    time.sleep(3)
                                                    html2 = driver2.page_source
                                                    resp2 = Selector(text=html2)

                                                    Rating2_1,Rating2_2,Momentum2,Server,GameNum = get_gameratings2(resp2)
                                                                        
                                                if (GameNum < setgames or Server == 0) and int(GameNum) + int(setgames) < 25:
                                                    print("ERROR: {} - {} | GameNum {}, SetGames {} | Server: {}, Rating: {} - {}, Status: {}".format(player1, player2, GameNum, setgames, server, Rating1_1, Rating1_2, status))
                                                    # haal gameratings op
                                                    if volgnumber == 1:
                                                        time.sleep(3)

                                                    driver2.get("https://www.tennis24.com/match/"+key+"/#match-summary/point-by-point/1")
                                                    time.sleep(3)
                                                    html2 = driver2.page_source
                                                    resp2 = Selector(text=html2)

                                                    Rating2_1,Rating2_2,Momentum2,Server,GameNum = get_gameratings2(resp2)

                                            if int(volgnumber) > 1:
                                                # haal gameratings set3 op
                                                setgames = int(games1_3) + int(games2_3)
                                            
                                                if volgnumber == 2:
                                                    time.sleep(3)
                                                                                
                                                driver2.get("https://www.tennis24.com/match/"+key+"/#match-summary/point-by-point/2")
                                                time.sleep(3)
                                                html2 = driver2.page_source
                                                resp2 = Selector(text=html2)

                                                Rating3_1,Rating3_2,Momentum3,Server,GameNum = get_gameratings3(resp2)
                                                                    
                                                if (GameNum < setgames or Server == 0) and int(GameNum) + int(setgames) < 25:
                                                    print("ERROR: {} - {} | GameNum {}, SetGames {} | Server: {}, Rating: {} - {}, Status: {}".format(player1, player2, GameNum, setgames, server, Rating1_1, Rating1_2, status))
                                                    # haal gameratings op
                                                    if volgnumber == 2:
                                                        time.sleep(3)

                                                    driver2.get("https://www.tennis24.com/match/"+key+"/#match-summary/point-by-point/2")
                                                    time.sleep(3)
                                                    html2 = driver2.page_source
                                                    resp2 = Selector(text=html2)

                                                    Rating3_1,Rating3_2,Momentum3,Server,GameNum = get_gameratings3(resp2)
                                                                        
                                                if (GameNum < setgames or Server == 0) and int(GameNum) + int(setgames) < 25:
                                                    print("ERROR: {} - {} | GameNum {}, SetGames {} | Server: {}, Rating: {} - {}, Status: {}".format(player1, player2, GameNum, setgames, server, Rating1_1, Rating1_2, status))
                                                    # haal gameratings op
                                                    if volgnumber == 2:
                                                        time.sleep(3)

                                                    driver2.get("https://www.tennis24.com/match/"+key+"/#match-summary/point-by-point/2")
                                                    time.sleep(3)
                                                    html2 = driver2.page_source
                                                    resp2 = Selector(text=html2)

                                                    Rating3_1,Rating3_2,Momentum3,Server,GameNum = get_gameratings3(resp2)

                                            if int(volgnumber) > 2:
                                                # haal gameratings set4 op
                                                setgames = int(games1_4) + int(games2_4)
                                            
                                                if volgnumber == 3:
                                                    time.sleep(3)
                                                                                
                                                driver2.get("https://www.tennis24.com/match/"+key+"/#match-summary/point-by-point/3")
                                                time.sleep(3)
                                                html2 = driver2.page_source
                                                resp2 = Selector(text=html2)

                                                Rating4_1,Rating4_2,Momentum4,Server,GameNum = get_gameratings4(resp2)
                                                                    
                                                if GameNum < setgames or Server == 0 and (GameNum != 12 and setgames != 13):
                                                    print("ERROR: {} - {} | GameNum {}, SetGames {} | Server: {}, Rating: {} - {}, Status: {}".format(player1, player2, GameNum, setgames, server, Rating1_1, Rating1_2, status))
                                                    # haal gameratings op
                                                    if volgnumber == 3:
                                                        time.sleep(3)

                                                    driver2.get("https://www.tennis24.com/match/"+key+"/#match-summary/point-by-point/3")
                                                    time.sleep(3)
                                                    html2 = driver2.page_source
                                                    resp2 = Selector(text=html2)

                                                    Rating4_1,Rating4_2,Momentum4,Server,GameNum = get_gameratings4(resp2)
                                                                        
                                                if GameNum < setgames or Server == 0 and (GameNum != 12 and setgames != 13):
                                                    print("ERROR: {} - {} | GameNum {}, SetGames {} | Server: {}, Rating: {} - {}, Status: {}".format(player1, player2, GameNum, setgames, server, Rating1_1, Rating1_2, status))
                                                    # haal gameratings op
                                                    if volgnumber == 3:
                                                        time.sleep(3)

                                                    driver2.get("https:/www.tennis24.com/match/"+key+"/#match-summary/point-by-point/3")
                                                    time.sleep(3)
                                                    html2 = driver2.page_source
                                                    resp2 = Selector(text=html2)

                                                    Rating4_1,Rating4_2,Momentum4,Server,GameNum = get_gameratings4(resp2)

                                            if int(volgnumber) > 3:
                                                # haal gameratings set4 op
                                                setgames = int(games1_5) + int(games2_5)
                                            
                                                if volgnumber == 4:
                                                    time.sleep(3)
                                                                                
                                                driver2.get("https://www.tennis24.com/match/"+key+"/#match-summary/point-by-point/4")
                                                time.sleep(3)
                                                html2 = driver2.page_source
                                                resp2 = Selector(text=html2)

                                                Rating5_1,Rating5_2,Momentum5,Server,GameNum = get_gameratings5(resp2)
                                                                    
                                                if GameNum < setgames or Server == 0 and (GameNum != 12 and setgames != 13):
                                                    print("ERROR: {} - {} | GameNum {}, SetGames {} | Server: {}, Rating: {} - {}, Status: {}".format(player1, player2, GameNum, setgames, server, Rating1_1, Rating1_2, status))
                                                    # haal gameratings op
                                                    if volgnumber == 4:
                                                        time.sleep(3)

                                                    driver2.get("https://www.tennis24.com/match/"+key+"/#match-summary/point-by-point/4")
                                                    time.sleep(3)
                                                    html2 = driver2.page_source
                                                    resp2 = Selector(text=html2)

                                                    Rating5_1,Rating5_2,Momentum5,Server,GameNum = get_gameratings5(resp2)
                                                                        
                                                if GameNum < setgames or Server == 0 and (GameNum != 12 and setgames != 13):
                                                    print("ERROR: {} - {} | GameNum {}, SetGames {} | Server: {}, Rating: {} - {}, Status: {}".format(player1, player2, GameNum, setgames, server, Rating1_1, Rating1_2, status))
                                                    # haal gameratings op
                                                    if volgnumber == 4:
                                                        time.sleep(3)

                                                    driver2.get("https://www.tennis24.com/match/"+key+"/#match-summary/point-by-point/4")
                                                    time.sleep(3)
                                                    html2 = driver2.page_source
                                                    resp2 = Selector(text=html2)

                                                    Rating5_1,Rating5_2,Momentum5,Server,GameNum = get_gameratings5(resp2)

                                        # werk array gegevens op
                                        row[1] = ScheduledTime
                                        row[2] = status                                
                                        row[14] = sets1
                                        row[15] = sets2
                                        row[16] = games1_1
                                        row[17] = games2_1
                                        row[18] = games1_2
                                        row[19] = games2_2
                                        row[20] = games1_3
                                        row[21] = games2_3
                                        row[22] = games1_4
                                        row[23] = games2_4
                                        row[24] = games1_5
                                        row[25] = games2_5
                                        row[26] = gamescore1
                                        row[27] = gamescore2
                                        row[28] = Rating1_1   
                                        row[29] = Rating1_2
                                        row[30] = Rating2_1
                                        row[31] = Rating2_2
                                        row[32] = Rating3_1
                                        row[33] = Rating3_2
                                        row[34] = Rating4_1
                                        row[35] = Rating4_2
                                        row[36] = Rating5_1
                                        row[37] = Rating5_2 
                                        row[38] = Momentum1
                                        row[39] = Momentum2
                                        row[40] = Momentum3
                                        row[41] = Momentum4
                                        row[42] = Momentum5
                                        row[43] = Server
                                        row[44] = totalgames 
                                        row[45] = now

                                        if status == 'Finished' and row[16] + row[17] == 0:

                                            print("Error finished match zonder games")

                                        else:
                                                                                                    
                                            print("Key: {}, Players: {} - {}, Games: {} - {} | {} - {} | {} - {}, Server: {}, Ratings: ({}-{}) {} | ({}-{}) {} | ({}-{}) {} , Status: {}, Rows: {}".format(row[0],row[3],row[4],row[16],row[17],row[18],row[19],row[20],row[21],row[43],row[28],row[29],row[38],row[30],row[31],row[39],row[32],row[33],row[40],row[2], len(rows)))

                                            # **********UPDATE ROW DATABASE********************
                                            query = "UPDATE matches SET TimeStamp='{}', Status='{}', Sets1='{}', Sets2='{}', Set11='{}', Set12='{}', Set21='{}', Set22='{}', Set31='{}', Set32='{}', Set41='{}', Set42='{}', Set51='{}', Set52='{}', GameScore1='{}', GameScore2='{}', Rating1_1='{}', Rating1_2='{}', Rating2_1='{}', Rating2_2='{}', Rating3_1='{}', Rating3_2='{}', Rating4_1='{}', Rating4_2='{}', Rating5_1='{}', Rating5_2='{}', Momentum1='{}', Momentum2='{}', Momentum3='{}', Momentum4='{}', Momentum5='{}', Server='{}', TotalGames='{}', LastUpdate='{}' WHERE MatchKey='{}'".format(ScheduledTime,
                                            status,sets1,sets2,games1_1,games2_1,games1_2,games2_2,games1_3,games2_3,games1_4,
                                            games2_4,games1_5,games2_5,gamescore1,gamescore2,Rating1_1,Rating1_2,Rating2_1,Rating2_2,Rating3_1,Rating3_2,Rating4_1,
                                            Rating4_2,Rating5_1,Rating5_2,Momentum1,Momentum2,Momentum3,Momentum4,Momentum5,server,totalgames,now,key)

                                            # print(query)

                                            with open(output_file, mode='wt', encoding='utf-8') as myfile:
                                                writer = csv.writer(myfile)
                                                writer.writerows(match_array)

            i = i + 1


        # for row in match_array:
        #     print("Key: {}, DateTime: {}, Players: {} - {}, Odds: {} - {}, Status: {}".format(row[0],row[1],row[3],row[4],row[12],row[13],row[2]))

        if refresh > 110:
            try:
                time.sleep(1)
                driver.get("https://www.tennis24.com/")
                time.sleep(3)
                refresh = 0
                haalodds = 110
                print("Refresh Browser") 
                datumtmp = resp.xpath("//div[@id='live-table']/div[1]/div[2]/div/div[2]/text()").get()
                print(datumtmp)
            except Exception as e:
                print(e)

        if haalodds > 100:
            try:
                print("Update Odds")

                key = ""
                player1 = ""
                player2 = ""
                status = ""

                l = 1

                now = datetime.now()
                jaar = now.year
                datumtmp = resp.xpath("//div[@id='live-table']/div[1]/div[2]/div/div[2]/text()").get()
                print(datumtmp)
                posslash = datumtmp.find("/")
                dag = datumtmp[:posslash]
                posspace = datumtmp.find(" ")
                maand = datumtmp[posslash + 1:posspace]
                datumstring = str(dag) + "." + str(maand) + "." + str(jaar)

                for row in resp.xpath("//div[@class='sportName tennis']/div"):        

                    tmp  = resp.xpath(f"(//div[@class='sportName tennis'])/div[{l}]/@class").get()

                    if "header" in tmp:
                        sort = resp.xpath(f"(//div[@class='sportName tennis']/div[{l}])/div/div/span/text()").get()
                        level = resp.xpath(f"(//div[@class='sportName tennis']/div[{l}])/div/div/span[2]/text()").get()
                        postourn = level.find('60')

                    else:
                        try:
                            temploc = level[:9]
                            tempcheck = "Davis Cup" 
                            tempcheck2 = "Billie Je"

                            if sort == "CHALLENGER MEN - SINGLES" or (sort == "ATP - SINGLES" and temploc != tempcheck)  or (sort == "WTA - SINGLES" and temploc != tempcheck2) or sort == "CHALLENGER WOMEN - SINGLES":
                                #  or sort == "EXHIBITION - MEN" or sort == "EXHIBITION - WOMEN"
                                key = resp.xpath(f"(//div[@class='sportName tennis'])/div[{l}]/@id").get()
                                key = key[-8:]                               

                                status = resp.xpath(f"(//div[@class='sportName tennis']/div[{l}])/div[2]/div/text()").get()
                                if status is None:
                                    tijd = 'None'
                                    status = "Scheduled"
                                    tijd = datumstring + " " + resp.xpath(f"(//div[@class='sportName tennis']/div[{l}])/div[2]/text()").get()
                                    # print(tijd)
                                elif status[0:3] == "Fin":
                                    status = "Finished"
                                elif status[0:3] == "Can":
                                    status = "Cancelled"
                                elif status[0:3] == "Wal":
                                    status = "WalkOver"
                                else:
                                    status = "Live"

                                player1 = resp.xpath(f"(//div[@class='sportName tennis'])/div[{l}]/div[3]/text()").get()
                                player2 = resp.xpath(f"(//div[@class='sportName tennis'])/div[{l}]/div[4]/text()").get()

                                rows = driver.find_elements_by_xpath(f"(//div[@class='sportName tennis']/div[{l}])/div")

                                oddrow1 = len(rows) - 1
                                
                                odds1 = resp.xpath(f"(//div[@class='sportName tennis'])/div[{l}]/div[{oddrow1}]/span/text()").get()
                                
                                if odds1 is None:
                                    odds1 = 0

                                odds2 = resp.xpath(f"(//div[@class='sportName tennis'])/div[{l}]/div[{oddrow1 + 1}]/span/text()").get()

                                if odds2 is None:
                                    odds2 = 0

                                if status == "Live" or status == "Scheduled":

                                    for row in match_array:
                                        if key == row[0]:
                                            row[12] = odds1
                                            row[13] = odds2

                                            # **********UPDATE ROW DATABASE********************
                                            if status == "Live":
                                                query = "UPDATE matches SET Odds1='{}', Odds2='{}' WHERE MatchKey='{}'".format(odds1, odds2, key)
                                            else:
                                                query = "UPDATE matches SET TimeStamp='{}', Odds1='{}', Odds2='{}' WHERE MatchKey='{}'".format(tijd, odds1, odds2, key)

                                            try:
                                                print("GOOD: Status: {} | Players: {} - {} | Odds: {} - {}".format(status, player1, player2, odds1,odds2))
                                            except Exception as e:
                                                exc_type, exc_obj, exc_tb = sys.exc_info()
                                                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                                                print(exc_type, fname, exc_tb.tb_lineno)
                                                print("ERROR: Status: {} | Players: {} - {} | Odds: {} - {}".format(status, player1, player2, odds1,odds2))
                                                
                        except Exception as e:
                            exc_type, exc_obj, exc_tb = sys.exc_info()
                            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                            print(exc_type, fname, exc_tb.tb_lineno)
                            pass

                    l = l + 1

                haalodds = 0

                if herladen > 100:

                    try:
                        refresh = 0
                        herladen = 0
                        print("Refresh Browser after odd update tomorow")
                        #goto tab today
                        path = "//div[@id='live-table']/div[1]/div[2]/div/div[1]/div"
                        element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, path)))
                        element.click()
                        time.sleep(3)
                        datumtmp = resp.xpath("//div[@id='live-table']/div[1]/div[2]/div/div[2]/text()").get()
                        print(datumtmp)
                    except Exception as e:
                        print(e)

            except Exception as e:
                        print("11")
                        print(e)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

    refresh = refresh + 1
    herladen = herladen + 1
    haalodds = haalodds + 1
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")










