from django.db import models
from django.db.models.fields import BooleanField

# Create your models here.
class Institution(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
            return str(self.name)
    
class Area(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
            return str(self.name)

class Paper(models.Model):
    title = models.CharField(max_length=200)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    year = models.IntegerField()
    single = models.BooleanField(default=False)
    double = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
            return str(self.institution.name) + ' - ' + str(self.area.name) + ' - ' + str(self.title) + ' - ' + str(self.year) 
    
class Author(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    
    def __str__(self):
            return str(self.paper.id) + ' - ' + str(self.name)

class Organization(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
            return str(self.name)  
        
class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
            return str(self.name)      

class CSCat(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
            return str(self.name)    

class Conference(models.Model):
    name = models.CharField(max_length=200)
    fullname = models.CharField(max_length=500)
    organizer = models.ForeignKey(Organization, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    cscat = models.ForeignKey(CSCat, on_delete=models.CASCADE, default=1)
    year = models.IntegerField()
    single = models.BooleanField(default=False)
    double = models.BooleanField(default=False)
    unknown = models.BooleanField(default=False)
    
    def __str__(self):
            return str(self.name) + ' - ' + str(self.year)
        
class ConfPaper(models.Model):
    conf = models.ForeignKey(Conference, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
            return str(self.conf.name) + ' - ' + str(self.conf.year) + ' - ' + str(self.title) 
        
class ConfAuthor(models.Model):
    paper = models.ForeignKey(ConfPaper, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    
    def __str__(self):
            return str(self.paper.id) + ' - ' + str(self.paper.conf.name) + ' - ' + str(self.paper.conf.year) + ' - ' + str(self.name) + ' - ' + str(self.institution)
    
         
    
