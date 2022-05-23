from django.urls import path
from . import views



urlpatterns = [
    path('authors', views.getAuthors, name='authors'),
    path('scopusauthor', views.getscopusauthor, name='scopusauthor'),
    path('publications', views.getPublications, name='publications')
]