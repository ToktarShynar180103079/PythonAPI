import requests
import json
import csv
from ..models.Author import *
from ..models.Publication import *


def iexp_author(lastname, name, result, index):
    url_base = 'https://ieeexplore.ieee.org'
    url = url_base + "/rest/search"

    payload = json.dumps({
        "newsearch": True,
        "queryText": lastname + " " + name,
        "highlight": True,
        "returnFacets": [
            "ALL"
        ],
        "returnType": "SEARCH",
        "matchPubs": True
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://ieeexplore.ieee.org',
        'Cookie': 'JSESSIONID=1f1uodkJQyFydS1nj60dhUga9TzcL1eSS2GtBmSb4I2UWoFyct4e!-1059566563; TS01b03060=012f3506239362e2457f97d2093c7ee2a7ae609257d4f289c6faeaf1e87e8b729d50e85168a48a955b71aa49179c7761b2b63e68b1; WLSESSION=203580044.20480.0000; ipCheck=46.34.147.74'
    }
    authors = []
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        out = json.loads(response.text)
        aut_id = []
        if out['endRecord'] != 0:
            for rec in out['records']:
                for au in rec['authors']:
                    if name in au['preferredName'] and lastname in au['preferredName'] and au['id'] not in aut_id:
                        author = Author(
                            index=len(aut_id),
                            iexpId=au['id'],
                            surname=str(au['lastName']),
                            name=str(au['firstName'].split()[0])
                        )
                        aut_id.append(au['id'])
                        authors.append(author)
        result[index] = authors
    except:
        result[index] = authors


def iexp_pub(auth_id):
    publications = []
    url_base = 'https://ieeexplore.ieee.org'
    url = url_base + "/rest/search"

    payload = json.dumps({
        "newsearch": True,
        "highlight": True,
        'history': 'no',
        "searchWithin": [
            f"\"Author Ids\":{auth_id}"
        ],
        "returnFacets": [
            "ALL"
        ],
        "returnType": "SEARCH",
        "sortType": 'newest'
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://ieeexplore.ieee.org',
        'Cookie': 'TS01b03060=012f35062340772011a882b0733f2bc949de2a36d5efd984d874bdbc3b7d6977f5d45d87053d2c9b1d38eed01035a37961c41c1a17; Path=/; Domain=.ieeexplore.ieee.org; Secure; HTTPOnly'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    out = json.loads(response.text)
    for rec in out['records']:

        aut = []
        for au in rec['authors']:
            aut.append(au['normalizedName'])

        publication = Publication(
            site="IEEEXplore",
            authors=','.join(aut),
            title=rec['highlightedTitle'],
            type=rec['articleContentType'],
            link=url_base + rec['htmlLink'],  # link
            year=rec['publicationYear'],  # year
            publisher=rec['publisher'],  # publisher
            wherePublished=rec['publicationTitle'],
            PP=rec['startPage'] + ' - ' + rec['endPage'],
            volume=rec['pdfSize']
        )
        publications.append(publication)
    return publications

# authors = iexp_author("Baimuratov", "A") # 3
#
# print(iexp_pub(37089228134)[0].link)

# for i in range(len(authors)):
#     print(authors[i].__str__())
