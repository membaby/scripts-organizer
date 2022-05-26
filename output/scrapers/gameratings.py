import scrapy
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

# algemene selenium gegevens
# chrome_options = Options()
# chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
# chrome_options.add_experimental_option("detach", True)
# chrome_path = which("chromedriver")
# driver2 = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)
# driver2.get("https://www.flashscore.com/match/"+key+"/#match-summary/point-by-point/"+volgnumber)

def get_gameratings1(resp2):
    resp = resp2

    Rating1_1 = 0
    Rating1_2 = 0
    Momentum1 = 0
    GameNum = 0
    Server = 0

    ScheduledTime = resp2.xpath(f"//div[@id='detail']/div[4]/div[1]/div/text()").get()

    point2point = resp.xpath("//div[@id='detail']/div[6]/div/a[2]/text()").get()

    if point2point is not None:
    
        i = 1
        try:   

            rijen = resp.xpath("//div[@id='detail']/div[8]/div/@class").get()

            if rijen is None:
                y = 9
            else:
                y = 8

            for row in resp.xpath(f"//div[@id='detail']/div[{y}]/div"):

                tmp  = resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/@class").get()

                # print("Row: {}, ClassLen: {}, Class: {}".format(i, len(tmp), tmp))

                try:
                    q = len(tmp)
                except:
                    pass                  
                else:
                    if q > 30:
                        classheader = resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/text()").get()
                    # elif q > 20 and q < 30:
                    elif q > 14 and q < 16:

                        if classheader[:8] != "Tiebreak":

                            game1 = resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/div[3]/div[1]/text()").get()
                            game2 = resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/div[3]/div[2]/text()").get()

                            GameNum = int(game1) + int(game2)
                            # print("Row: {}, Score: {} - {}, GameNum: {}".format(i, game1, game2, GameNum))

                            if resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/div[2]/div/svg/@class").get() is None:
                                Server = 2
                            else:
                                Server = 1

                            # print("Kop: {}, Score: {} - {}, server: {}".format(classheader, game1, game2, Server))

                    # elif q > 15 and q < 20:
                    elif q > 23 and q < 28:
                        t = 1
                        gamescore = ''
                        for row in resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/span"):
                            gamescore = gamescore + resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/span[{t}]/text()").get()
                            t = t + 1

                        # print(gamescore)
                        deuce = gamescore.count('40:40')
                        bp = gamescore.count('BP')

                        if Server == 1:
                            Server = 1
                            if bp > 0:
                                Rating1_2 = Rating1_2 + 2
                                if Momentum1 >= 0:
                                    Momentum1 = -2
                                else:
                                    Momentum1 = Momentum1 - 2
                            elif deuce > 0:
                                Rating1_2 = Rating1_2 + 1
                                if Momentum1 >= 0:
                                    Momentum1 = -1
                                else:
                                    Momentum1 = Momentum1 - 1
                        else:
                            Server = 2
                            if bp > 0:
                                Rating1_1 = Rating1_1 + 2
                                if Momentum1 <= 0:
                                    Momentum1 = 2
                                else:
                                    Momentum1 = Momentum1 + 2
                            elif deuce > 0:
                                Rating1_1 = Rating1_1 + 1
                                if Momentum1 <= 0:
                                    Momentum1 = 1
                                else:
                                    Momentum1 = Momentum1 + 1
                        # print("Row: {}, Score: {} - {}, Rating: {} - {}, Momentum: {}, GameNum: {}".format(i, game1, game2, Rating1_1, Rating1_2, Momentum1, GameNum))
                    
                    else:
                        if q <5:
                            break
                i = i + 1
        except:
            print(resp)
            pass
        Point2point = 1
    else:
        Rating1_1 = 0
        Rating1_2 = 0
        Momentum1 = 0
        Server = 0
        ScheduledTime = 0
        GameNum = 0
        Point2point = 0

    # print("Row: {}, Score: {} - {}, Rating: {} - {}, Momentum: {}, GameNum: {}, Server: {} | {}".format(i, game1, game2, Rating1_1, Rating1_2, Momentum1, GameNum, Server, ScheduledTime))
    return Rating1_1, Rating1_2, Momentum1, Server, ScheduledTime, GameNum, Point2point

