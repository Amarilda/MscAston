#cd '/Users/Edite/Documents/GitHub/MscAston/MSC'
#python capitals.py

import random
import datetime
import pandas as pd
import sqlite3

print('Hello world')
print()
name = input('State your name: ').title() or 'Anders'

df = pd.read_csv('country_hist.csv')
session_id = 1 if pd.isnull(df.session[df.name == name].max()) == True else df.session[df.name == name].max()+1
print(f'Hello {name}! {session_id}')
#print(f'____________________________________ {session_id} _________________________________________\n')
df2 = pd.read_csv('capitals.csv')
df2 = df2[df2.capital.isin(['Riga', 'Oslo'])].reset_index(drop = True)

chance = 10
tries = chance
number = len(df2)
counter = 0

print(f'You have {chance} tries')

while number > 0 and chance > 0:
    atbilde = []   
    num = random.randint(0, number-1)
    atbilde.append((datetime.datetime.now()).date())
    atbilde.append(name)
    atbilde.append(session_id)
    atbilde.append(df2['country'][num])
    atbilde.append(df2['capital'][num])

    print()
    print(df2['country'][num])
    answer= input().strip().lower()
    atbilde.append(answer)      
    if df2['capital'][num].lower() != answer:
        atbilde.append(0)
        print(df2['capital'][num])
        chance -= 1
        print(f'You have {chance} tries left')
    else:
        atbilde.append(1)
        df2 = df2.drop(num).reset_index(drop = True)
        number -= 1
        counter += 1
    df.loc[len(df)]= atbilde

if chance == 0:
    print(f'\n{name}, seriously??? Do you even like capitals?\n')
    precision = round((counter/(counter+tries))*100 if counter != 0 else 0.00,2)
    print(f'Correct answers: {counter}\nPrecision: {precision}%\n')
else:
    ending = 's' if chance >1 else ""
    print(f'\nYou finished with {chance} unused chance{ending}')
    precision = round((counter/(counter+tries-chance))*100 if counter != 0 else 0.00,2)
    print(f'Correct answers: {counter}\nPrecision: {precision}%\n')

df.to_csv('country_hist.csv', index = False)
answer = [datetime.datetime.now(), name, session_id, precision]
fame = pd.read_csv('fame.csv')
fame.loc[len(fame)]= answer

print('____________________________HALL OF FAME_________________________________\n')
top10 = fame[['name','precision']].sort_values(by = 'precision', ascending = False).reset_index(drop = True)[:10]
for i in range(0, len(top10)):
    print(top10.name[i], top10.precision[i])
fame.to_csv('fame.csv', index=False)

    