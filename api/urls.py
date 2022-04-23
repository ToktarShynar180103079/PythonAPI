from django.urls import path
from . import views



urlpatterns = [
    path('authors', views.getAuthors),
    path('publications', views.getPublications),
]