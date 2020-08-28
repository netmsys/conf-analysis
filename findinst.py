import csv
import json
import requests
from papertracker.models import ConfPaper, ConfAuthor, Conference

authors = open('C:/Users/Mattia/Downloads/authors.csv', encoding='utf-8')
affiliations = open('C:/Users/Mattia/Downloads/affiliations.csv', encoding='utf-8')


authreader = csv.reader(authors)
affireader = csv.reader(affiliations)

#x = Conference.objects.filter(name="SIGMOD", year="2017").first()
#y = ConfPaper.objects.filter(conf=x).first()
#confs = ConfPaper.objects.filter(id__gte=y.id, institution='None')
##confs = ConfAuthor.objects.filter(institution='None')
#confs = ConfAuthor.objects.filter(id__gte=institution='None')
ids = Conference.objects.filter(name="FAST").values_list('id').distinct()
paps = ConfPaper.objects.filter(conf__in=ids).values_list('id').distinct()
confs = ConfAuthor.objects.filter(paper__in=paps)


for conf in confs:
    for row in authreader:
        name = row[1] + ' ' + row[2]
        #print(name)
        #result = ''.join([i for i in conf.name if not i.isdigit()])
        #print(conf.name, result)
        if name == conf.name:
            inst_id = row[4]
            
            for r in affireader:
                if r[0] == inst_id:
                    c = ConfAuthor.objects.get(id=conf.id)
                    c.institution = r[1]
                    c.save()
                    print(c)
                    break
                    break
                    
            affiliations.seek(0)
    authors.seek(0)
    
 
