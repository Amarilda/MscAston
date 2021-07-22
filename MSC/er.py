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
from credentials import credentials
from data import *

client_id, client_secret,password, user_agent, username = credentials

import datetime as dt
df = pd.read_csv("/Users/Edite/Documents/GitHub/KPI/feelings.csv")
answer = []

datums = datetime.datetime.now() - datetime.timedelta(days=1)
answer.append(datums)        
       
for i in df.columns[1:]:
    print(i)
    i = input() or 0
    answer.append(i)
    
df.loc[len(df)] = answer
df.to_csv("/Users/Edite/Documents/GitHub/KPI/feelings.csv", index = False) 
print("One day closer to year in pixels")

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