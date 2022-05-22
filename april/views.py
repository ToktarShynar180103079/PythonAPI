import csv
import json
import os
from urllib import response
from django_tex.core import compile_template_to_pdf
from django.http import HttpResponse
from django.shortcuts import render
import jsonpickle
import pickle
import requests
import requests
import time

from django_tex.shortcuts import render_to_pdf
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


def homePage(request):
    return render(request, "april/home.html")

def faq(request):
    return render(request, "april/faqhelp.html")

def about(request):
    return render(request, "april/about.html")

def contact(request):
    return render(request, "april/contacthelp.html")

def authors(request):
    if request.method == "POST":
        attempt_num = 0  # keep track of how many times we've retried
        while attempt_num < 3:
            url = 'http://127.0.0.1:8000/api/authors'
            fname = request.POST.get("name", "Name")
            fsname = request.POST.get("lastname", "Surname")
            payload = {'name': fname, 'lastname': fsname, 'content_type':'application/json'}
            r = requests.post(url, data=payload)
            if r.status_code == 200:
                data = r.json()
                return render(request, "april/author.html",{'response_data':data, 'name': fname, 'lastname': fsname, 'len': len(data)})
            else:
                attempt_num += 1
                # You can probably use a logger to log the error here
                time.sleep(1)  # Wait for 5 seconds before re-trying
        return Response({"error": "Request failed"}, status=r.status_code)
    else:
        return Response({"error": "Method not allowed"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def publications(request, id):
    if request.method == "POST":
        attempt_num = 0  # keep track of how many times we've retried
        while attempt_num < 3:
            url = 'http://127.0.0.1:8000/api/publications'
            payload = {'index': id, 'content_type':'application/json'}
            r = requests.post(url, data=payload)
            if r.status_code == 200:
                data = r.json()
                with open("exp.pickle", "wb") as f:
                    pickle.dump(data, f)
                return render(request, "april/publication.html",{'response_pub':data[1][1:], 'response_aut':data[0][0], 'index': id, 'len': len(data[1])})
            else:
                attempt_num += 1
                time.sleep(1)  # Wait for 5 seconds before re-trying
        return Response({"error": "Request failed"}, status=r.status_code)
    else:
        return Response({"error": "Method not allowed"}, status=status.HTTP_400_BAD_REQUEST)

def getbibtext(pub_list):
    ResList = []
    for item in pub_list:
        ob = ''
        ob = ob + str(item['authors']) + ', '
        title = str(item['title'])
        title = title.replace('&', '\&')
        ob = ob + '\href{' + str(item['link']) + '}{' + title + '}, '
        wherePublished = str(item['wherePublished'])
        ob = ob + wherePublished + ', ' + str(item['year'])
        if str(item['PP']) != "":
            ob = ob + ', pp.' + str(item['PP']) + '.'
        ResList.append(ob)
    return ResList

def exporttopdf(request):
    with open("exp.pickle", "rb") as fp:  # Unpickling
        PubList = pickle.load(fp)
    ResList = getbibtext(PubList[1][1:])
    AuthorInf = PubList[0][0]
    template_name = "april/sometexfile.tex"
    context = {'name': AuthorInf['surname']  + ' ' + AuthorInf['name'], 'publist': ResList, 'aff': AuthorInf['affilation'], 'country': AuthorInf['country'], 'orcid': AuthorInf['orcidId']}
    return render_to_pdf(request, template_name, context, filename='pdfpublications.pdf')

def exporttocsv(request):
    with open("exp", "rb") as fp:  # Unpickling
        PubList = (pickle.load(fp))[1]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csvpublication.csv"'
    writer = csv.writer(response)
    writer.writerow(['Site', 'Title', 'Authors', 'Type', 'HtmlLink',  'Publisher', 'Year', 'Pages'])
    for item in PubList[1:]:
        writer.writerow([
            item['site'],
            item['title'],
            item['authors'],
            item['type'],
            item['link'],
            item['wherePublished'],
            item['year'],
            item['PP']])
    return response
