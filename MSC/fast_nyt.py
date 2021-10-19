import pandas as pd
import sqlite3
from credentials import *
from nytimes_scraper.nyt_api import NytApi
import datetime


def NYT_articles():
    #NYT new articles
    connection = sqlite3.connect('MSC/ny.db')
    cursor = connection.cursor()
    sql = ("select _id || ' ' || strftime('%d-%m-%Y', pub_date) as ids from articles where strftime('%m', pub_date) = strftime('%m', date()) and strftime('%Y', pub_date) = strftime('%Y', date())")
    dd = pd.read_sql_query(sql,connection)
    ignore = list(dd.ids)

    api = NytApi(api_key)
    df = pd.DataFrame(columns = kkolonas)
    date=datetime.datetime.now().date()

    articles = api.archive.archive(date.year, date.month)['response']['docs']
    for article in articles:
        if str(article['_id']+' '+  pd.to_datetime(article['pub_date']).strftime('%d-%m-%Y')) in ignore:pass      
        else:
            atbilde = []
            for columns in ['_id', 'abstract', 'web_url', 'snippet', 'lead_paragraph', 'source','multimedia', 'keywords', 'pub_date', 'document_type', 'news_desk','section_name', 'type_of_material', 'word_count', 'uri', 'text', 'subsection_name', 'print_section','print_page']:
                try:atbilde.append(article[columns])
                except:atbilde.append('')
            for i in ['headline.main', 'headline.kicker', 'headline.content_kicker','headline.print_headline', 'headline.name', 'headline.seo','headline.sub', 'byline.original', 'byline.person','byline.organization']:
                try:
                    m, n = i.split('.')
                    atbilde.append(article[m][n])
                except:atbilde.append('')
            df.loc[len(df)] = atbilde

    if len(df) == 0:pass
    else:
        df = df[kkkolonas]
        df.pub_date = pd.to_datetime(df.pub_date).dt.tz_convert('America/New_York')
        df = df.applymap(str)
        '''
            df.to_csv('xxxx.csv', index = False)
            df = pd.read_csv('xxxx.csv')
        '''
        connection = sqlite3.connect('MSC/ny.db')
        cursor = connection.cursor()
        print(len(df))
        df.to_sql('articles', connection, index = False, if_exists = 'append')
        connection.commit()
        connection.close()
        print('NYT articles entered')
        atbildes = []

        for i in df.pub_date:
            date = pd.to_datetime(i)
            if date.hour >15:
                date_new = date.normalize()+ datetime.timedelta(days=1)
            else:
                date_new = date.normalize()
            while date_new.weekday() >4 or date_new.date() in bank_holidays:
                date_new = date_new.normalize()+ datetime.timedelta(days=1)
            atbildes.append(str(date_new.date()))           
        df['w_day'] = atbildes
        connection = sqlite3.connect('MSC/ny.db')
        cursor = connection.cursor()
        df.to_sql('main', connection, index = False, if_exists = 'append')
        connection.commit()
        connection.close()

        print('NYT main entered')
    print()