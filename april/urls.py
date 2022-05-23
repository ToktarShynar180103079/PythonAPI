from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name = 'home'),
    path('faq', views.faq, name = 'faq'),
    path('about', views.about, name = 'about'),
    path('contact', views.contact, name = 'contact'),
    path('authors', views.authors, name='authors'),
    path('publications/<int:id>', views.publications, name='publications'),
    path('exporttopdf', views.exporttopdf, name='exporttopdf'),
    path('exporttocsv', views.exporttocsv, name='exporttocsv'),
    path('scopusauthor', views.scopusauthor, name='scopusauthor')
]
