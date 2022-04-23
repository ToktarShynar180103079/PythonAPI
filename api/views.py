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
def getAuthors(request):  # authors filtration
    name = request.POST['name']
    lastname = request.POST['lastname']

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
    print(str(result[1]))

    hashmap = {}
    for j in range(len(result[0])):
        hashmap[result[0][j].name + result[0][j].surname] = result[0][j]
    for i in range(len(result[1])):
        if result[1][i].name + result[1][i].surname in hashmap:
            hashmap[result[1][i].name + result[1][i].surname].iexpId = result[1][i].iexpId
        else:
            hashmap[result[1][i].name + result[1][i].surname] = result[1][i]

    if result[2].name + result[2].surname in hashmap:
        hashmap[result[2].name + result[2].surname].scholarUrl = result[2].scholarUrl
    else:
        hashmap[result[2].name + result[2].surname] = result[2]

    authors = list(hashmap.values())
    with open("authors", "wb") as fp:
        pickle.dump(authors, fp)

    result = []
    for i in range(len(authors)):
        result.append(json.loads(authors[i].toJSON()))

    return Response(result, content_type='application/json')


@api_view(['POST'])
def getPublications(request):
    list_iexp = []
    list_scop = []
    list_scholar = []
    final_authors = []
    with open("authors", "rb") as fp:  # Unpickling
        final_authors = pickle.load(fp)

    print("final authors: " + str(final_authors))
    index = request.POST['index']
    if final_authors[int(index)].scopusId != "":
        list_scop = scopus_pub(final_authors[int(index)].scopusId)

    if final_authors[int(index)].iexpId != "":
        list_iexp = iexp_pub(final_authors[int(index)].iexpId)
    r3 = [None]
    r3 = scholar_author(final_authors[int(index)].surname, final_authors[int(index)].name, r3, 0)
    if r3 is not None:
        list_scholar = scholar_pub(r3[0].scholarUrl)

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

    return Response(resultp, content_type='application/json')
