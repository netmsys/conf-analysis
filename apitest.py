import csv
import json
import requests
from papertracker.models import ConfPaper, ConfAuthor, Conference

csvfile = open('C:/Users/Mattia/Pictures/csrankings.csv', encoding='utf-8')
a = requests.get('https://dblp.org/search/publ/api/?q=ASPLOS%202020&format=json&h=1000')
c = a.json()
spamreader = csv.reader(csvfile)
inst = 'None'
prev = None
 
for items in c['result']['hits']['hit']:
    for it in items['info']:
        if 'authors' in it:
            for i in items['info']['authors']['author']:
                check = False
                if isinstance(i, dict):
                    print(i['text'])
                    for row in spamreader:
                        if row[0] == i['text']:
                            check = True
                            inst = row[1]
                            print(inst)
                    csvfile.seek(0)
                elif isinstance(i, str):
                    if i == 'text':
                        print('#############', items['info']['authors']['author']['text'])
                        for row in spamreader:
                            if row[0] == items['info']['authors']['author']['text']:
                                check = True
                                inst = row[1]
                                print(inst)
                        csvfile.seek(0)
                    

