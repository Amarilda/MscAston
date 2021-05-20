import pandas as pd
import requests
from datetime import datetime
import datetime
import sqlite3
import praw
from bs4 import BeautifulSoup
import re
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
from credentials import credentials

client_id, client_secret,password, user_agent, username = credentials

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    password=password,
    user_agent=user_agent,
    username=username,
)
print(reddit.user.me())

###Individual table
top_posts = reddit.subreddit('worldnews').top(time_filter='day',limit=30)

#Get all unique columns
kolonas = ['moment', 'daily_rank']   
for post in top_posts:
     for m in vars(post):
            if m not in kolonas:
                kolonas.append(m)
thisday = str("ER"+datetime.date.today().strftime('%Y%m%d'))
createtable, columnnames, insertintotable = "", "", ""

#Create strings for SQL injection
z = len(kolonas)
for k in kolonas:
    if z > 1:
        createtable+= str(k + " TEXT,")
        columnnames += str(f"'{k}', ")
        insertintotable += str("?,")        
    else:
        createtable+= str(k + " TEXT")
        columnnames += str(k)
        insertintotable += str("?")
    z+= -1
    
#Drop and create the todays table
connection = sqlite3.connect('MSC/MSC.db')
cursor = connection.cursor()
a = f"cursor.executescript('DROP TABLE IF EXISTS {thisday}')"
b = f"cursor.execute('CREATE TABLE {thisday} ({createtable} )')"
eval(a)
eval(b)
    
#An actual webscraping
top_posts = reddit.subreddit('worldnews').top(time_filter='day',limit=30)
i = 1
for post in top_posts:    
    answer =[]
    answer.append(str(datetime.datetime.now()))
    answer.append(str(i))
    for j in kolonas[2:]:
        try:
            answer.append(str(eval("post."+j)))
        except:
            answer.append("")
    
    connection = sqlite3.connect('MSC/MSC.db')
    cursor = connection.cursor()
    sql2 = f'cursor.execute("insert INTO  {thisday} ({columnnames}) VALUES ({insertintotable})", {answer})'
    eval(sql2)
    connection.commit()
    connection.close()    
    i +=1    
print("Individual table is created")

'''
### Append to top 30
top_posts = reddit.subreddit('worldnews').top(time_filter='day',limit=30)
i = 1

connection = sqlite3.connect('MSC/MSC.db')
cursor = connection.cursor()
sql = ('Select * from top30')
z = pd.read_sql_query(sql,connection)

for post in top_posts:
    answer =[]
    answer.append(str(datetime.datetime.now()))
    answer.append(str(i))
    for j in z.columns[2:]:
        try:
            answer.append(str(eval("post."+j)))
        except:
            answer.append("")

    for m in vars(post):
        if m not in z.columns[2:]:
            print(m)
    
    connection = sqlite3.connect('MSC/MSC.db')
    cursor = connection.cursor()
    sql2 = ("insert INTO top30('moment', 'daily_rank', 'comment_limit', 'comment_sort', '_reddit', 'approved_at_utc', 'subreddit', 'selftext', 'author_fullname', 'saved', 'mod_reason_title', 'gilded', 'clicked', 'title', 'link_flair_richtext', 'subreddit_name_prefixed', 'hidden', 'pwls', 'link_flair_css_class', 'downs', 'top_awarded_type', 'hide_score', 'name', 'quarantine', 'link_flair_text_color', 'upvote_ratio', 'author_flair_background_color', 'subreddit_type', 'ups', 'total_awards_received', 'media_embed', 'author_flair_template_id', 'is_original_content', 'user_reports', 'secure_media', 'is_reddit_media_domain', 'is_meta', 'category', 'secure_media_embed', 'link_flair_text', 'can_mod_post', 'score', 'approved_by', 'author_premium', 'thumbnail', 'edited', 'author_flair_css_class', 'author_flair_richtext', 'gildings', 'content_categories', 'is_self', 'mod_note', 'created', 'link_flair_type', 'wls', 'removed_by_category', 'banned_by', 'author_flair_type', 'domain', 'allow_live_comments', 'selftext_html', 'likes', 'suggested_sort', 'banned_at_utc', 'url_overridden_by_dest', 'view_count', 'archived', 'no_follow', 'is_crosspostable', 'pinned', 'over_18', 'all_awardings', 'awarders', 'media_only', 'can_gild', 'spoiler', 'locked', 'author_flair_text', 'treatment_tags', 'visited', 'removed_by', 'num_reports', 'distinguished', 'subreddit_id', 'mod_reason_by', 'removal_reason', 'link_flair_background_color', 'id', 'is_robot_indexable', 'report_reasons', 'author', 'discussion_type', 'num_comments', 'send_replies', 'whitelist_status', 'contest_mode', 'mod_reports', 'author_patreon_flair', 'author_flair_text_color', 'permalink', 'parent_whitelist_status', 'stickied', 'url', 'subreddit_subscribers', 'created_utc', 'num_crossposts', 'media', 'is_video', '_fetched', '_comments_by_id', 'author_cakeday', 'flair', 'link_flair_template_id', 'num_duplicates', 'post_hint', 'preview', 'thumbnail_height', 'thumbnail_width','_comments') VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)")
    cursor.execute(sql2, answer)          
    connection.commit()
    connection.close()    
    i +=1
print("Todays data is appended to top30")

----delete bfore this
'''


