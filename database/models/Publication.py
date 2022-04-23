import json


class Publication:

    def __init__(self, site="", authors="",
                 title="", type="",
                 link="", year="",
                 wherePublished="", PP="",
                 volume="",
                 keyWords="", publisher=""):
        self.site = site
        self.authors = authors
        self.title = title
        self.type = type
        self.link = link
        self.year = year
        self.wherePublished = wherePublished
        self.PP = PP
        self.volume = volume
        self.keyWords = keyWords
        self.publisher = publisher

    def __str__(self):
        return "Site " + self.site + " Authors " + self.authors + " Title " + self.title + " Type " + self.type

    def __hash__(self):
        return self.title.__hash__() + self.year.__hash__() + self.wherePublished.__hash__()

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)