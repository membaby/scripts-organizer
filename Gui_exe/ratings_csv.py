import sys
input_file = sys.argv[1]
output_file = sys.argv[2]

def getdata(bestandsnaam):
    import sys
    import difflib
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
    import os
    from datetime import datetime
    import csv
    import numpy as np
    from webdriver_manager.chrome import ChromeDriverManager


    now1 = datetime.now()  

    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except:
            base_path = os.path.dirname(__file__)
        return os.path.join(base_path, relative_path)

    def nested_count(lst, x):
        return lst.count(x) + sum(
            nested_count(l,x) for l in lst if isinstance(l,list))

    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    items = []

    with open(input_file) as csvfile:    
        csvReader = csv.reader(csvfile)    
        for row in csvReader:        
            items.append(row[0])        
    print(len(items))

    # while l < len(data_array):

    url = "https://www.oddsportal.com/soccer/netherlands/eredivisie/results/"

    # open webpage
    driver.get(url)
    time.sleep(1)
    html = driver.page_source

    # def parse(self, response):
    resp = Selector(text=html)

    r = 1
    q = 1
    teller = 1
    aantalpag = 1
    matchlist_array = []
    teamlist = set()

    # aantal pagina's

    countrie = resp.xpath(f"//div[@id='breadcrumb']/a[3]/text()").get()
    league = resp.xpath(f"//div[@id='breadcrumb']/a[4]/text()").get()

    for rij in resp.xpath("//div[@id='pagination']/a"):
        aantalpag = resp.xpath(f"//div[@id='pagination']/a[{r}]/@x-page").get()
        r = r + 1
    
    i = 1

    for rij in resp.xpath("//div[@id='tournamentTable']/table/tbody/tr"):
        
        if resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/th/span/text()") is not None:
            temp = resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/th/span/@class").get()
            
            if temp is not None and len(temp) > 10:
                datum = resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/th/span/text()").get()
                # print(datum)

        if resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/@xeid").get() is not None:
            tijd = resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/td[1]/text()").get()

            try:
                score = resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/td[3]/text()").get()
                score1 = score[:1]
                score2 = score[-1:]
            except:
                continue

            odd1 = resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/td[4]/a/text()").get()
            odd3 = resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/td[5]/a/text()").get()
            odd2 = resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/td[6]/a/text()").get()

            if resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/td[2]/a/span/text()").get() is not None:
                team1tmp = resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/td[2]/a/span/text()").get()
                team2tmp = resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/td[2]/a/text()").get()
                posteam = team2tmp.find('-')

                if posteam > 2:                        
                    team1 = team2tmp.replace("- ", "")
                    team1 = team1.replace(" -", "")
                    team1 = team1.strip()
                    team2 = team1tmp
                else:
                    team2 = team2tmp.replace(" -", "")
                    team2 = team2.replace("- ", "")
                    team2 = team2.strip()
                    team1 = team1tmp

            else:
                team3 = resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/td[2]/a/text()").get()
                pos = team3.find(' - ')
                lengte = len(team3)
            
                team1 = team3[0:pos]
                team1 = team1.strip() 
                team2 = team3[pos+3:lengte]
                team2 = team2.strip()

            try:
                if len(score) == 3:
                    newvalues = [q,countrie,league,datum,tijd,team1,team2,score1,score2,odd1,odd2,odd3]
                    matchlist_array.append(newvalues)
                    teamlist.add(team1)
                    teamlist.add(team2)
            except:
                continue
            
        i = i + 1
        q = q + 1

    if int(aantalpag) > 1:
        while teller < int(aantalpag):
            teller = teller + 1

            url1 = f"{url}/#/page/{teller}/"

            # open webpage
            driver.get(url1)
            time.sleep(1)
            html = driver.page_source

            # def parse(self, response):
            resp = Selector(text=html)

            i = 1

            for rij in resp.xpath("//div[@id='tournamentTable']/table/tbody/tr"):
                
                if resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/th/span/text()") is not None:
                    temp = resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/th/span/@class").get()
                    
                    if temp is not None and len(temp) > 10:
                        datum = resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/th/span/text()").get()
                        # print(datum)

                if resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/@xeid").get() is not None:
                    tijd = resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/td[1]/text()").get()
                    score = resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/td[3]/text()").get()
                    score1 = score[:1]
                    score2 = score[-1:]
                    odd1 = resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/td[4]/a/text()").get()
                    odd3 = resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/td[5]/a/text()").get()
                    odd2 = resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/td[6]/a/text()").get()

                    if resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/td[2]/a/span/text()").get() is not None:
                        team1tmp = resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/td[2]/a/span/text()").get()
                        team2tmp = resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/td[2]/a/text()").get()
                        posteam = team2tmp.find('-')

                        if posteam > 2:                        
                            team1 = team2tmp.replace("- ", "")
                            team1 = team1.replace(" -", "")
                            team1 = team1.strip()
                            team2 = team1tmp
                        else:
                            team2 = team2tmp.replace(" -", "")
                            team2 = team2.replace("- ", "")
                            team2 = team2.strip()
                            team1 = team1tmp
                    else:
                        team3 = resp.xpath(f"//div[@id='tournamentTable']/table/tbody/tr[{i}]/td[2]/a/text()").get()
                        pos = team3.find(' - ')
                        lengte = len(team3)
                    
                        team1 = team3[0:pos]
                        team1 = team1.strip() 
                        team2 = team3[pos+3:lengte]
                        team2 = team2.strip()

                    try:
                        if len(score) == 3:
                            newvalues = [q,countrie,league,datum,tijd,team1,team2,score1,score2,odd1,odd2,odd3]
                            matchlist_array.append(newvalues)
                            teamlist.add(team1)
                            teamlist.add(team2)
                    except:
                        continue
                    
                i = i + 1
                q = q + 1

    aantal_teams = len(teamlist)
    teamlist_array = []
    matches = []
    newratings = []
    count = 0

    while teamlist:
        teamnaam = teamlist.pop()
        count = nested_count(matchlist_array, teamnaam)
        
        matches = [ match for match in matchlist_array if match[5] == teamnaam or match[6] == teamnaam ]
        matches.sort()

        wins = [ x for x in matches if (x[5] == teamnaam and x[7] > x[8]) or (x[6] == teamnaam and x[8] > x[7])]
        draws = [ x for x in matches if (x[5] == teamnaam and x[7] == x[8]) or (x[6] == teamnaam and x[8] == x[7])]
        lost = [ x for x in matches if (x[5] == teamnaam and x[7] < x[8]) or (x[6] == teamnaam and x[8] < x[7])]
        winst = len(wins)
        gelijk = len(draws)
        lost = len(lost)
        aantal = winst + gelijk + lost
        punten = winst * 3 + gelijk
        avg = round(punten / aantal, 3)
        
        # bereken odds/vorm
        if count > 5:
            lengte = 5
        else:
            lengte = count

        puntenreeks = 0
        m = []

        for rij in matches[:lengte]:
            if rij[5] == teamnaam:
                if rij[7] > rij[8]:
                    puntenreeks = puntenreeks + 3
                elif rij[7] == rij[8]:
                    puntenreeks = puntenreeks + 1

                try:
                    oddchange = 1 / float(rij[9])
                    m.append(oddchange)
                except:
                    continue

            elif rij[6] == teamnaam:
                if rij[8] > rij[7]:
                    puntenreeks = puntenreeks + 3
                elif rij[7] == rij[8]:
                    puntenreeks = puntenreeks + 1
                
                try:
                    oddchange = 1 / float(rij[10])
                    m.append(oddchange)
                except:
                    continue

        try:    
            oddvorm = round(sum(m) / len(m),2)
        except:
            continue
        
        puntenverwachting = round(oddvorm * 3,2)
        puntenreal = round(puntenreeks / len(m),2)
        puntenvorm = round(puntenreal - puntenverwachting,2)

        newratings = [avg,countrie,league,teamnaam,aantal,winst,gelijk,punten,0,0,puntenverwachting,puntenreal,puntenvorm,0]
        teamlist_array.append(newratings) 

        # print("{}: {} verwachting: {}, real: {}, vorm: {} odds: {}".format(teamnaam,puntenreeks,puntenverwachting,puntenreal,puntenvorm,m))        

    teamlist_array.sort(reverse=True)

    p = 0
    oldrank = "0"
    i = 0

    for rij in teamlist_array:
        i = i + 1
        newrank = round(rij[7] / rij[4],2)
        newrank = str(newrank)
        newrank = newrank.replace('.','')
        output_list = [li for li in difflib.ndiff(newrank, oldrank) if li[0] != ' ']  
        
        if len(output_list) > 0:   
            p = i
            oldrank = newrank

        if p / aantal_teams <= 0.25:
            group = 1
        elif p / aantal_teams <= 0.50:
            group = 2
        elif p / aantal_teams <= 0.75:
            group = 3
        else:
            group = 4

        rij[8] = p
        rij[9] = group
    
    for elem in teamlist_array:
        avg = elem[0]
        elem[13] = avg
        elem.remove(elem[0])


    with open(output_file, mode='wt', encoding='utf-8', newline='') as myfile:
        writer = csv.writer(myfile)
        writer.writerows(teamlist_array)



    # l = l + 1

    now2 = datetime.now() 

    c = now2-now1 
    print('Difference: ', c)

if __name__ == "__main__":
    getdata("complist.csv")