#!/usr/bin/env python
# coding: utf-8

# In[4]:


import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests
import datetime
timestart = datetime.datetime.now()
import cx_Oracle
import db_config
con = cx_Oracle.connect(db_config.user, db_config.pw, db_config.dsn)

link = pd.read_excel(r'C:\Users\vishal.lote\loan_project\Tender_Links.xlsx')
urls = list(link['STATE_URL'].str.split("?", n= 1, expand=False).str[0])
dataset = []
for url in urls:
    try:
        options = Options()
        options.headless = False
        options.add_argument('--headless')
        driver = webdriver.Chrome(executable_path=r'C:\Users\vishal.lote\Downloads/chromedriver.exe',options=options)
        links = []
        driver.get(url + "?page=FrontEndTendersByOrganisation&service=page")
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        name_div = soup.find('table', {'id':"table",'class': 'list_table'})
        gdp_table_data = name_div.findAll("td")
        for tr in gdp_table_data:
            cols = tr.find_all('a')
            cols = [ele.get('href').strip() for ele in cols]
            links.append([ele for ele in cols if ele])
        data = pd.DataFrame(links)
        data.dropna(inplace = True)
        data.reset_index(drop = True, inplace = True)
        link1 = pd.DataFrame(data[0].str.split("?", n= 1, expand=False).str[1])
        all_data = []
        for x in range(0, len(link1[0].index)):
            driver.get(url +'?'+ link1[0][x])
#             driver.find_element_by_id('restart').click()
#             driver.get(url +'?'+ link1[0][x])
            src = driver.page_source
            soup1 = BeautifulSoup(src, 'lxml')
            name_div = soup1.find('table', {'id':"table",'class': 'list_table'})
            table = soup1.find("table",{"class":"list_table"})
            columns = [i.get_text(strip=True) for i in table.find_all("th")]
            data2 = []
            data3 = []
            for tr in table.find("tbody").find_all("tr"):
                data2.append([td.get_text(strip=True) for td in tr.find_all("td")])
            data2 = pd.DataFrame(data2)
            data2 = data2.iloc[1:].reset_index()

            name_div = soup1.find('table', {'id':"table",'class': 'list_table'})
            gdp_table_data = name_div.findAll("td")
            for tr in gdp_table_data:
                cols = tr.find_all('a')
                cols = [ele.get('href').strip() for ele in cols]
                data3.append([ele for ele in cols if ele])
            data3 = pd.DataFrame(data3)
            data3.dropna(inplace = True)
            data3.reset_index(drop = True, inplace = True)
            link3 = pd.DataFrame(data3[0].str.split("?", n= 1, expand=False).str[1])
            link3.columns = ['Link']
            link3['Link'] = url #+ '?'+ link3['Link'].astype(str)
            data = pd.concat([data2, link3], axis = 1)
            all_data.append(data)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.max_rows', 500)
        df_temp3 = list(pd.DataFrame(all_data)[0])
        tender_data = pd.concat(df_temp3, axis=0, ignore_index=True)
        tender_data[['A', 'B','C']] = tender_data[4].str.split(']', 2, expand=True)
        tender_data.dropna(inplace = True)
        tender_data = tender_data.drop(['index'],axis=1)
        tender_data = tender_data.rename({0: 'S.No', 1: 'e-Published Date', 2: 'Closing Date', 3: 'Opening Date', 4: 'Title and Ref.No./Tender ID',5:'Organisation Chain','A': 'Title','B': 'Ref.No.','C': 'Tender ID'}, axis=1)
        tender_data = tender_data.rename({'S.No':'IDS','e-Published Date':'e_published_date', 'Closing Date':'closing_date','Opening Date':'opening_date','Organisation Chain':'organisation_chain','Title':'tender_title','Ref.No.':'ref_no','Tender ID':'tender_id','Link':'tender_url'}, axis=1)
        tender_data = tender_data[['IDS','e_published_date','closing_date','opening_date','ref_no', 'tender_id', 'organisation_chain', 'tender_url', 'tender_title']]
        tender_data["ref_no"] = tender_data["ref_no"].str.replace("[", "", regex=True)
        tender_data["tender_id"] = tender_data["tender_id"].str.replace("[", "").str.replace("]", "", regex=True)
        tender_data["tender_title"] = tender_data["tender_title"].str.replace("[", "").str.replace("]", "", regex=True).str.upper()
        
        tender_data = tender_data.rename({'IDS':'IDS','e_published_date':'E_PUBLISHED_DATE', 'closing_date':'CLOSING_DATE','opening_date':'OPENING_DATE','ref_no':'REF_NO','tender_id':'TENDER_ID','organisation_chain':'ORGANISATION_CHAIN','tender_url':'TENDER_URL','tender_title':'TENDER_TITLE'}, axis=1)
        tender_data['IDS'] = tender_data.index
        tender_data['E_PUBLISHED_DATE'] = pd.to_datetime(tender_data['E_PUBLISHED_DATE'])
        tender_data['CLOSING_DATE'] = pd.to_datetime(tender_data['CLOSING_DATE'])
        tender_data['OPENING_DATE'] = pd.to_datetime(tender_data['OPENING_DATE'])
        tender_data = tender_data.fillna(0)
        
        con = cx_Oracle.connect('py/py@192.168.1.42/orcl')
        cursor = con.cursor()
        df_list = tender_data.values.tolist()
        for i in range(len(df_list)):
            cursor.prepare('INSERT INTO py.per_day_tender_data VALUES(:1,:2,:3,:4,:5,:6,:7,:8,:9)')
            cursor.executemany(None,([df_list[i]]))
        con.commit()
        
#         df_list=[ tuple(i) for i in  tender_data.values]
#         sql='INSERT INTO py.per_day_tender_data (IDS, E_PUBLISHED_DATE, CLOSING_DATE, OPENING_DATE, REF_NO,TENDER_ID, ORGANISATION_CHAIN, TENDER_URL, TENDER_TITLE) VALUES(:1,:2,:3,:4,:5,:6,:7,:8,:9)'
#         cursor.executemany(sql,df_list)

        print(url)

    except:
        continue
#     dataset.append(tender_data)
# dataset = pd.concat(dataset)
# dataset.reset_index(drop=True, inplace=True)
# dataset.to_csv(r'C:\Users\vishal.lote\loan_project\web_scrapping\per_day_tender_details4.csv')

con = cx_Oracle.connect('py/py@192.168.1.42/orcl')
cursor = con.cursor()
cursor.execute('Begin pr_insert_tender_data;commit;end;') 
cursor.execute('TRUNCATE TABLE per_day_tender_data')
con.commit()
cursor.close()
con.close()
timeend = datetime.datetime.now()
timedelta = round((timeend-timestart).total_seconds(), 2)
print ("Time taken to execute above cell: " + str(timedelta) + " seconds")   


# In[ ]:





# In[ ]:





# In[ ]:




