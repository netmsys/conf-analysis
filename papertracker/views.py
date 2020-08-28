from django.shortcuts import render
from django.http import HttpResponse
from papertracker.models import Institution, Area, Paper, Author, Conference, Organization, Category

# Create your views here.
def get_authors(papers):
    authors = Author.objects.none()
    for paper in papers:
        authors |= Author.objects.filter(paper=paper)
    return authors

def index(request):
    papers = Paper.objects.all()
    authors = get_authors(papers)
    conferences = Conference.objects.filter(year=2020)
    single = Conference.objects.filter(year=2020, single=True).count()
    double = Conference.objects.filter(year=2020, double=True).count()
    return render(request, 'papertracker/index.html', {'papers' : papers, 'authors' : authors, 'conferences' : conferences,
                                                       'single' : single, 'double' : double})
   
   
def conference(request, conf):
    confer = Conference.objects.filter(id=conf)
    if confer.exists():
        confer = confer.first()
    else:
        return redirect('papertracker:index')
    
    confers = Conference.objects.filter(name=confer.name).exclude(year=confer.year)
    single = confers.filter(single=True).count()
    double = confers.filter(double=True).count()
    
    similars = Conference.objects.filter(category=confer.category, year=confer.year, single=confer.single, double=confer.double).exclude(id=confer.id)
    return render(request, 'papertracker/conference.html', {'confer' : confer, 'confers' : confers, 'similars' : similars,
                                                            'single' : single, 'double' : double})
   
    