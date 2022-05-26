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