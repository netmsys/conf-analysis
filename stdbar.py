from django.db.models import Count
from papertracker.models import Conference, ConfAuthor, ConfPaper, CSCat
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import statistics
import sys
import subprocess

count=0
temp = ''
author_set = ConfAuthor.objects.none()
i=1
set_prev= set()
inter = []
year = []
mean = []
years = []
datas = []
y=[]
devs = []
cat = CSCat.objects.get(id=12)

cont = []
confers = []

cats = CSCat.objects.all()
for cat in cats:
    confs = Conference.objects.filter(cscat=cat).order_by('name', '-year')
#print(confs.values('name', 'year').distinct())
    for conf in confs:
        #print(count, confs.count()-1)
        if count == 0:
            temp = conf.name
        if conf.name == temp:
            #print(conf)
            papers = ConfPaper.objects.filter(conf=conf).values_list('id').distinct()
            authors = ConfAuthor.objects.filter(paper__in=papers)
            r = authors.values('name').annotate(c=Count('name')).order_by('-c')[:20]
            author_set |= r
            author_list = []
            number_list = []
            for a in r:
                author_list.append(a['name'])
                datas.append(a['c'])
            
            title = str(conf.year) +'\n single' if conf.single == True else str(conf.year) + '\n double'
            #datas.append(number_list)
            y.append(conf.year)
            if i == 0:
                set_prev = set(author_list)
            if i > 0:
                if len(author_list) > 2:
                    inter.append(len(set_prev.intersection(set(author_list))))
                    years.append(conf.year)
            i+=1
        else:
        
            base = range(len(datas))
            #print(temp, statistics.stdev(datas)) 
            if len(datas) > 2:
                print(temp, statistics.stdev(datas))
                cont.append(statistics.stdev(datas))
                confers.append(temp)
            
            
                #print(temp, statistics.stdev(inter))
                devs.append(statistics.stdev(inter))
                #cc.append(temp)
            datas = []
            
            temp = conf.name
            #count = -1
            i = 0
            inter = []
            year = []
            mean = []
            years = []   
            y=[]
    
        count+=1
if len(datas) > 2:
    print(temp, statistics.stdev(datas))
    cont.append(statistics.stdev(datas))
    confers.append(temp)  

    print(temp, statistics.stdev(inter))
    devs.append(statistics.stdev(inter))
    #cc.append(temp)   


print('correlation coefficient', np.corrcoef(cont, devs))      
ind = np.arange(len(confers))
width = 0.4

fig, ax = plt.subplots()
ax.barh(ind, devs, width, color='red', label='TOP20 INTERSECTION')
ax.barh(ind + width, cont, width, color='green', label='TOP20 PUBL. NUMBER')

ax.set(yticks=ind + width, yticklabels=confers)
ax.legend()

plt.show()   
'''
plt.barh(confers, cont)
plt.title('STD DEV')
plt.show()
'''    
   
