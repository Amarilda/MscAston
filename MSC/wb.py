import pandas as pd
import praw, datetime
import sqlite3
from credentials import *
from data import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def stonks():
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        password=password,
        user_agent=user_agent,
        username=username,)

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
        except:pass
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
            else:scores[symbol] = score
        # calculating avg.
        for key in score:
            scores[symbol][key] = scores[symbol][key] / symbols[symbol]
            scores[symbol][key]  = "{pol:.3f}".format(pol=scores[symbol][key])
    print("wb_sentiment done")