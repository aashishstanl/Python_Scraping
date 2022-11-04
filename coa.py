# This is the scraping code in python for the usnews.com

#importing modules
from gettext import gettext
import re
from socket import timeout
from sqlite3 import Row
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import openpyxl

# requesting to the page
print("-----------------Please wait, Scraping going on!-----------------" )
try:
    #Add the file for scraping in line 18 in html format
    with open("./usaeducation.html") as fp:

        soup = BeautifulSoup(fp, "html.parser")

        # storing the university detail 
        list_of_university = soup.select('li h3')

        list_of_University = []
        cost_of_books_url = []
        
        for item in list_of_university:
            university = item.find('a', attrs = {'class':'Anchor-byh49a-0 hWoTvt'}).text 

            #finding the href of the books
            href = item.a['href']
            
            list_of_University.append(university)
            cost_of_books_url.append(href)
        
        print(len(list_of_University))
        
        #storing  city and state of the university
        City =[]
        State = []
        list_of_city = soup.findAll('p', attrs = {'class':'Paragraph-sc-1iyax29-0 dtHrAA'})
        for item in list_of_city:
            Address = item.get_text(strip = True).split(',')

            if(len(Address) == 2):
                city = Address[0]
                state = Address[1]
            else:
                city = 'unknown'
                state = Address[0]
            
            City.append(city)
            State.append(state)
        
        cost = []
        for li in soup.find('ol', class_='BigSixResults__OrderedList-sc-19pb4sw-4 lkwNHw').find_all('div', attrs= {'class':'Box-w0dun1-0 DetailCardCompare__CardSidebar-sc-1x70p5o-3 dSmsjE gAVhxx Hide-kg09cx-0 hWOBmI'}):
            cost.append(list(li.stripped_strings))
        print(len(cost))

        #appending the all attributes/detail in one list
        cost_detail = []
        for index, item in enumerate(cost):
            item_ = [i for i in item if i != 'undefined'] 
            item_.insert(0, list_of_University[index])
            item_.append(City[index])
            item_.append(State[index])
            item_.append('Education')     #enter the course type before running(e.i, Engineering or Education etc)
            item_.append(cost_of_books_url[index])
            cost_detail.append(item_)

        

# #creating dataframe
        df = pd.DataFrame(cost_detail)
        print(df.head(10))
        print(df.columns)

# #formating dataframe       
#---------------------------for education coa  and all other course---------------------------------------
# #.filter 

        #Naming the columns
        df.columns = ['University', 'b', 'Cost', 'd', 'Tuition', 'Duration', 'g', 'h', 'i', 'j', 'City', 'State', 'Type', 'Books_href']
        #removing the university which doesn't have the Tuition cost
        df = df[df['Cost']!= "N/A"]
        #droping the not required columns
        df.drop(labels=['b','Cost','d','g', 'h', 'i', 'j'], axis=1, inplace=True)
        #creating the extra columns for the credit  and separate from the Tuition column
        def get_per_credit(row):
            if 'per credit' in row['Duration']:
                return row['Tuition']
            else:
                return None

        def get_cost(row):
            if 'per credit' in row['Duration']:
                return None
            else:
                return row['Tuition']
        #copying the credit into the 'Credit' column & and initialize 'none' in Tuition instead credit 
        df['Credit'] = df.apply(lambda row: get_per_credit(row), axis=1)
        df['Tuition'] = df.apply(lambda row: get_cost(row), axis=1)
        #arranging the columns in required format
        df = df.reindex(['University','Tuition',  'Credit','Duration', 'City', 'State', 'Type', 'Books_href'], axis=1)
        
        print(df.columns.tolist())
        #Name the filename before running the code to store the scraped COA in csv file
        df.to_csv("./Education.csv", index=True)  

except Exception as e:
    print(e)
