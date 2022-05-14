import json

from pybliometrics.scopus import ScopusSearch
from pybliometrics.scopus import AuthorRetrieval
from pybliometrics.scopus import AuthorSearch
from pybliometrics.scopus.exception import Scopus401Error
from ..models.Author import *
from ..models.Publication import *


def scopus_author(lastname, name, result, index):
    res_aut_list = []
    try:
        s = AuthorSearch(f'AUTHLAST({lastname}) and AUTHFIRST({name})')
        res = s.authors
        for i in range(len(res)):
            author = Author(
                index = i,
                name = str(res[i][4].split()[0]),
                surname= str(res[i][2]),
                orcidId= str(res[i][1]),
                scopusId=res[i][0][7:],
                docCount=str(res[i][6]),
                affilation=str(res[i][5]),
                country= str(res[i][8])  + ', ' + str(res[i][9]),
                area=str(res[i][10])
            )
            res_aut_list.append(author)
    except:
        result[index] = res_aut_list

    result[index] = res_aut_list


def scopus_pub(scopusId):
    try:
        result = []
        au = AuthorRetrieval(scopusId)
        a = au.get_documents()
        for i in range(len(a)):
            publication = Publication(
                site="Scopus",
                authors=a[i][13],
                title=a[i][4],
                type=a[i][6],
                link=None,
                year=a[i][17],
                wherePublished=a[i][18],
                PP=a[i][26],
                volume=a[i][23],
                keyWords=a[i][28]
            )
            result.append(publication)
    except Scopus401Error:
        return result
    return result

# authors = scopus_author("Ba", "") # 3

# print(scopus_pub(55832104800))

# for i in range(len(list)):
#     print(list[i].__str__())
