import csv
import json
import requests
from papertracker.models import ConfPaper, ConfAuthor, Conference

csvfile = open('C:/Users/Mattia/Pictures/csrankings.csv', encoding='utf-8')
a = requests.get('https://dblp.org/search/publ/api/?q=conf/fast/2011$&format=json&h=1000')
c = a.json()
conf = Conference.objects.get(id=715)
spamreader = csv.reader(csvfile)
inst = 'None'
 
for items in c['result']['hits']['hit']:
    if 'venue' in items['info']:
        if items['info']['venue'] == 'FAST':
        #if 'FSE' in items['info']['venue']:
            cc = ConfPaper.objects.create(conf=conf, title=items['info']['title'])     
            cc.save()
            for it in items['info']:
                if 'authors' in it:
                    for i in items['info']['authors']['author']:
                        check = False
                        if isinstance(i, dict):
                            for row in spamreader:
                                if row[0] == i['text']:
                                    check = True
                                    inst = row[1]
                            csvfile.seek(0)
                            if check == True:
                                au = ConfAuthor.objects.create(paper=cc, name=i['text'], institution=inst)
                                au.save()
                            else:
                                au = ConfAuthor.objects.create(paper=cc, name=i['text'], institution='None')
                                au.save()
                                
                            inst = 'None'
                        elif isinstance(i, str):
                            if i == 'text':
                                for row in spamreader:
                                    if row[0] == items['info']['authors']['author']['text']:
                                        check = True
                                        inst = row[1]
                                csvfile.seek(0)
                                if check == True:
                                    au = ConfAuthor.objects.create(paper=cc, name=items['info']['authors']['author']['text'], institution=inst)
                                    au.save()
                                else:
                                    au = ConfAuthor.objects.create(paper=cc, name=items['info']['authors']['author']['text'], institution='None')
                                    au.save()
                                    
                                    inst = 'None'

