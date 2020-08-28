from django.db.models import Count
from papertracker.models import Conference, ConfAuthor, ConfPaper
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import statistics

ids = ConfPaper.objects.all().values_list('conf').distinct()
confs = Conference.objects.filter(id__in=ids).order_by('name', '-year')

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

        title = conf.name + '\n' + str(conf.year) +'\n single' if conf.single == True else conf.name + '\n' + str(conf.year) + '\n double'
        
        set_prev = set(author_list)
        plt.barh(author_list, number_list) #color=np.random.rand(3))
        plt.title(title)
        plt.gca().invert_yaxis()
        plt.show()
            