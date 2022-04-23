from django.http import HttpResponse
from django.shortcuts import render
from . import *

def homePage(request):
    return render(request, "180103018.html")
    # return HttpResponse("Hello")
