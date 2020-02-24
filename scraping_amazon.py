#!/usr/bin/env python
# coding: utf-8

# In[5]:


from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import xlsxwriter
import pandas as pd

counter = 1
lastnum = ''

#     leverage the pattern in url to loop through all pages
while True:
    page_url = 'https://www.amazon.com/s?k=table+lamp&crid=2E4P43QLFK3P8&qid=1582534745&sprefix=table+%2Caps%2C387&ref=sr_pg_' + str(counter)  
#     opens the connection and downloads html page from url
    uClient = uReq(page_url)
    page_soup = soup(uClient.read(), "html.parser")
    uClient.close()
    
    # use Dataframe library to temporarily store the information
    data = pd.DataFrame(columns = ('Name','Rating','Price','Discount','Earliest_Arrivel_Time'))

    # finds each product from the store page
    containers = page_soup.findAll("div", {"class": "a-section a-spacing-medium"})
    for container in containers:
    #         if the grid is not about actual table lamp, skip it
        if container.h5:
            continue       
        name = container.findAll('a',{"class": "a-link-normal a-text-normal"})[0].text.strip()

    #         if there's no rating, mark it 
        if len(container.findAll('div',{'class':'a-row a-size-small'})) == 0:
            rating = 'No rating available'
        else:
            view = container.findAll('div',{'class':'a-row a-size-small'})
            score = view[0].findAll('span')[0]['aria-label']
            viewer = view[0].findAll('span')[3]['aria-label']
            rating = score+ ' (' + viewer+ 'viewers)'

        price = '$' + container.findAll('a',{"class": "a-size-base a-link-normal s-no-hover a-text-normal"})[0].text.strip().split('$')[1]

    #     if there's no discount, mark it
        if len(container.findAll('span',{'class':'s-coupon-unclipped '})) == 0:
            discount = 'N/A'
        else:
            discount = container.findAll('span',{'class':'s-coupon-unclipped '})[0].span.text.strip()

    #     if there's no specified time, mark it
        if len(container.findAll('div',{'class':'a-row s-align-children-center'})) == 0 or         len(container.findAll('div',{'class':'a-row s-align-children-center'})[0].findAll('span',{'class':'a-text-bold'})) == 0:
            time = 'N/A'
        else:
            time = container.findAll('div',{'class':'a-row s-align-children-center'})[0].findAll('span',{'class':'a-text-bold'})[0].text

    #     create a new row in data for each product
        item = pd.DataFrame([[name,rating,price,discount,time]],columns = ('Name','Rating','Price','Discount','Earliest_Arrivel_Time'))
        data = data.append(item,ignore_index = True)
        
    #     check if current page is the last page
    if counter == 1:
        lastnum = page_soup.find("li",{"class":"a-disabled"}).text
    else:
        if lastnum != page_soup.find("li",{"class":"a-disabled"}).text:
            break  
    counter += 1    
    

#     transport the information from Dataframe to Excel
workbook=xlsxwriter.Workbook('C:\\Users\\kkevi\\Desktop\\Amazon_scraping.xlsx')
worksheet=workbook.add_worksheet()

for col in range(len(data.columns)):
    worksheet.write(0,col,data.columns[col])
    
for row in range(len(data.index)):
    for col in range((len(data.columns))):
        worksheet.write(row+1, col, data[data.columns[col]][row])

workbook.close()


# In[ ]:




