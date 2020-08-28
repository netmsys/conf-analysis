from django.db.models import Count
from papertracker.models import Conference, ConfAuthor, ConfPaper, CSCat
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import statistics

#ids = ConfPaper.objects.all().values_list('conf').distinct()
#confs = Conference.objects.filter(id__in=ids).order_by('name', '-year')

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
devs = []
cc = []
cont = []
confers = []

cats = CSCat.objects.all()
for cat in cats:
    confs = Conference.objects.filter(cscat=cat).order_by('name', '-year')

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
                if len(author_list) > 2:
                    inter.append(len(set_prev.intersection(set(author_list))))
                    years.append(conf.year)
            i+=1
        else:
            base = range(len(datas))
            if len(inter) > 2:
                #print(temp, statistics.stdev(inter))
                devs.append(statistics.stdev(inter))
                cc.append(temp)
                cont.append(statistics.stdev(number_list))
                confers.append(temp)
                #plt.plot(years, inter, label=temp)
            datas = []
            temp = conf.name
            
            i = 0
            inter = []
            year = []
            mean = []
            years = []   
            #cont = []
            confers = []
        count+=1
    
if len(inter) > 2:
    print(temp, statistics.stdev(inter))
    devs.append(statistics.stdev(inter))
    cc.append(temp)
    cont.append(statistics.stdev(number_list))
    confers.append(temp)
    #plt.plot(years, inter, label=temp)
    

ind = np.arange(len(cc))
width = 0.4

fig, ax = plt.subplots()
ax.barh(ind, devs, width, color='red', label='N')
ax.barh(ind + width, cont, width, color='green', label='M')

ax.set(yticks=ind + width, yticklabels=cc)
ax.legend()

plt.show()
'''
plt.barh(cc, devs, color='blue')
plt.barh(confers, cont, color='red')
plt.title('Yearly Top 20 author intersection')    
plt.legend()
plt.show()
'''