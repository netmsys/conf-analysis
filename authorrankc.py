from django.db.models import Count
from papertracker.models import Conference, ConfAuthor, ConfPaper, CSCat
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import statistics

def numpy_fillna(data):
    # Get lengths of each row of data
    lens = np.array([len(i) for i in data])

    # Mask of valid places in each row
    mask = np.arange(lens.max()) < lens[:,None]

    # Setup output array and put elements from data into masked positions
    out = np.zeros(mask.shape, dtype=data.dtype)
    out[mask] = np.concatenate(data)
    return out

cat = CSCat.objects.get(id=2)
ids = ConfPaper.objects.all().values_list('conf').distinct()
confs = Conference.objects.filter(id__in=ids, cscat=cat).order_by('name', '-year')

count=0
temp = ''
author_set = ConfAuthor.objects.none()
i=1
set_prev= set()
inter = []
year = []
mean = []
years = []
cont = []
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
        
        print(conf.name, conf.year, author_list, number_list)
        if conf.single == True:
            title = str(conf.year) +'\n single'  
        elif conf.double == True:
            title = str(conf.year) +'\n double' 
        else:
            title = str(conf.year) +'\n unknwn'
        
        mean.append(statistics.mean(number_list))
        years.append(conf.year)
        tot_years.append(conf.year)
        tot_vals.append(statistics.mean(number_list))
        
    else:
        #print(author_set.count(), ' / ', author_set.values('name').distinct().count())
        #print(inter)
        #print(years)
        author_set = ConfAuthor.objects.none()
        #fig.suptitle(temp)
        #plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
        #plt.tick_params(axis='x', which='major', pad=15)
        #plt.show()
        cont.append(mean)
        if len(mean) > 2:
            plt.plot(years, mean, label=temp)
            print(temp, mean)
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
        tot_years.append(conf.year)
        tot_vals.append(statistics.mean(number_list))
        
    count+=1   
if len(mean) > 2:
    plt.plot(years, mean, label=temp)
    print(temp, mean)
plt.legend()
plt.show()
'''
c = np.array(cont, dtype=object)
print(c)
c = numpy_fillna(c)
c = np.mean(c, axis=0)
print(c, years)
y = range(2011, 2011+len(c))
plt.plot(y, c)
plt.show()
'''
m, b = np.polyfit(tot_years, tot_vals, 1)
m = float(m)
print(m,b)
plt.plot(tot_years, tot_vals, 'o')
tot_years = np.array(tot_years)
plt.plot(tot_years, m*tot_years + b)
plt.title(cat.name)
plt.show()




