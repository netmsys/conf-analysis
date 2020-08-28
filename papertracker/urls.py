from django.urls import path

from . import views

app_name = 'papertracker'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:conf>/', views.conference, name='conference'),
]