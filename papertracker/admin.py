from django.contrib import admin

# Register your models here.
from .models import Institution, Area, Paper, Author, Organization, Conference, Category, ConfAuthor, ConfPaper, CSCat

admin.site.register(Institution)
admin.site.register(Area)
admin.site.register(Paper)
admin.site.register(Author)
admin.site.register(Organization)
admin.site.register(Conference)
admin.site.register(Category)
admin.site.register(ConfAuthor)
admin.site.register(ConfPaper)
admin.site.register(CSCat)
