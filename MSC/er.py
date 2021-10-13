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
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from credentials import *
from data import *

#thinking your feelings
import datetime as dt
df = pd.read_csv("/Users/Edite/Documents/GitHub/KPI/feelings.csv")
if pd.to_datetime(df.date[len(df)-1]) != (datetime.datetime.now() - datetime.timedelta(days=1)).date():
    answer = []

    datums = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
    print(datums.strftime('%d/%m/%y'))
    answer.append(datums)        
        
    for i in df.columns[1:]:
        print(i)
        i = input() or 0
        answer.append(i)
        
    df.loc[len(df)] = answer
    df.to_csv("/Users/Edite/Documents/GitHub/KPI/feelings.csv", index = False) 
    print("One day closer to year in pixels")
else:pass

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    password=password,
    user_agent=user_agent,
    username=username,
)
print(reddit.user.me())

###TOP30 Reddit daily table
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
a = f"cursor.execute('CREATE TABLE if not exists {thisday} ({createtable} )')"
eval(a)
    
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

#NYT new articles
connection = sqlite3.connect('MSC/ny.db')
cursor = connection.cursor()
sql = ("select _id || ' ' || strftime('%d-%m-%Y', pub_date) as ids from articles where strftime('%m', pub_date) = strftime('%m', date()) and strftime('%Y', pub_date) = strftime('%Y', date())")
dd = pd.read_sql_query(sql,connection)
ignore = list(dd.ids)

from nytimes_scraper.nyt_api import NytApi
api = NytApi(api_key)

df = pd.DataFrame(columns = ['_id','abstract',
 'web_url',
 'snippet',
 'lead_paragraph',
 'source',
 'multimedia',
 'keywords',
 'pub_date',
 'document_type',
 'news_desk',
 'section_name',
 'type_of_material',
 'word_count',
 'uri',
 'text',
 'subsection_name',
 'print_section',
 'print_page',
 'headline.main',
 'headline.kicker',
 'headline.content_kicker',
 'headline.print_headline',
 'headline.name',
 'headline.seo',
 'headline.sub',
 'byline.original',
 'byline.person',
 'byline.organization'] )

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

date=datetime.datetime.now().date()

articles = api.archive.archive(date.year, date.month)['response']['docs']
for article in articles:
    if str(article['_id']+' '+  pd.to_datetime(article['pub_date']).strftime('%d-%m-%Y')) in ignore:
        pass      
    else:
        atbilde = []

        for columns in ['_id', 'abstract', 'web_url', 'snippet', 'lead_paragraph', 'source','multimedia', 'keywords', 'pub_date', 'document_type', 'news_desk','section_name', 'type_of_material', 'word_count', 'uri', 'text', 'subsection_name', 'print_section','print_page']:
            try:
                atbilde.append(article[columns])
            except:
                atbilde.append('')

        for i in ['headline.main', 'headline.kicker', 'headline.content_kicker','headline.print_headline', 'headline.name', 'headline.seo','headline.sub', 'byline.original', 'byline.person','byline.organization']:
            try:
                m, n = i.split('.')
                atbilde.append(article[m][n])
            except:
                atbilde.append('')
        df.loc[len(df)] = atbilde

if len(df) == 0:pass
else:
    print(datetime.datetime.now())
    print(len(df))

    df = df[['_id', 'abstract', 'web_url', 'snippet', 'lead_paragraph', 'source',
        'multimedia', 'keywords', 'pub_date', 'document_type', 'news_desk',
        'section_name', 'type_of_material', 'word_count', 'uri', 'text',
        'headline.main', 'headline.kicker', 'headline.content_kicker',
        'headline.print_headline', 'headline.name', 'headline.seo',
        'headline.sub', 'byline.original', 'byline.person',
        'byline.organization', 'subsection_name', 'print_section',
        'print_page']]

    df.pub_date = pd.to_datetime(df.pub_date).dt.tz_convert('America/New_York')
    df.to_csv('xxxx.csv', index = False)
    df = pd.read_csv('xxxx.csv')

    connection = sqlite3.connect('MSC/ny.db')
    cursor = connection.cursor()
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

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    password=password,
    user_agent=user_agent,
    username=username,
)
print(reddit.user.me())

print("Starting Wallstreets bets")
#Getting tickers for sp500
connection = sqlite3.connect('MSC/MSC.db')
cursor = connection.cursor()
sql = ("Select symbol from SP500_companies")
df = pd.read_sql_query(sql,connection)
us = df['Symbol'].to_list()
# set the program parameters
subs = ['wallstreetbets' ]     # sub-reddit to search
post_flairs = {'Daily Discussion', 'Weekend Discussion', 'Discussion'}    # posts flairs to search || None flair is automatically considered
goodAuth = {'AutoModerator'}   # authors whom comments are allowed more than once
uniqueCmt = True                # allow one comment per author per symbol
ignoreAuthP = {'example'}       # authors to ignore for posts 
ignoreAuthC = {'example'}       # authors to ignore for comment 
upvoteRatio = 0.70         # upvote ratio for post to be considered, 0.70 = 70%
ups = 20       # define # of upvotes, post is considered if upvotes exceday
#
limit = 500     # define the limit, comments 'replace more' limit
upvotes = 2     # define # of upvotes, comment is considered if upvotes exceed this #

posts, count, c_analyzed, tickers, titles, a_comments, cmt_auth = 0, 0, 0, {}, [], {}, {}

