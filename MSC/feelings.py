import pandas as pd
import datetime
from docxlatex import Document

def ThinkingTheFeelings():
    df = pd.read_csv("/Users/Edite/Documents/GitHub/KPI/feelings.csv")
    if pd.to_datetime(df.date[len(df)-1]) != (datetime.datetime.now()).date():
        answer = []

        #datums = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
        datums = (datetime.datetime.now()).date()
        print(datums.strftime('%d/%m/%y'))
        answer.append(datums)        
            
        for i in df.columns[1:]:
            print(i)
            i = input() or 0
            answer.append(i)
            
        df.loc[len(df)] = answer
        df.to_csv("/Users/Edite/Documents/GitHub/KPI/feelings.csv", index = False) 
        print("One day closer to year in pixels")
        print()
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
