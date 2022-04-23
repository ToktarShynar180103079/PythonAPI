from django.urls import path
from .views import homePage
from django.contrib import admin

urlpatterns = [
    path('', homePage)
]
