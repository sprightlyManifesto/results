import math
import os
import datetime
import copy
from race import Race
from entry import Entry
from QE import QE
from helm import Helm
from seriesEntry import SeriesEntry


class Series:
    def __init__(
        self, handicapsFile, QEfile, racesDirs, name, toCount=None, countAll=False
    ):
        self.toCount = toCount
        self.countAll = countAll
        self.name = name
        self.races = []
        self.PYs = dict()
        self.types = dict()
        PYcols = {"CLASS": 0, "PY": 1, "TYPE": 2, "RIG": 3, "CREW": 4, "KITE": 5}
        for line in open(handicapsFile, "r").readlines():
            tokens = line.split(",")
            if tokens[0] != "":
                self.PYs[tokens[PYcols["CLASS"]]] = int(tokens[PYcols["PY"]])
                self.types[tokens[PYcols["CLASS"]]] = tokens[PYcols["TYPE"]]

        # parses and verify QES create a list of all helms with their QEs collated.
        self.QEs = []
        ln = 0
        for line in open(QEfile, "r").readlines():
            ln += 1
            qe = QE(line, self.PYs)
            if qe.dinghy in self.types.keys():
                qe.type = self.types[qe.dinghy]
                self.QEs.append(qe)
            elif len(line.strip()) > 0:
                print(f"dinghy type not in handicaps file on LineNo: {ln}: {line}")

        # read race files
        files = []
        for racesDir in racesDirs:
            dirlist = os.listdir(racesDir)
            for f in dirlist:
                if f[-5:] == ".race":
                    files.append(os.path.join(racesDir, f))

        # sort them
        files.sort(key=lambda x: int(x.split(" ")[1]), reverse=False)  # race No
        files.sort(key=lambda x: x.split(" ")[0].upper(), reverse=False)  # AM/PM
        files.sort(
            key=lambda x: int(
                datetime.datetime.strptime(x.split(" ")[2], "%d-%m-%Y.race").timestamp()
            ),
            reverse=False,
        )

        # add them to the series
        for x in files:
            print(x)
            if x[-5:] == ".race":
                r = Race([], self.QEs)
                r.load(x)
                self.races.append(r)

    def filterByBoatType(self, f):
        singles = []
        doubles = []
        cats = []
        lasers = []
        for r in self.races:
            newEntriesList = []
            for e in r.entries:
                if e.QE.type == f:
                    newEntriesList.append(e)
                if f == "M" and e.QE.type != "C":
                    newEntriesList.append(e)
            r.entries = newEntriesList
        return self

    def filterByAge(self, f):
        for r in self.races:
            newEntriesList = []
            for e in r.entries:
                if e.QE.ageGroup == f:
                    newEntriesList.append(e)
            r.entries = newEntriesList
        return self

    def summary(self, silver, personal, outfile, score=True):
        headings = r"<tr><th>competitor(s)</th><th>Class(es)</th>"
        entries = dict()
        boats = []
        i = 1
        for r in self.races:
            headings += r"<th>" + str(i) + r"</th>"
            i += 1
            for e in r.entries:
                if e.QE.helm in entries.keys():
                    if not (e.QE.dinghy in entries[e.QE.helm].boats):
                        entries[e.QE.helm].boats.append(e.QE.dinghy)
                else:
                    entries[e.QE.helm] = SeriesEntry(e.QE.dinghy, e.QE.helm)
        headings += r"<th>Score</th></tr>"
        # score all races with dnc value calculated
        dnc = len(entries) + 1
        for r in self.races:
            r.score(dnc)

        for r in self.races:
            for se in entries.keys():
                result = dnc
                resultpersonal = dnc
                for e in r.entries:
                    if e.QE.helm == se:
                        result = e.PYplace
                        resultpersonal = e.personalPlace
                entries[se].resultsPY.append(result)
                entries[se].resultsPersonal.append(resultpersonal)
                # print(entries[se]scorePY ,entries[se].scorePersonal ,entries[se].name)

        with open(outfile, "w") as out:
            out.write(
                """<html><head><title>"""
                + self.name
                + """</title><style>
				th, td {border: 1px solid black;}
				table#PY tr:nth-child(odd) td{background-color: #f2f2f2;}
				table#personal tr:nth-child(even) td{background-color: #a2a2a2;}
				table#personal {float: left; width:40%}
				table#PY {float: right;width:60%}
				table#layout {width:100%} 
				th, td {
				padding: 5px;
				text-align: left;
				}</style></head>"""
            )
            if self.toCount == None:
                toCount = int(math.ceil(len(self.races) / 3) + 1)
                if toCount > len(self.races):
                    toCount = len(self.races)
            else:
                toCount = self.toCount
            if self.countAll:
                toCount = len(self.races)
            print("ToCount:", toCount)
            # PY overall result

            summary = ""
            if score:
                summary = f"Races to count:{toCount} from: {len(self.races)}"
                summary += "<p>PY Results</p><table>" + headings
                for se in entries.keys():
                    entries[se].scoreSeries(toCount, dnc)
                entries = list(entries.values())
                entries.sort(key=lambda x: x.scorePY, reverse=False)
                for se in entries:
                    summary += se.summary()
                summary += "</table>"

            # Personal overall result
            if personal:
                summary += "<p>Personal result</p><table>" + headings
                entries.sort(key=lambda x: x.scorePersonal, reverse=False)
                for se in entries:
                    summary += se.summaryPersonal()
                summary += "</table>"
            out.write(summary)

            for r in self.races:
                summary = ""
                pth, name = os.path.split(r.f)
                summary += (
                    "<table id=layout><tr><td>"
                    + name
                    + "</td></tr></table>"
                    + r.PYresult()
                    + r.personalResult()
                )
                out.write(summary)
            out.write("</html>")
        print("done")