### Append to main. aka transposed top30
connection = sqlite3.connect('MSC/MSC.db')
cursor = connection.cursor()
sql = (f"Select date(moment) as date, title from {thisday}")
z = pd.read_sql_query(sql,connection)
answer = []
columnnames = "'date', 'top1', 'top2', 'top3', 'top4', 'top5', 'top6', 'top7', 'top8', 'top9', 'top10', 'top11', 'top12', 'top13', 'top14', 'top15', 'top16', 'top17', 'top18', 'top19', 'top20', 'top21', 'top22', 'top23', 'top24', 'top25', 'top26', 'top27', 'top28', 'top29', top30"
insertintotable = '?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?'
answer = [z.date[0]] +[i for i in  z.title]

connection = sqlite3.connect('MSC/MSC.db')
cursor = connection.cursor()
sql2 = f'cursor.execute("insert INTO  main ({columnnames}) VALUES ({insertintotable})", {answer})'
eval(sql2)
connection.commit()
connection.close()
print("Appended to MAIN")

#for symbol in df
connection = sqlite3.connect('MSC/MSC.db')
cursor = connection.cursor()

sql = (f'''
Select symbol from SP500_companies 
where symbol not in (select distinct symbol from prices where date == "2021-05-19 00:00:00")
and  symbol not in ('BRK.B', 'BF.B', 'FLIR')'''
    )
df = pd.read_sql_query(sql,connection)

connection = sqlite3.connect('MSC/MSC.db')
cursor = connection.cursor()
sql = ("Select * from prices order by date desc")
z = pd.read_sql_query(sql,connection)
connection.commit()
connection.close()

columnnames = "'date', 'open', 'high', 'low', 'close', 'adj_close','volume', 'symbol'"
insertintotable = '?,?,?,?,?,?,?,?'

for i in df.Symbol:
    r = requests.get(f'https://finance.yahoo.com/quote/{i}/history?p={i}')
    print(f'https://finance.yahoo.com/quote/{i}/history?p={i}')
    data = r.text
    soup = BeautifulSoup(data, features="lxml")
    
    for j in range (0, len(soup.find_all('td'))):
        try:
            if (type(pd.to_datetime(soup.find_all('td')[j].text,infer_datetime_format=True)) == pd._libs.tslibs.timestamps.Timestamp) == True and isinstance(locale.atof(soup.find_all('td')[j+1].text), (int, float, complex)) == True and pd.to_datetime(soup.find_all('td')[j].text,infer_datetime_format=True) > pd.to_datetime(z.date[z.symbol == i].iloc[0]):
                #print(pd.to_datetime(soup.find_all('td')[j].text,infer_datetime_format=True))
                answer = []
                answer.append(str(pd.to_datetime(soup.find_all('td')[j].text,infer_datetime_format=True)))
                answer = answer + [i.span.text for i in soup.find_all('td')[j+1: j+7]] + [i]
                print(answer)

                connection = sqlite3.connect('MSC/MSC.db')
                cursor = connection.cursor()
                sql2 = f'cursor.execute("insert INTO  prices ({columnnames}) VALUES ({insertintotable})", {answer})'
                eval(sql2)
                connection.commit()
                connection.close()

            else: pass
        except:pass            
print('Price injection done')

import datetime as dt
df = pd.read_csv("/Users/Edite/Documents/GitHub/KPI/feelings.csv")
answer = []

datums = datetime.datetime.now() - datetime.timedelta(days=1)
answer.append(datums)        
       
for i in df.columns[1:]:
    print(i)
    i = input()
    answer.append(i)
    
df.loc[len(df)] = answer
df.to_csv("/Users/Edite/Documents/GitHub/KPI/feelings.csv", index = False) 
print("One day closer to year in pixels")