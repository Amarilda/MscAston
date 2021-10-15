import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup
import datetime

def ss():
    connection = sqlite3.connect('MSC/marmelade.db')
    cursor = connection.cursor()
    sql = ("select * from  sludinajumi")
    df = pd.read_sql_query(sql,connection)

    existing = []
    for i in df.Url:
        existing.append(i[17:])

    print(len(existing))
    started = len(existing)

    #Loop through pages
    urls = []
    urls.append('https://www.ss.lv/lv/real-estate/flats/jurmala/sell/')
    for i in range(1, 16):
        dz = "https://www.ss.lv/lv/real-estate/flats/jurmala/sell/page"+str(i)+".html"
        urls.append(dz)    

    #Include all Jurmala. After EDA can reduce it to +- 5 km.m 
    a = []
    for url in urls:
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, features="lxml")
        for link in soup.find_all('a', href=True):
            if link['href'].startswith( '/msg' ) and link['href'] not in a and link['href'] not in existing:
                a.append(link['href'])

    if len(a) ==0:
        pass
    else:
        url_ss = "https://www.ss.lv"
        for i in a:
            ex = []
            bildes = []
            full_web_address = url_ss+i
            #print(full_web_address)
            ex.append(full_web_address)
            r = requests.get(full_web_address)
            data = r.text
            soup = BeautifulSoup(data, features="lxml")   
            table_MN = pd.read_html(full_web_address)

            frames = [table_MN[3], table_MN[4], table_MN[5]]
            result = pd.concat(frames)

            for i in ['Pilsēta:', 'Rajons:', 'Iela:', 'Istabas:','Platība:','Stāvs:', 'Sērija:', 'Mājas tips:', 'Ērtības:','Cena:']:
                if i in result[0].unique():
                    ex.append(result.loc[result[0] == i, (1)].item())
                else:
                    ex.append('FALSE')
            if table_MN[7].shape[0] == 4:
                ex.append(table_MN[7][2][1][8:])
                ex.append(table_MN[7][2][2][28:])
            else:
                ex.append(table_MN[8][2][1][8:])
                ex.append(table_MN[8][2][2][28:])
            #Datums
            ex.append(str(datetime.datetime.now()))
            ex.append({str(soup.find_all("div", {"id": "msg_div_msg"}))})
            
            for link in soup.find_all('a', href=True):
                if 'gallery' in link['href']:
                    bildes.append(link['href'])
            ex.append(bildes)       
            df.loc[len(df)]= ex
        print(len(df)-len(existing))
        connection = sqlite3.connect('MSC/marmelade.db')
        cursor = connection.cursor()
        df = df.applymap(str)
        df[started:].to_sql('sludinajumi', connection, index = False, if_exists = 'append')
        connection.commit()
        connection.close()
    print()