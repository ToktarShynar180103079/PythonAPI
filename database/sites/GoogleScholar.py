import requests
from bs4 import BeautifulSoup
import csv  # Google scholar parsing code

from database.models.Publication import Publication
from database.models.Author import Author


def get_html(url, params=None, data=None):
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "accept": "text/html, */*"}
    r = requests.get(url, headers=HEADERS, params=params, data=data)
    return r


def scholar_author(lastname, name, result, index):
    URL = "https://scholar.google.com/scholar?hl=ru&as_sdt=0%2C5&q=" + lastname + "+" + name
    html = get_html(URL)
    if html.status_code == 200:
        soup = BeautifulSoup(html.text, "html.parser")
        items = soup.find_all("h4", class_="gs_rt2")
        if items == []:
            result[index] = []
        else:
            html1 = items[0].find("a", class_=None).get("href")
            name = (items[0].find("a", class_=None).get_text()).split()[0]
            lastname = (items[0].find("a", class_=None).get_text()).split()[1]
            result[index] = [Author(
                index=0,
                name=name,
                surname=lastname,
                scholarUrl='https://scholar.google.com/' + html1)]
    else:
        result[index] =  []


def item_for(items):
    publications = []
    for item in items:
        publication = Publication(
            site="Google Scholar",
            title = item.find("a", class_="gsc_a_at").get_text(),
            link = 'https://scholar.google.com/' + item.find("a", class_="gsc_a_at").get("href"),
            authors = item.find("div", class_="gs_gray").get_text(),
            wherePublished = item.find("div", class_="gs_gray").find_next("div").get_text().rsplit(',', 2)[0],
            year = item.find("span", class_="gsc_a_h gsc_a_hc gs_ibl").get_text()
            )
        if len(item.find("div", class_="gs_gray").find_next("div").get_text().rsplit(',', 2)) > 1:
            pages = item.find("div", class_="gs_gray").find_next("div").get_text().rsplit(',', 2)[1]
            if pages != "":
                if pages[1:5] != item.find("span", class_="gsc_a_h gsc_a_hc gs_ibl").get_text() and pages[1] in ['0','1','2',
                                                                                                                     '3','4','5',
                                                                                                                     '6','7','8','9']:
                    publication.PP = pages

        publications.append(publication)

    return publications

def scholar_pub(url):
    html1 = get_html(url)
    result = []
    #   1-20 publications
    if html1.status_code == 200:
        soup = BeautifulSoup(html1.text, "html.parser")
        items = soup.find_all("tr", class_="gsc_a_tr")
        result = result + item_for(items)
    # 21-100 publications
    html2 = get_html(url + '&cstart=20&pagesize=80')
    if html2.status_code == 200:
        soup = BeautifulSoup(html2.text, "html.parser")
        items = soup.find_all("tr", class_="gsc_a_tr")
        if len(items) > 1:
            result = result + item_for(items)
    # 101 - 200 publications
    html3 = get_html(url + '&cstart=100&pagesize=100')
    if html3.status_code == 200:
        soup = BeautifulSoup(html3.text, "html.parser")
        items = soup.find_all("tr", class_="gsc_a_tr")
        if len(items) > 1:
            result = result + item_for(items)
    # 201 - 300 publications
    html4 = get_html(url + '&cstart=200&pagesize=100')
    if html4.status_code == 200:
        soup = BeautifulSoup(html4.text, "html.parser")
        items = soup.find_all("tr", class_="gsc_a_tr")
        if len(items) > 1:
            result = result + item_for(items)

    return result

# authors = scholar_pub("https://scholar.google.com/citations?hl=ru&user=WQe0zyIAAAAJ")
#
# for i in range(len(authors)):
#     print(str(i) + authors[i].__str__())
