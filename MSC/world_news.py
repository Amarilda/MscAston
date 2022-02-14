import praw
from credentials import *
import sqlite3
import pandas as pd
import datetime

def world_news():
    reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    password=password,
    user_agent=user_agent,
    username=username,
    )
    print(reddit.user.me())

    connection = sqlite3.connect('MSC/MSC.db')
    cursor = connection.cursor()
    def tables_in_sqlite_db(conn):
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [
            v[0] for v in cursor.fetchall()
            if v[0] != "sqlite_sequence"
        ]
        cursor.close()
        return tables

    tables = tables_in_sqlite_db(connection)

    if pd.to_datetime(str(tables[-1:])[4:-2], format = "%Y%m%d") == datetime.date.today(): pass 

    else:
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

        ## Append to main. aka transposed top30
        connection = sqlite3.connect('MSC/MSC.db')

        cursor = connection.cursor()
        sql = (f"Select date(moment) as date, title from {thisday}")
        z = pd.read_sql_query(sql,connection)
        answer = []
        columnnames = "'date', 'top1', 'top2', 'top3', 'top4', 'top5', 'top6', 'top7', 'top8', 'top9', 'top10', 'top11', 'top12', 'top13', 'top14', 'top15', 'top16', 'top17', 'top18', 'top19', 'top20', 'top21', 'top22', 'top23', 'top24', 'top25', 'top26', 'top27', 'top28', 'top29', top30"
        insertintotable = '?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?'
        answer = [z.date[0]] +[i for i in  z.title]
        for i in range(0, 31-len(answer)):
            answer.append("")

        connection = sqlite3.connect('MSC/MSC.db')

        cursor = connection.cursor()
        sql2 = f'cursor.execute("insert INTO  main ({columnnames}) VALUES ({insertintotable})", {answer})'
        eval(sql2)
        connection.commit()
        connection.close()
        print("Appended to MAIN")