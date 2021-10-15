import pandas as pd
import datetime

def ThinkingTheFeelings():
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
        print()
    else:
        print('You got this')
        pass
