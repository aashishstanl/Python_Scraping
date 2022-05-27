from posixpath import split
import openpyxl
import requests
from bs4 import BeautifulSoup
import pandas as pd

#creating the excel

excel = openpyxl.Workbook()
sheet = excel.active
#giving the name of the excel file
sheet.title = 'COA of Northeastern'

#appending the columns in the sheets
sheet.append(['University','Programs','Cost of program'])

try:
    url = 'https://catalog.northeastern.edu/graduate/expenses/tuition-fees/'
    # getting the request
    page = requests.get(url)
    page.raise_for_status()
    soup = BeautifulSoup(page.content, 'html.parser')

    university = soup.title.get_text().split('<')[1]

    #getting the all program details via loop
    
    ProgramDetail = soup.find('tbody').find_all('tr')
#Iterating through the courses and fees
    for programs in ProgramDetail:
        #all the courses
        Courses = programs.select('td', class_ = 'column0')[0].text
        #all the costs
        Costs = programs.select('td', class_ = 'column1')[1].text
        #adding the columns into the sheet
        sheet.append([university,Courses,Costs])
    
except Exception as e:
    print(e)
#saving the file
excel.save('COA.xlsx')