def get_gameratings2(resp2):
    resp = resp2

    Rating2_1 = 0
    Rating2_2 = 0
    Momentum2 = 0
    GameNum = 0
    Server = 0
 
    i = 1
    try:   

        rijen = resp.xpath("//div[@id='detail']/div[8]/div/@class").get()

        if rijen is None:
            y = 9
        else:
            y = 8

        for row in resp.xpath(f"//div[@id='detail']/div[{y}]/div"):

            tmp  = resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/@class").get()

            # print("Row: {}, ClassLen: {}, Class: {}".format(i, len(tmp), tmp))

            try:
                q = len(tmp)
            except:
                pass                  
            else:
                if q > 30:
                    classheader = resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/text()").get()
                elif q > 14 and q < 16:

                    if classheader[:8] != "Tiebreak":

                        game1 = resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/div[3]/div[1]/text()").get()
                        game2 = resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/div[3]/div[2]/text()").get()

                        GameNum = int(game1) + int(game2)
                        # print("Row: {}, Score: {} - {}, GameNum: {}".format(i, game1, game2, GameNum))

                        if resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/div[2]/div/svg/@class").get() is None:
                            Server = 2
                        else:
                            Server = 1

                        # print("Kop: {}, Score: {} - {}, server: {}".format(classheader, game1, game2, Server))

                elif q > 23 and q < 28:
                    t = 1
                    gamescore = ''
                    for row in resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/span"):
                        gamescore = gamescore + resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/span[{t}]/text()").get()
                        t = t + 1

                    # print(gamescore)
                    deuce = gamescore.count('40:40')
                    bp = gamescore.count('BP')

                    if Server == 1:
                        Server = 1
                        if bp > 0:
                            Rating2_2 = Rating2_2 + 2
                            if Momentum2 >= 0:
                                Momentum2 = -2
                            else:
                                Momentum2 = Momentum2 - 2
                        elif deuce > 0:
                            Rating2_2 = Rating2_2 + 1
                            if Momentum2 >= 0:
                                Momentum2 = -1
                            else:
                                Momentum2 = Momentum2 - 1
                    else:
                        Server = 2
                        if bp > 0:
                            Rating2_1 = Rating2_1 + 2
                            if Momentum2 <= 0:
                                Momentum2 = 2
                            else:
                                Momentum2 = Momentum2 + 2
                        elif deuce > 0:
                            Rating2_1 = Rating2_1 + 1
                            if Momentum2 <= 0:
                                Momentum2 = 1
                            else:
                                Momentum2 = Momentum2 + 1
                    # print("Rating: {} - {}, Momentum: {}".format(rating1, rating2, momentum))
                   
                else:
                    if q <5:
                        break
            i = i + 1
    except:
        print(resp)
        pass

    return Rating2_1,Rating2_2,Momentum2,Server,GameNum

