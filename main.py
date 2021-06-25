#this program uses bs4 and requests to fetch data from a wikipedia article about bright stars
#it stores it as a csv file using the csv module
from bs4 import BeautifulSoup
# import time
import csv
import requests

#creating a variable for our URL
URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

#requesting data
r = requests.get(URL)

#storing our data as a html file using a function
def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)
        
#calling the function        
save_html(r.content, 'wiki_scrap.html')

#creating a headers list ('we will just be getting two rows of stars with their names, distances in light-years, masses and their radiuses')
headers = ['name','distance','mass','radius']
planet_data = [] #creating a planet_data list to store our final data
for i in range(0,1): #we will only be running this one time as our table is a one whole table, the for loop isn;t necessary, but just clarifies the code to use when you have multiple tables
    soup = BeautifulSoup(r.content, 'html.parser') # creating a BeautifulSoup object, bs4 is a parser which, parses or makes the data compatible to work with
    for tr_tag in soup.find_all("tr",limit=3): # we our finding 3 tr tags, the headers, and two rows
        td_tags = tr_tag.find_all("td") # we are finding all the td tags which contain the info we need
        temp = []                          # creating a temp listb to store our data
        for i,tag in enumerate(td_tags): #the enumerate function returns the index and the value
            if i == 1:      #if its the  2nd column or the 1st index, its our name
                try:
                    temp.append(tag.find_all('a')[0].contents[0]) #we will append the 0th index of 0th index of an a tag if the td tag contains an a tag instead of simply the name. a tag is used to link urls
                except:
                    temp.append(tag.contents[0]) #we will simply append the 0th index, if its simply the name
 
            elif i ==3 or i==5 or i == 6: # these indexes contain the remaining headers ; distance, mass ,radius
                try:
                    temp.append(float(tag.contents[0])) # if its simply either of them, as the 1st element, we will convert them to float. 
                except:
                    temp.append(tag.contents[-1])     # if its not them, the exception block will work, appending the last element NOTE: THE FLOAT IS SIMPLY TO CHECK WHETHER THE DATA IS A NUMBER
        planet_data.append(temp) #appending all temp data into our final list

#creating and writing all the data into a csv file        
with open('scrapper.csv','w') as f :
        cw=csv.writer(f)   #creating a csv writer
        cw.writerow(headers) #writerow writes only 1 row, which is the headers over here
        cw.writerows(planet_data)       #wriiterows will write multiple rows, which is our remaning data over here