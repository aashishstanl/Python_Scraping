#importing modules

import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import openpyxl

# requesting to the page
try:
    with open("./usamba.html") as fp:
        soup = BeautifulSoup(fp, "html.parser")

        #obtaining all the universities of the page into the list
        list_of_university = soup.select('li h3')
        list_of_city = soup.findAll('p', attrs = {'class':'Paragraph-sc-1iyax29-0 dtHrAA'})

        list_of_University = []
        cost_of_books_url = []
        #iterating through the university tag to obtain the name of the university
        for item in list_of_university:
            university = item.find('a', attrs = {'class':'Anchor-byh49a-0 hWoTvt'}).text
            
            list_of_University.append(university)
            href = item.a['href']
            cost_of_books_url.append(href)

        print(len(list_of_University))

        City =[]
        State = []
        #list_of_city = soup.findAll('p', attrs = {'class':'Paragraph-sc-1iyax29-0 dtHrAA'})
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


        #accessing the section of the cost of Attendance from the desired location
        result = []
        for li in soup.find('ol', class_='BigSixResults__OrderedList-sc-19pb4sw-4 lkwNHw').find_all('div', attrs={'class':'Box-w0dun1-0 DetailCardCompare__CardSidebar-sc-1x70p5o-3 dSmsjE gAVhxx Hide-kg09cx-0 hWOBmI'}):
            result.append(list(li.stripped_strings))
        
        
        print(len(result))
        
        #formating the cost data to be in 1 row
        results = []
        for index, item in enumerate(result):
            item_ = [i for i in item if i != 'undefined']
            item_.insert(0, list_of_University[index])
            item_.append('MBA')
            item_.append(City[index])
            item_.append(State[index])
            item_.append(cost_of_books_url[index])
           
            #arranging the in-state and out-state cost in separate row
            if item_[3] != 'per year (full-time)'  and item_[3] != 'per credit (full-time)' and item_[3] != 'total program (full-time)' and len(item_) > 7:
                print(item_)
                #item temporory
                item_t = item_.copy()
                new_item_ = item_[0:4] + item_[6:]
                new_item_.remove('TUITION AND FEES')
                
                results.append(new_item_)
                print(new_item_)
                del item_t[2:4]
                #del item_t[3]
                item_t.remove('TUITION AND FEES')
                
                print(item_t)
                results.append(item_t)
                
                
                print('------------------')
            else:
                item_.remove('TUITION AND FEES')
                
                results.append(item_)
                
            
        
        #converting the extracted data  into dataframe
        df = pd.DataFrame(results)
        #Nameing the final columns we have after cleaning
        df.columns = ['University','Tuition', 'Duration', 'd','e','f','g','Type','City', 'State', 'Books_href']
        print(df.columns)
        #separating the credit from the tution fee column
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
        #formating the scraped data
        df.drop(labels=['d', 'e', 'f', 'g'], inplace=True, axis=1)
        #arranging the columns in required format
        df = df.reindex(['University','Tuition',  'Credit','Duration', 'City', 'State', 'Type', 'Books_href'], axis=1)
        #removing the university which doesn't have the Tuition cost
        df = df[df['Tuition']!= "N/A"]
        df = df[df['Duration']!= "AVERAGE GMAT (FULL-TIME)"]
        print(df)
        print(df.columns)
        #storing the scraped data into the csv file
        df.to_csv('./MBA_CO.csv', index=False, header=True)
    
      
except Exception as e:
    print(e)
