import json

from pybliometrics.scopus import ScopusSearch
from pybliometrics.scopus import AuthorRetrieval
from pybliometrics.scopus import AuthorSearch
from pybliometrics.scopus.exception import Scopus401Error
from ..models.Author import *
from ..models.Publication import *


def scopus_author(lastname, name, result, index):
    s = AuthorSearch(f'AUTHLAST({lastname}) and AUTHFIRST({name})')
    res = s.authors
    res_aut_list = []
    try:
        for i in range(len(res)):
            author = Author(
                str(res[i][4].split()[0]),
                str(res[i][2]),
                str(res[i][1]),
                res[i][0][7:],
                str(res[i][6]),
                str(res[i][5]),
                str(res[i][9]) + ', ' + str(res[i][8]),
                str(res[i][10])
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
        return 'Error'
    return result

# authors = scopus_author("Ba", "") # 3

# print(scopus_pub(55832104800))

# for i in range(len(list)):
#     print(list[i].__str__())
