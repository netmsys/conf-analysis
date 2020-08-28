from django.db.models import Count
from papertracker.models import Conference, ConfAuthor, ConfPaper
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import statistics

#ids = ConfPaper.objects.all().values_list('conf').distinct()
conf = 'FSE'
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
    
    papers = ConfPaper.objects.filter(conf=conf).values_list('id').distinct()
    authors = ConfAuthor.objects.filter(paper__in=papers)
    r = authors.values('name').annotate(c=Count('name')).order_by('-c')[:limit]
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
    elif conf.unknown == True:
        title = str(conf.year) +'\n unknwn'
    if i == 1:
        set_prev = set(author_list)
        fig, axs = plt.subplots(1, 9, sharey=True)
        axs[i-1].bar(author_list, number_list, width=0.5) #color=np.random.rand(3))
        axs[i-1].set_title(title)
        axs[i-1].axhline(statistics.mean(number_list), color='blue', linewidth=2)
        axs[i-1].tick_params(labelrotation=90)
        #axs[i-1].xticks(rotation=90, ha="right")
        #axs[i-1].legend(author_list, loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)
        mean.append(statistics.mean(number_list))
        years.append(conf.year)
        #axs[i-1].axhline(max(number_list), color='yellow', linewidth=1)
        #axs[i-1].axhline(min(number_list), color='yellow', linewidth=1)
    else:
        print('intersection: ', len(set_prev.intersection(set(author_list))))
        if len(number_list) > 2:
            mean.append(statistics.mean(number_list))
            years.append(conf.year)
            year.append(conf.year)
            inter.append(len(set_prev.intersection(set(author_list))))
            axs[i-1].bar(author_list, number_list, width=0.5) #color=np.random.rand(3))
            axs[i-1].set_title(title)
            axs[i-1].axhline(statistics.mean(number_list), color='blue', linewidth=2)
            #axs[i-1].axhline(len(set_prev.intersection(set(author_list))), color='red', linewidth=2)
            axs[i-1].tick_params(labelrotation=90)
            #axs[i-1].xticks(rotation=90, ha="right")
            #axs[i-1].legend(author_list, loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=1)
            set_prev = set(author_list)
            
            #axs[i-1].axhline(max(number_list), color='yellow', linewidth=1)
            #axs[i-1].axhline(min(number_list), color='yellow', linewidth=1)
        #plt.subplot(1, 9, i)
        #plt.bar(author_list, number_list, width=0.8)
        #plt.set_ylim(0, 10)
    i+=1
        
    
#print(author_set.count(), ' / ', author_set.values('name').distinct().count())
#print(inter)
#print(years)
print('INTER', inter)
author_set = ConfAuthor.objects.none()
#fig.suptitle(temp)
#plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
#plt.tick_params(axis='x', which='major', pad=15)
plt.show()

plt.plot(years, mean, label=temp)
#plt.plot(2018, 1, 'ro')
plt.legend()

#plt.plot(years, mean, color='blue', label='Publications mean')
#plt.legend()
#print('correlation coefficient', np.corrcoef(inter, mean[:len(inter)]))           
#plt.show()
#temp = conf.name
#i = 1
#inter = []
#year = []
#mean = []
#years = []
'''
m, b = np.polyfit(year, inter, 1)
m = float(m)
print(m,b)

year = np.array(year)
plt.plot(year, m*year + b)
plt.title(confs)
'''
plt.plot(2017, 2, 'ro')
plt.show()

   

#plt.hist(r)



count+=1
