from django.db.models import Count
from papertracker.models import Conference, ConfAuthor, ConfPaper, CSCat
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import statistics

cat = CSCat.objects.get(id=10)
ids = ConfPaper.objects.all().values_list('conf').distinct()
confs = Conference.objects.filter(id__in=ids, cscat=cat).order_by('name', '-year')

count=0
temp = ''
author_set = ConfAuthor.objects.none()
i=0
set_prev= set()
inter = []
year = []
mean = []
years = []
datas = []
set_prev= set()
tot_years = []
tot_vals = []

for conf in confs:
    if count == 0:
        temp = conf.name
    
    if conf.name == temp:
        papers = ConfPaper.objects.filter(conf=conf).values_list('id').distinct()
        authors = ConfAuthor.objects.filter(paper__in=papers)
        r = authors.values('name').annotate(c=Count('name')).order_by('-c')[:20]
        author_set |= r
        author_list = []
        number_list = []
        for a in r:
            author_list.append(a['name'])
            number_list.append(a['c'])
        
        
        title = str(conf.year) +'\n single' if conf.single == True else str(conf.year) + '\n double'
        #datas.append(number_list)
        if i == 0:
            set_prev = set(author_list)
        if i > 0:
            inter.append(len(set_prev.intersection(set(author_list))))
            years.append(conf.year)
            tot_years.append(conf.year)
            tot_vals.append(len(set_prev.intersection(set(author_list))))
        i+=1
    else:
        base = range(len(datas))
        plt.plot(years, inter, label=temp)
        print(temp, inter)
        datas = []
        temp = conf.name
        
        i = 1
        inter = []
        year = []
        mean = []
        years = []   
        papers = ConfPaper.objects.filter(conf=conf).values_list('id').distinct()
        authors = ConfAuthor.objects.filter(paper__in=papers)
        r = authors.values('name').annotate(c=Count('name')).order_by('-c')[:20]
        author_set |= r
        author_list = []
        number_list = []
        for a in r:
            author_list.append(a['name'])
            number_list.append(a['c'])
        
        
        title = str(conf.year) +'\n single' if conf.single == True else str(conf.year) + '\n double'
        #datas.append(number_list)
        
        set_prev = set(author_list)
        
    count+=1
if len(inter) > 2:
    plt.plot(years, inter, label=temp)
    print(temp, inter)
plt.title(cat.name)    
plt.legend()
plt.show()

m, b = np.polyfit(tot_years, tot_vals, 1)
m = float(m)
print(m,b)
plt.plot(tot_years, tot_vals, 'o')
tot_years = np.array(tot_years)
plt.plot(tot_years, m*tot_years + b)
plt.title(cat.name)
plt.show()
