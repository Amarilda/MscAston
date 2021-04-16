import requests
from datetime import datetime
import datetime
import pandas as pd
import sqlite3
import praw

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
                
sodiena = str("ER"+datetime.date.today().strftime('%Y%m%d'))

createtable = ""
columnnames = ""
insertintotable = ""

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
a = f"cursor.executescript('DROP TABLE IF EXISTS {sodiena}')"
b = f"cursor.execute('''CREATE TABLE {sodiena} ({createtable} )''')"

eval(a)
eval(b)
    
#An actual webscraping
top_posts = reddit.subreddit('worldnews').top(time_filter='day',limit=30)
i = 1
for post in top_posts:    
    atbilde =[]
    atbilde.append(str(datetime.datetime.now()))
    atbilde.append(str(i))
    for j in kolonas[2:]:
        try:
            atbilde.append(str(eval("post."+j)))
        except:
            atbilde.append("")
    
    connection = sqlite3.connect('MSC/MSC.db')
    cursor = connection.cursor()
    sql2 = f'cursor.execute("insert INTO  {sodiena} ({columnnames}) VALUES ({insertintotable})", {atbilde})'
    eval(sql2)
    connection.commit()
    connection.close()
    
    i +=1
    
print("Individual table is created")

### Append to top 30
connection = sqlite3.connect('MSC/MSC.db')
cursor = connection.cursor()
top_posts = reddit.subreddit('worldnews').top(time_filter='day',limit=30)
i = 1

connection = sqlite3.connect('MSC/MSC.db')
cursor = connection.cursor()
sql = ('Select * from top30')
z = pd.read_sql_query(sql,connection)

for post in top_posts:
    atbilde =[]
    atbilde.append(str(datetime.datetime.now()))
    atbilde.append(str(i))
    for j in z.columns[2:]:
        try:
            atbilde.append(str(eval("post."+j)))
        except:
            atbilde.append("")

    for m in vars(post):
        if m not in z.columns[2:]:
            print(m)
    
    connection = sqlite3.connect('MSC.db')
    cursor = connection.cursor()
    sql2 = ("insert INTO top30('moment', 'daily_rank', 'comment_limit', 'comment_sort', '_reddit', 'approved_at_utc', 'subreddit', 'selftext', 'author_fullname', 'saved', 'mod_reason_title', 'gilded', 'clicked', 'title', 'link_flair_richtext', 'subreddit_name_prefixed', 'hidden', 'pwls', 'link_flair_css_class', 'downs', 'top_awarded_type', 'hide_score', 'name', 'quarantine', 'link_flair_text_color', 'upvote_ratio', 'author_flair_background_color', 'subreddit_type', 'ups', 'total_awards_received', 'media_embed', 'author_flair_template_id', 'is_original_content', 'user_reports', 'secure_media', 'is_reddit_media_domain', 'is_meta', 'category', 'secure_media_embed', 'link_flair_text', 'can_mod_post', 'score', 'approved_by', 'author_premium', 'thumbnail', 'edited', 'author_flair_css_class', 'author_flair_richtext', 'gildings', 'content_categories', 'is_self', 'mod_note', 'created', 'link_flair_type', 'wls', 'removed_by_category', 'banned_by', 'author_flair_type', 'domain', 'allow_live_comments', 'selftext_html', 'likes', 'suggested_sort', 'banned_at_utc', 'url_overridden_by_dest', 'view_count', 'archived', 'no_follow', 'is_crosspostable', 'pinned', 'over_18', 'all_awardings', 'awarders', 'media_only', 'can_gild', 'spoiler', 'locked', 'author_flair_text', 'treatment_tags', 'visited', 'removed_by', 'num_reports', 'distinguished', 'subreddit_id', 'mod_reason_by', 'removal_reason', 'link_flair_background_color', 'id', 'is_robot_indexable', 'report_reasons', 'author', 'discussion_type', 'num_comments', 'send_replies', 'whitelist_status', 'contest_mode', 'mod_reports', 'author_patreon_flair', 'author_flair_text_color', 'permalink', 'parent_whitelist_status', 'stickied', 'url', 'subreddit_subscribers', 'created_utc', 'num_crossposts', 'media', 'is_video', '_fetched', '_comments_by_id', 'author_cakeday', 'flair', 'link_flair_template_id', 'num_duplicates', 'post_hint', 'preview', 'thumbnail_height', 'thumbnail_width','_comments') VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)")
    cursor.execute(sql2, atbilde)          
    connection.commit()
    connection.close()
    
    i +=1

print("Todays data is appended to top30")