import os
import datetime


class QE:
    def __init__(self, line, Classes):
        QEcols = {
            "QE": 0,
            "HELM": 1,
            "CREW": 2,
            "CLASS": 3,
            "SAILNO": 4,
            "PERSONAL": 5,
            "AGEGROUP": 6,
            "FLEET": 7,
        }
        fleets = ["G", "S"]
        ageGroups = ["J", "S", "M", "G"]
        self.QE = ""
        self.helm = ""
        self.crew = ""
        self.personal = 0
        self.PY = 0
        self.dinghy = ""
        self.sailno = ""
        self.fleet = ""
        self.ageGroup = ""
        self.message = ""
        self.type = ""
        self.classNames = Classes.keys()
        line = line.replace("\r", "")
        line = line.replace("\n", "")
        tokens = line.split(",")
        if len(tokens) == len(QEcols):
            if tokens[3] in Classes.keys():
                if tokens[QEcols["AGEGROUP"]] in ageGroups:
                    if tokens[QEcols["FLEET"]] in fleets:
                        try:
                            self.personal = int(tokens[QEcols["PERSONAL"]])
                        except:
                            self.personal = 0
                        self.QE = tokens[QEcols["QE"]]
                        self.helm = tokens[QEcols["HELM"]]
                        self.crew = tokens[QEcols["CREW"]]
                        self.dinghy = tokens[QEcols["CLASS"]]
                        self.PY = Classes[tokens[QEcols["CLASS"]]]
                        self.sailno = tokens[QEcols["SAILNO"]]
                        self.ageGroup = tokens[QEcols["AGEGROUP"]]
                        self.fleet = tokens[QEcols["FLEET"]]
                    else:
                        self.message = (
                            "ERROR: "
                            + line
                            + " unknown fleet "
                            + tokens[QEcols["FLEET"]]
                        )
                else:
                    self.message = "ERROR: " + line + " unknown age group"
            else:
                self.message = "ERROR: " + line + "unknown class"
        elif len(tokens) != 1:
            self.message = "ERROR: line should have 7 tokens QE,HELM,CREW,CLASS,SAILNO,PERSONAL,AGERGROUP, Contains"
        # print(self.QE,self.helm,self.crew,self.dinghy,self.sailno,self.personal,self.ageGroup,self.fleet)
