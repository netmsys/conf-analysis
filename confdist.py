from django.db.models import Count
from papertracker.models import Conference, ConfAuthor, ConfPaper
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import statistics

#ids = ConfPaper.objects.all().values_list('conf').distinct()
conf = 'USENIX'
limit = 20
confs = Conference.objects.filter(name=conf).exclude(year=2020).order_by('name', '-year')

count=0
temp = ''
author_set = ConfAuthor.objects.none()
i=1
set_prev= set()
inter = []
year = []
mean = []
years = []

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
        
        print(conf.name, conf.year, author_list, number_list)
        if conf.single == True:
            title = str(conf.year) +'\n single'  
        elif conf.double == True:
            title = str(conf.year) +'\n double' 
        else:
            title = str(conf.year) +'\n unknwn'
        
        mean.append(statistics.mean(number_list))
        years.append(conf.year)
        
        
    else:
        print(author_set.count(), ' / ', author_set.values('name').distinct().count())
        #print(inter)
        #print(years)
        author_set = ConfAuthor.objects.none()
        #fig.suptitle(temp)
        #plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
        #plt.tick_params(axis='x', which='major', pad=15)
        #plt.show()
        if len(mean) > 2:
            plt.plot(years, mean, label=temp)
        #plt.plot(year, inter, color='red', label='Authors intersection')
        #plt.legend()
        #plt.plot(years, mean, color='blue', label='Publications mean')
        #plt.legend()
        #print('correlation coefficient', np.corrcoef(inter, mean[:len(inter)]))           
        #plt.show()
        temp = conf.name
        i = 1
        inter = []
        year = []
        mean = []
        years = []
        
    count+=1   
if len(mean) > 2:
    plt.plot(years, mean, label=temp)
plt.legend()
plt.plot(2019, 2.15, 'ro')
plt.show()