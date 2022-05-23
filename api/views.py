import json
import jsonpickle
import pickle
import requests
from database.sites.GoogleScholar import scholar_author
from database.sites.Iexplore import iexp_author
from database.sites.Scopus import scopus_author
from threading import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from database.models.Author import Author

from database.sites.GoogleScholar import scholar_pub
from database.sites.Iexplore import iexp_pub
from database.sites.Scopus import scopus_pub


@api_view(['POST'])
def getAuthors(request):
    if request.method == 'POST':
        name = request.POST.get("name", "Name")
        lastname = request.POST.get("lastname", "Surname")
        result = [None] * 3
        t1 = Thread(target=scopus_author, args=(lastname, name, result, 0))
        t2 = Thread(target=iexp_author, args=(lastname, name, result, 1))
        t3 = Thread(target=scholar_author, args=(lastname, name, result, 2))
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()
        print(result[0])
        hashmap = {}     # authors filtration
        for j in range(len(result[0])):
            hashmap[result[0][j].name + result[0][j].surname] = result[0][j]
        for i in range(len(result[1])):
            if result[1][i].name + result[1][i].surname in hashmap:
                hashmap[result[1][i].name + result[1][i].surname].iexpId = result[1][i].iexpId
            else:
                hashmap[result[1][i].name + result[1][i].surname] = result[1][i]
        for k in range(len(result[2])):
            if result[2][0].name + result[2][0].surname in hashmap:
                hashmap[result[2][0].name + result[2][0].surname].scholarUrl = result[2][0].scholarUrl
            else:
                hashmap[result[2][0].name + result[2][0].surname] = result[2][0]

        authors = list(hashmap.values())
        with open("authors", "wb") as fp:
            pickle.dump(authors, fp)
        result = []
        for i in range(len(authors)):
            authors[i].index = i
            result.append(json.loads(authors[i].toJSON()))

        return Response(result, content_type='application/json')

@api_view(['POST'])
def getscopusauthor(request):
    if request.method == 'POST':
        id = request.POST.get("id", "Id")
        publicationsList = scopus_pub(id)
        resultp = [None]
        if(len(publicationsList) != 0):
            for i in range(len(publicationsList[1])):
                resultp.append(json.loads(publicationsList[1][i].toJSON()))
            author = [json.loads(publicationsList[0].toJSON())]
            result = [author, resultp]
        else:
            result=[]

        return Response(result, content_type='application/json')

@api_view(['POST'])
def getPublications(request):
    list_iexp = []
    list_scop = []
    list_scholar = []
    final_authors = []
    with open("authors", "rb") as fp:  # Unpickling
        final_authors = pickle.load(fp)

    index = request.POST.get('index')
    if final_authors[int(index)].scopusId != "":
        list_scop = scopus_pub(final_authors[int(index)].scopusId)[1]

    if final_authors[int(index)].iexpId != "":
        list_iexp = iexp_pub(final_authors[int(index)].iexpId)
    r3 = [None]
    scholar_author(final_authors[int(index)].surname, final_authors[int(index)].name, r3, 0)
    if r3[0] !=[]:
        list_scholar = scholar_pub(r3[0][0].scholarUrl)

    publicationsSet = set()
    for i in range(len(list_scop)):
        publicationsSet.add(list_scop[i])
    for i in range(len(list_scholar)):
        publicationsSet.add(list_scholar[i])
    for i in range(len(list_iexp)):
        publicationsSet.add(list_iexp[i])

    publicationsList = list(publicationsSet)

    resultp = [None]
    for i in range(len(publicationsList)):
        resultp.append(json.loads(publicationsList[i].toJSON()))
    author = [json.loads(final_authors[int(index)].toJSON())]
    result = [author, resultp]

    return Response(result, content_type='application/json')
