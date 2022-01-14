import pickle
import sqlite3
import pandas as pd
import datetime

connection = sqlite3.connect('MSC/ny.db')
cursor = connection.cursor()
sql = ("select max(pub_date) as maxi from articles ")
dd = pd.read_sql_query(sql,connection)
print('max date at the db: ', dd.maxi[0])
last_date = dd.maxi[0]

bank_holidays = [datetime.date(2020, 1, 1),
 datetime.date(2020, 1, 20),
 datetime.date(2020, 2, 17),
 datetime.date(2020, 4, 10),
 datetime.date(2020, 5, 25),
 datetime.date(2020, 7, 4),
 datetime.date(2020, 7, 3),
 datetime.date(2020, 9, 7),
 datetime.date(2020, 11, 26),
 datetime.date(2020, 12, 25),
 datetime.date(2021, 1, 1),
 datetime.date(2021, 12, 31),
 datetime.date(2021, 1, 18),
 datetime.date(2021, 2, 15),
 datetime.date(2021, 4, 2),
 datetime.date(2021, 5, 31),
 datetime.date(2021, 7, 4),
 datetime.date(2021, 7, 5),
 datetime.date(2021, 9, 6),
 datetime.date(2021, 10, 11),
 datetime.date(2021, 11, 11),
 datetime.date(2021, 11, 25),
 datetime.date(2021, 12, 25),
 datetime.date(2021, 12, 24)]

columns_needed = ['_id', 'abstract', 'web_url', 'snippet', 'lead_paragraph', 'source',
       'multimedia', 'keywords', 'pub_date', 'document_type', 'news_desk',
       'section_name', 'type_of_material', 'word_count', 'uri', 'text',
       'headline.main', 'headline.kicker', 'headline.content_kicker',
       'headline.print_headline', 'headline.name', 'headline.seo',
       'headline.sub', 'byline.original', 'byline.person',
       'byline.organization', 'subsection_name', 'print_section',
       'print_page']

i = datetime.datetime.now().month
    
name = 'MSC/2021-'+str(i).zfill(2)+'-articles.pickle'

# Load data (deserialize)
with open(name, 'rb') as handle:
    unserialized_data = pickle.load(handle)
    
unserialized_data.reset_index(inplace = True)
unserialized_data = unserialized_data[columns_needed]

print(len(unserialized_data))
unserialized_data = unserialized_data[unserialized_data.pub_date > last_date]
print(len(unserialized_data))

name2 = 'MSC/2021-'+str(i).zfill(2)+'.csv'
unserialized_data.to_csv(name2, index = False)
del unserialized_data
df = pd.read_csv(name2)
#unserialized_data.pub_date = unserialized_data.pub_date.astype(str)
print(i)

connection = sqlite3.connect('MSC/ny.db')
cursor = connection.cursor()
df.to_sql('articles', connection, index = False, if_exists = 'append')
connection.commit()
connection.close()

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

print(df.w_day.value_counts())
print(len(df))
print(df)

connection = sqlite3.connect('MSC/ny.db')
cursor = connection.cursor()
df.to_sql('main', connection, index = False, if_exists = 'append')
connection.commit()
connection.close()