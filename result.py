from django.db.models import Count
from papertracker.models import Conference, ConfAuthor, ConfPaper
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import statistics

'''
res = [18, 8, 4]
nam = ['drop&raise', 'flat&raise', 'flat']
plt.barh(nam, res)
plt.title('TOP20 AUTHOR INCREASING INTERSECTIONS TRENDS (SINGLE/DOUBLE)')
#plt.legend()
#plt.plot(years, mean, color='blue', label='Publications mean')
#plt.legend()
plt.show()
'''
labels = 'Decrease&Increase', 'Stable&Increase', 'Stable'
sizes = [63, 27, 10]
explode = (0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()