def get_gameratings3(resp2):
    resp = resp2

    Rating3_1 = 0
    Rating3_2 = 0
    Momentum3 = 0
    GameNum = 0
    Server = 0

    i = 1
    try:    

        rijen = resp.xpath("//div[@id='detail']/div[8]/div/@class").get()

        if rijen is None:
            y = 9
        else:
            y = 8

        for row in resp.xpath(f"//div[@id='detail']/div[{y}]/div"):

            tmp  = resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/@class").get()

            # print("Row: {}, ClassLen: {}, Class: {}".format(i, len(tmp), tmp))

            try:
                q = len(tmp)
            except:
                pass                  
            else:
                if q > 30:
                    classheader = resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/text()").get()
                elif q > 14 and q < 16:

                    if classheader[:8] != "Tiebreak":

                        game1 = resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/div[3]/div[1]/text()").get()
                        game2 = resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/div[3]/div[2]/text()").get()

                        GameNum = int(game1) + int(game2)
                        # print("Row: {}, Score: {} - {}, GameNum: {}".format(i, game1, game2, GameNum))

                        if resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/div[2]/div/svg/@class").get() is None:
                            Server = 2
                        else:
                            Server = 1

                        # print("Kop: {}, Score: {} - {}, server: {}".format(classheader, game1, game2, Server))

                elif q > 23 and q < 28:
                    t = 1
                    gamescore = ''
                    for row in resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/span"):
                        gamescore = gamescore + resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/span[{t}]/text()").get()
                        t = t + 1

                    # print(gamescore)
                    deuce = gamescore.count('40:40')
                    bp = gamescore.count('BP')

                    if Server == 1:
                        Server = 1
                        if bp > 0:
                            Rating3_2 = Rating3_2 + 2
                            if Momentum3 >= 0:
                                Momentum3 = -2
                            else:
                                Momentum3 = Momentum3 - 2
                        elif deuce > 0:
                            Rating3_2 = Rating3_2 + 1
                            if Momentum3 >= 0:
                                Momentum3 = -1
                            else:
                                Momentum3 = Momentum3 - 1
                    else:
                        Server = 2
                        if bp > 0:
                            Rating3_1 = Rating3_1 + 2
                            if Momentum3 <= 0:
                                Momentum3 = 2
                            else:
                                Momentum3 = Momentum3 + 2
                        elif deuce > 0:
                            Rating3_1 = Rating3_1 + 1
                            if Momentum3 <= 0:
                                Momentum3 = 1
                            else:
                                Momentum3 = Momentum3 + 1
                    # print("Rating: {} - {}, Momentum: {}".format(rating1, rating2, momentum))
                   
                else:
                    if q <5:
                        break
            i = i + 1
    except:
        print(resp)
        pass

    return Rating3_1,Rating3_2,Momentum3,Server,GameNum

def get_gameratings4(resp2):
    resp = resp2

    Rating4_1 = 0
    Rating4_2 = 0
    Momentum4 = 0
    GameNum = 0
    Server = 0
 
    i = 1
    try:   

        rijen = resp.xpath("//div[@id='detail']/div[8]/div/@class").get()

        if rijen is None:
            y = 9
        else:
            y = 8

        for row in resp.xpath(f"//div[@id='detail']/div[{y}]/div"):

            tmp  = resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/@class").get()

            # print("Row: {}, ClassLen: {}, Class: {}".format(i, len(tmp), tmp))

            try:
                q = len(tmp)
            except:
                pass                  
            else:
                if q > 30:
                    classheader = resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/text()").get()
                elif q > 14 and q < 16:

                    if classheader[:8] != "Tiebreak":

                        game1 = resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/div[3]/div[1]/text()").get()
                        game2 = resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/div[3]/div[2]/text()").get()

                        GameNum = int(game1) + int(game2)
                        # print("Row: {}, Score: {} - {}, GameNum: {}".format(i, game1, game2, GameNum))

                        if resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/div[2]/div/svg/@class").get() is None:
                            Server = 2
                        else:
                            Server = 1

                        # print("Kop: {}, Score: {} - {}, server: {}".format(classheader, game1, game2, Server))

                elif q > 23 and q < 28:
                    t = 1
                    gamescore = ''
                    for row in resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/span"):
                        gamescore = gamescore + resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/span[{t}]/text()").get()
                        t = t + 1

                    # print(gamescore)
                    deuce = gamescore.count('40:40')
                    bp = gamescore.count('BP')

                    if Server == 1:
                        Server = 1
                        if bp > 0:
                            Rating4_2 = Rating4_2 + 2
                            if Momentum4 >= 0:
                                Momentum4 = -2
                            else:
                                Momentum4 = Momentum4 - 2
                        elif deuce > 0:
                            Rating4_2 = Rating4_2 + 1
                            if Momentum4 >= 0:
                                Momentum4 = -1
                            else:
                                Momentum4 = Momentum4 - 1
                    else:
                        Server = 2
                        if bp > 0:
                            Rating4_1 = Rating4_1 + 2
                            if Momentum4 <= 0:
                                Momentum4 = 2
                            else:
                                Momentum4 = Momentum4 + 2
                        elif deuce > 0:
                            Rating4_1 = Rating4_1 + 1
                            if Momentum4 <= 0:
                                Momentum4 = 1
                            else:
                                Momentum4 = Momentum4 + 1
                    # print("Rating: {} - {}, Momentum: {}".format(rating1, rating2, momentum))
                   
                else:
                    if q <5:
                        break
            i = i + 1
    except:
        print(resp)
        pass

    return Rating4_1,Rating4_2,Momentum4,Server,GameNum