subreddit = reddit.subreddit('wallstreetbets')
hot_python = subreddit.hot()    # sorting posts by hot
# Extracting comments, symbols from subreddit
for submission in hot_python:
    try:
        flair = submission.link_flair_text 
        author = submission.author.name         

        # checking: post upvote ratio # of upvotes, post flair, and author 
        if submission.upvote_ratio >= upvoteRatio and submission.ups > ups and (flair in post_flairs or flair is None) and author not in ignoreAuthP:   
            submission.comment_sort = 'new'     
            comments = submission.comments
            titles.append(submission.title)
            posts += 1
            try: 
                submission.comments.replace_more(limit=limit)   
                for comment in comments:
                    # try except for deleted account?
                    try: auth = comment.author.name
                    except: pass
                    c_analyzed += 1
                    answer = []
                    columnnames = "'date','thread', 'upvote_ratio', 'likes', 'comment'"
                    insertintotable = '?,?,?,?,?'

                    # checking: comment upvotes and author
                    if comment.score > upvotes and auth not in ignoreAuthC: 
                        #df.loc[len(df)] = [submission.title, submission.upvote_ratio, comment.body, comment.score]
                        answer = [datetime.date.today(), submission.title, submission.upvote_ratio, comment.score, comment.body]
                        connection = sqlite3.connect('MSC/MSC.db')
                        cursor = connection.cursor()
                        sql2 = f'cursor.execute("insert INTO  wb_comments ({columnnames}) VALUES ({insertintotable})", {answer})'
                        eval(sql2)
                        connection.commit()
                        connection.close()
                        split = comment.body.split(" ")
                        for word in split:
                            word = word.replace("$", "")        
                            # upper = ticker, length of ticker <= 5, excluded words,                     
                            if word.isupper() and len(word) <= 5 and word not in blacklist and word in us:
                                # unique comments, try/except for key errors
                                if uniqueCmt and auth not in goodAuth:
                                    try: 
                                        if auth in cmt_auth[word]:break
                                    except: pass
                                # counting tickers
                                if word in tickers:
                                    tickers[word] += 1
                                    a_comments[word].append(comment.body)
                                    cmt_auth[word].append(auth)
                                    count += 1
                                else:                               
                                    tickers[word] = 1
                                    cmt_auth[word] = [auth]
                                    a_comments[word] = [comment.body]
                                    count += 1   
            except Exception as e: print(e)
    except:
        pass
# sorts the dictionary
symbols = dict(sorted(tickers.items(), key=lambda item: item[1], reverse = True))
print("wb_comments done")

top_picks = list(symbols.keys())
times = []
top = []
for i in top_picks:
    times.append(symbols[i])
    top.append(f"{i}: {symbols[i]}")
      
# Applying Sentiment Analysis
scores, s = {}, {}
vader = SentimentIntensityAnalyzer()
# adding custom words from data.py 
vader.lexicon.update(new_words)
picks_sentiment = list(symbols.keys())

answer = []
columnnames = "'date', 'symbol', 'neg', 'neu', 'pos', 'compound', 'comment'"
insertintotable = '?,?,?,?,?,?,?'
for symbol in picks_sentiment:
    stock_comments = a_comments[symbol]
    for cmnt in stock_comments:
        score = vader.polarity_scores(cmnt)
        answer = [datetime.date.today(), symbol]
        for i in list(score.values()):
            answer.append(i)
        answer += [cmnt]
        connection = sqlite3.connect('MSC/MSC.db')
        cursor = connection.cursor()
        sql2 = f'cursor.execute("insert INTO  wb_sentiment ({columnnames}) VALUES ({insertintotable})", {answer})'
        eval(sql2)
        connection.commit()
        connection.close()
        
        if symbol in s:
            s[symbol][cmnt] = score
        else:
            s[symbol] = {cmnt:score}      
        if symbol in scores:
            for key, _ in score.items():
                scores[symbol][key] += score[key]
        else:
            scores[symbol] = score
            
    # calculating avg.
    for key in score:
        scores[symbol][key] = scores[symbol][key] / symbols[symbol]
        scores[symbol][key]  = "{pol:.3f}".format(pol=scores[symbol][key])
print("wb_sentiment done")

connection = sqlite3.connect('MSC/marmelde.db')
cursor = connection.cursor()
sql = ("select * from  sludinajumi")
df = pd.read_sql_query(sql,connection)

existing = []
for i in df.Url:
    existing.append(i[17:])

print(len(existing))

#Loop through pages
urls = []
urls.append('https://www.ss.lv/lv/real-estate/flats/jurmala/sell/')
for i in range(1, 16):
    dz = "https://www.ss.lv/lv/real-estate/flats/jurmala/sell/page"+str(i)+".html"
    urls.append(dz)    

if len(a) ==0:pass
else:
    #Include all Jurmala. After EDA can reduce it to +- 5 km.m 
    a = []
    for url in urls:
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data)
        for link in soup.find_all('a', href=True):
            if link['href'].startswith( '/msg' ) and link['href'] not in a and link['href'] not in existing:
                a.append(link['href'])

    url_ss = "https://www.ss.lv"
    for i in a:
        ex = []
        bildes = []
        full_web_address = url_ss+i
        #print(full_web_address)
        ex.append(full_web_address)
        r = requests.get(full_web_address)
        data = r.text
        soup = BeautifulSoup(data)
        #print()    
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
        ex.append(datetime.datetime.now())
        #Advertisment text. Just in case. Todays mission is just to get it working. run now analyse later. 
        ex.append(str(soup.find_all("div", {"id": "msg_div_msg"})))
        
        for link in soup.find_all('a', href=True):
            if 'gallery' in link['href']:
                bildes.append(link['href'])
        ex.append(bildes)       
        df.loc[len(df)]= ex
    print(df.shape)
    connection = sqlite3.connect('MSC/marmelde.db')
    cursor = connection.cursor()
    df.to_sql('sludinajumi', connection, index = False)
    connection.commit()
    connection.close()
print('ss sell scraped')
