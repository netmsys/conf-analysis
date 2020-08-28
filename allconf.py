from django.db.models import Count
from papertracker.models import Conference, ConfAuthor, ConfPaper
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import statistics

ids = ConfPaper.objects.all().values_list('conf').distinct()
confs = Conference.objects.filter(id__in=ids).exclude(year=2020).order_by('name', '-year')

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
tot_years = []
tot_vals = []

for conf in confs:
    if count == 0:
        temp = conf.name
    
    if conf.name == temp:
        papers = ConfPaper.objects.filter(conf=conf).values_list('id').distinct()
        authors = ConfAuthor.objects.filter(paper__in=papers)
        r = authors.values('name').annotate(c=Count('name')).order_by('-c')[:5]
        author_set |= r
        author_list = []
        number_list = []
        for a in r:
            author_list.append(a['name'])
            datas.append(a['c'])
        
        years.append(conf.year)
        mean.append(statistics.mean(datas))
        tot_years.append(conf.year)
        tot_vals.append(statistics.mean(datas))
        title = str(conf.year) +'\n single' if conf.single == True else str(conf.year) + '\n double'
        #datas.append(number_list)
        
    else:
        base = range(len(datas))
        print(temp, years, datas)
        plt.plot(years, mean, label=temp)
        #plt.plot(datas, label=temp)
        datas = []
        temp = conf.name
        i = 1
        inter = []
        year = []
        mean = []
        years = []   
        papers = ConfPaper.objects.filter(conf=conf).values_list('id').distinct()
        authors = ConfAuthor.objects.filter(paper__in=papers)
        r = authors.values('name').annotate(c=Count('name')).order_by('-c')[:5]
        author_set |= r
        author_list = []
        number_list = []
        for a in r:
            author_list.append(a['name'])
            datas.append(a['c'])
        
        years.append(conf.year)
        mean.append(statistics.mean(datas))
        tot_years.append(conf.year)
        tot_vals.append(statistics.mean(datas))
        title = str(conf.year) +'\n single' if conf.single == True else str(conf.year) + '\n double'
        
    
    count+=1
    
plt.legend(ncol=3)#bbox_to_anchor=(0, 1), loc='upper left', ncol=1)
#plt.xticks(years)
plt.show()
#plt.savefig('allconf_mean_dist.png')

m, b = np.polyfit(tot_years, tot_vals, 1)
m = float(m)
print(m,b)
plt.plot(tot_years, tot_vals, 'o')
tot_years = np.array(tot_years)
plt.plot(tot_years, m*tot_years + b)
plt.title(cat.name)
plt.show()
