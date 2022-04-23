import json
import json_fix


class Author:

    def __init__(self, name="", surname="",
                 orcidId="", scopusId="",
                 docCount="", affilation="",
                 country="", area="", iexpId="", scholarUrl=""):
        self.name = name
        self.surname = surname
        self.orcidId = orcidId
        self.scopusId = scopusId
        self.docCount = docCount
        self.affilation = affilation
        self.country = country
        self.area = area
        self.iexpId = iexpId
        self.scholarUrl = scholarUrl

    def __str__(self):
        return "Name " + self.name + " Surname " + self.surname + " OrcidId " + self.orcidId

    def __hash__(self):
        return self.name.__hash__() + self.surname.__hash__() + "Yernar".__hash__()

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)