def get_gameratings5(resp2):
    resp = resp2

    Rating5_1 = 0
    Rating5_2 = 0
    Momentum5 = 0
    GameNum = 0
    Server = 0
 
    i = 1
    try:   

        rijen = resp.xpath("//div[@id='detail']/div[8]/div/@class").get()

        if rijen is None:
            y = 9
        else:
            y = 8

        for row in resp.xpath(f"//div[@id='detail']/div[{y}]/div"):

            tmp  = resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/@class").get()

            # print("Row: {}, ClassLen: {}, Class: {}".format(i, len(tmp), tmp))

            try:
                q = len(tmp)
            except:
                pass                  
            else:
                if q > 30:
                    classheader = resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/text()").get()
                elif q > 14 and q < 16:

                    if classheader[:8] != "Tiebreak":

                        game1 = resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/div[3]/div[1]/text()").get()
                        game2 = resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/div[3]/div[2]/text()").get()

                        GameNum = int(game1) + int(game2)
                        # print("Row: {}, Score: {} - {}, GameNum: {}".format(i, game1, game2, GameNum))

                        if resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/div[2]/div/svg/@class").get() is None:
                            Server = 2
                        else:
                            Server = 1

                        # print("Kop: {}, Score: {} - {}, server: {}".format(classheader, game1, game2, Server))

                elif q > 23 and q < 28:
                    t = 1
                    gamescore = ''
                    for row in resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/span"):
                        gamescore = gamescore + resp.xpath(f"(//div[@id='detail']/div[{y}]/div[{i}])/span[{t}]/text()").get()
                        t = t + 1

                    # print(gamescore)
                    deuce = gamescore.count('40:40')
                    bp = gamescore.count('BP')

                    if Server == 1:
                        Server = 1
                        if bp > 0:
                            Rating5_2 = Rating5_2 + 2
                            if Momentum5 >= 0:
                                Momentum5 = -2
                            else:
                                Momentum5 = Momentum5 - 2
                        elif deuce > 0:
                            Rating5_2 = Rating5_2 + 1
                            if Momentum5 >= 0:
                                Momentum5 = -1
                            else:
                                Momentum5 = Momentum5 - 1
                    else:
                        Server = 2
                        if bp > 0:
                            Rating5_1 = Rating5_1 + 2
                            if Momentum5 <= 0:
                                Momentum5 = 2
                            else:
                                Momentum5 = Momentum5 + 2
                        elif deuce > 0:
                            Rating5_1 = Rating5_1 + 1
                            if Momentum5 <= 0:
                                Momentum5 = 1
                            else:
                                Momentum5 = Momentum5 + 1
                    # print("Rating: {} - {}, Momentum: {}".format(rating1, rating2, momentum))
                   
                else:
                    if q <5:
                        break
            i = i + 1
    except:
        print(resp)
        pass

    return Rating5_1,Rating5_2,Momentum5,Server,GameNum