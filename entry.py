# import os
# import datetime


class Entry:
    def __init__(self, qe, laps, tm, finCode, maxlaps):
        self.QE = qe
        self.laps = laps
        self.time = tm
        self.finCode = finCode
        self.correctedPY = 0
        self.correctedPersonal = 0
        self.PYplace = 0
        self.personalPlace = 0
        self.maxlaps = maxlaps

    def PersonalLine(self):
        line = (
            "<tr><td>"
            + self.QE.helm
            + " "
            + self.QE.crew
            + "</td><td>"
            + str(self.QE.personal)
            + "</td><td>"
            + str(self.correctedPersonal)
            + "</td><td>"
            + str(self.personalPlace)
            + "</td></tr>"
        )
        return line

    def PYline(self):

        line = (
            "<tr><td>"
            + self.QE.QE
            + "</td><td>"
            + self.QE.helm
            + " "
            + self.QE.crew
            + "</td><td>"
            + self.QE.dinghy
            + "</td><td>"
            + str(self.QE.PY)
            + "</td><td>"
            + str(self.laps)
            + "</td><td>"
            + str(self.time)
            + "</td>"
        )
        if self.finCode != "":
            line += (
                "<td>" + self.finCode + "</td><td>" + str(self.PYplace) + "</td></tr>"
            )
        else:
            line += (
                "<td>"
                + str(self.correctedPY)
                + "</td><td>"
                + str(self.PYplace)
                + "</td></tr>"
            )
        return line

    def calCorrected(self):
        if self.finCode == "":
            # print(self.time,self.maxlaps,self.laps,self.QE.PY)
            self.correctedPY = int(
                self.time * self.maxlaps * 1000 / self.laps / self.QE.PY
            )
            if self.QE.personal > 0:
                self.correctedPersonal = int(self.correctedPY * 1000 / self.QE.personal)

    def audit(self, avg):
        return int(self.correctedPY / avg * 1000)
