from bs4 import BeautifulSoup
import time
import csv
import requests

URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"


r = requests.get(URL)


def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)
        
        
save_html(r.content, 'wiki_scrap.html')


headers = ['name','distance','mass','radius']
planet_data = []
for i in range(0,1):
    soup = BeautifulSoup(r.content, 'html.parser')
    for tr_tag in soup.find_all("tr",limit=3):
        td_tags = tr_tag.find_all("td")
        temp = []
        for i,tag in enumerate(td_tags):
            if i == 1:
                try:
                    temp.append(tag.find_all('a')[0].contents[0])
                except:
                    temp.append(tag.contents[0])
 
            elif i ==3 or i==5 or i == 6:
                try:
                    temp.append(int(tag.contents[0]))
                except:
                    temp.append(tag.contents[-1])        
        planet_data.append(temp)
with open('scrapper.csv','w') as f :
        cw=csv.writer(f)   
        cw.writerow(headers)
        cw.writerows(planet_data)       