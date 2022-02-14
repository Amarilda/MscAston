import pandas as pd
import datetime
from docxlatex import Document
import shutil
import os

def ThinkingTheFeelings():
    df = pd.read_csv("/Users/Edite/Documents/GitHub/KPI/feelings.csv")
    if pd.to_datetime(df.date[len(df)-1]) != (datetime.datetime.now()).date():
        answer = []
        datums = (datetime.datetime.now()).date()
        print(datums.strftime('%d/%m/%y'))
        answer.append(datums)                   
        for i in df.columns[1:]:
            print(i)
            i = input() or 0
            answer.append(i)           
        df.loc[len(df)] = answer
        df.to_csv("/Users/Edite/Documents/GitHub/KPI/feelings.csv", index = False) 
    else:
        print('You got this')
        pass

    # This is Amarilda
    df = pd.read_csv('MSC/amarilda.csv')
    atbilde = []
    atbilde.append(datetime.datetime.now())
    doc = Document("/Users/Edite/Desktop/Amarilda.docx")
    text = doc.get_text()
    atbilde.append(len(text.split()))
    df.loc[len(df)] = atbilde
    df.to_csv('MSC/amarilda.csv', index = False)
  
    if df['word count'].iloc[-1] == df['word count'].iloc[-2]:
            df = pd.read_csv('MSC/amarilda.csv')
            maximums = max(df['word count'])
            if (datetime.date.today() - pd.to_datetime(min(df.entry_date[df['word count'] == int(maximums) ])).date()).days >= 3:
                print('Please top up your Path Authoring')
    else:
        print('Self authoring. Words written: ', df['word count'].iloc[-1] - df['word count'].iloc[-2])
        print('short: '+ str(round(df['word count'].iloc[-1]/(7*6*1000)*100,1)) +'% done, long: ' +str(round(df['word count'].iloc[-1]/(7*6*3000)*100,1)) +'% done')

        ## read the doc    
        doc = Document("/Users/Edite/Desktop/Amarilda.docx")
        text = doc.get_text()

        # extract chapters from the table of contents
        chapters = []

        for i in text[20:text.find('8 Lessons, rules for bright future')+38].split('\n\n'):
            if len(i) != 3 and len(i) != 4:
                i = i.strip()
                # remove heading number and ending page number
                i = i[:i.find('\t')]
                chapters.append(i)  

        start = text.find('Please describe in detail up to six significant experiences that happened to you during this period of your life. You can describe positive and negative experiences. 1k-3k\n\n')+len('Please describe in detail up to six significant experiences that happened to you during this period of your life. You can describe positive and negative experiences. 1k-3k\n\n')
        # extract text after the table of contents
        bodies = text[start:]

        df = pd.DataFrame(columns = ['chapter','heading', 'start', 'title length'])
        main = pd.read_csv('MSC/amarilda_hist.csv')
        for chapter in chapters:
            df.loc[len(df)] = [chapter[:chapter.find(' ')], chapter[chapter.find(' ')+1:], bodies.find(chapter[chapter.find(' ')+1:]), len(chapter[chapter.find(' ')+1:])]

        ending = list(df['start'][1:])
        ending.append(len(bodies))
        df['end'] = ending

        word_count = []
        for i in range(0,len(df)):
            word_count.append(len(bodies[df.start[i]:df.end[i]].split())-len(df.heading[i].split()))
        df['word count'] = word_count
        df['date'] = datetime.date.today()
        df = df[['date','chapter','heading', 'word count']]
        main.append(df).to_csv('MSC/amarilda_hist.csv', index = False)

        #create a cony of file for future NLP
        os.chdir('/Users/Edite/Desktop')
        renFolder= '/Volumes/Seagate Backup Plus Drive/Learning/Past Authoring'
        oldname = 'Amarilda.docx'
        newname= 'Amarilda_'+datetime.date.today().strftime('%Y_%m_%d') +'.docx'
        shutil.copy(oldname, renFolder+'/'+newname)