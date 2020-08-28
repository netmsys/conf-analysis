import csv
import json
import requests
from papertracker.models import ConfPaper, ConfAuthor, Conference

csvfile = open('C:/Users/Mattia/Pictures/csrankings.csv', encoding='utf-8')
a = requests.get('https://dblp.org/search/publ/api/?q=ASPLOS%202011&format=json&h=1000')
c = a.json()
conf = Conference.objects.get(id=375)
spamreader = csv.reader(csvfile)
inst = 'None'
 
for items in c['result']['hits']['hit']:
	cc = ConfPaper.objects.create(conf=conf, title=items['info']['title'])     
	cc.save()
	for it in items['info']:
		if 'authors' in it:
			for i in items['info']['authors']['author']:
				if isinstance(i, dict):
					check = False
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


