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
acount = []
stdd = []
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
        
        
        if conf.single == True:
            title = str(conf.year) +'\n single'  
        elif conf.double == True:
            title = str(conf.year) +'\n double' 
        else:
            title = str(conf.year) +'\n unknwn'
        if i == 1:
            
            #axs[i-1].legend(author_list, loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)
            mean.append(statistics.mean(number_list))
            stdd.append(statistics.stdev(number_list))
            tot_years.append(conf.year)
            tot_vals.append(statistics.stdev(number_list))
            years.append(conf.year)
            acount.append(authors.values('name').distinct().count())
            #axs[i-1].axhline(max(number_list), color='yellow', linewidth=1)
            #axs[i-1].axhline(min(number_list), color='yellow', linewidth=1)
        else:
            
            mean.append(statistics.mean(number_list))
            stdd.append(statistics.stdev(number_list))
            tot_years.append(conf.year)
            tot_vals.append(statistics.stdev(number_list))
            years.append(conf.year)
            year.append(conf.year)
            acount.append(authors.values('name').distinct().count())
            inter.append(len(set_prev.intersection(set(author_list))))
            
            #axs[i-1].legend(author_list, loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=1)
            set_prev = set(author_list)
            
            #axs[i-1].axhline(max(number_list), color='yellow', linewidth=1)
            #axs[i-1].axhline(min(number_list), color='yellow', linewidth=1)
        #plt.subplot(1, 9, i)
        #plt.bar(author_list, number_list, width=0.8)
        #plt.set_ylim(0, 10)
        i+=1
        
    else:
        
        print(temp, stdd)
        plt.plot(years, stdd, label=temp)
        #print(inter)
        #print(years)
        author_set = ConfAuthor.objects.none()
        temp = conf.name
        i = 1
        inter = []
        year = []
        mean = []
        years = [] 
        acount = []
        stdd = []
        
        papers = ConfPaper.objects.filter(conf=conf).values_list('id').distinct()
        authors = ConfAuthor.objects.filter(paper__in=papers)
        r = authors.values('name').annotate(c=Count('name')).order_by('-c')[:20]
        author_set |= r
        author_list = []
        number_list = []
        for a in r:
            author_list.append(a['name'])
            number_list.append(a['c'])
        
        
        if conf.single == True:
            title = str(conf.year) +'\n single'  
        elif conf.double == True:
            title = str(conf.year) +'\n double' 
        else:
            title = str(conf.year) +'\n unknwn'
        if i == 1:
            
            #axs[i-1].legend(author_list, loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)
            mean.append(statistics.mean(number_list))
            stdd.append(statistics.stdev(number_list))
            tot_years.append(conf.year)
            tot_vals.append(statistics.stdev(number_list))
            years.append(conf.year)
            acount.append(authors.values('name').distinct().count())
            #axs[i-1].axhline(max(number_list), color='yellow', linewidth=1)
            #axs[i-1].axhline(min(number_list), color='yellow', linewidth=1)
        else:
            
            mean.append(statistics.mean(number_list))
            stdd.append(statistics.stdev(number_list))
            tot_years.append(conf.year)
            tot_vals.append(statistics.stdev(number_list))
            years.append(conf.year)
            year.append(conf.year)
            acount.append(authors.values('name').distinct().count())
            inter.append(len(set_prev.intersection(set(author_list))))
            
            #axs[i-1].legend(author_list, loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=1)
            set_prev = set(author_list)
            
            #axs[i-1].axhline(max(number_list), color='yellow', linewidth=1)
            #axs[i-1].axhline(min(number_list), color='yellow', linewidth=1)
        #plt.subplot(1, 9, i)
        #plt.bar(author_list, number_list, width=0.8)
        #plt.set_ylim(0, 10)
        i+=1
        
       
    
    #plt.hist(r)
    
    
    
    count+=1
plt.legend(ncol=3)
plt.show()

m, b = np.polyfit(tot_years, tot_vals, 1)
m = float(m)
print(m,b)
plt.plot(tot_years, tot_vals, 'o')
tot_years = np.array(tot_years)
plt.plot(tot_years, m*tot_years + b)
plt.title(cat.name)
plt.show()