import os
import datetime
from entry import Entry
from QE import QE


class Race:
    def __init__(self, entries, QEs):
        self.entries = entries
        self.maxLaps = 0
        self.QEs = QEs
        self.f = ""
        self.handicaps = []

    def PYresult(self):
        results = "<table id='PY'><tr><th>QE</th><th>Helm/<br>Crew</th><th>Class</th><th>PY</th>\
<th>Laps</th><th>Time</th><th>Corrected</th><th>Rank</th></tr>"
        self.entries.sort(key=lambda x: x.PYplace, reverse=False)
        self.entries
        for e in self.entries:
            results += e.PYline() + "\n"
        results += "</table>"
        return results

    def summary(self):
        results = self.f + "\n"
        self.entries.sort(key=lambda x: x.PYplace, reverse=False)
        results += "QE   Helm                Class     Time  Laps  Corrected Place\n"
        for e in self.entries:
            results += (
                str(e.QE.QE).ljust(5, " ")
                + str(e.QE.helm).ljust(20, " ")
                + str(e.QE.dinghy).ljust(10, " ")
                + str(e.time).ljust(6, " ")
                + str(e.laps).ljust(6, " ")
                + str(e.correctedPY).ljust(10, " ")
                + str(e.PYplace)
                + "\n"
            )
        return results

    def personalResult(self):
        results = "<table id ='personal'><tr><th>Helm/<br>Crew</th><th>Personal<br>Handicap\
</th><th>Corrected</th><th>Rank</th></tr>"
        self.entries.sort(key=lambda x: x.personalPlace, reverse=False)
        for e in self.entries:
            results += e.PersonalLine() + "\n"
        results += "</table>"
        return results

    def score(self, dnc):

        self.maxLaps = 0
        for e in self.entries:
            if e.laps > self.maxLaps:
                self.maxLaps = e.laps

        for e in self.entries:
            e.maxlaps = self.maxLaps
            e.calCorrected()

        scored = 0
        for e in self.entries:
            if e.finCode != "":
                e.PYplace = dnc
                e.personalPlace = dnc
                scored += 1

        place = 1
        while scored < len(self.entries):
            last = scored
            inplace = 0
            t = 9999
            for e in self.entries:
                if e.PYplace == 0 and e.correctedPY < t:
                    t = e.correctedPY
            for e in self.entries:
                if e.correctedPY == t:
                    inplace += 1
            for e in self.entries:
                if e.correctedPY == t:
                    e.PYplace = float((place * inplace + inplace - 1)) / inplace
                    scored += 1
            place += inplace
            if scored == last:
                print("ERROR: PY scoring in :", self.f)
                break

        place = 1
        scored = 0
        for e in self.entries:
            if e.QE.personal == 0:
                e.personalPlace = dnc

        while scored < len(self.entries):
            last = scored
            t = 9999
            inplace = 0
            for e in self.entries:
                if e.personalPlace == 0 and e.correctedPersonal < t:
                    t = e.correctedPersonal
            for e in self.entries:
                if e.correctedPersonal == t:
                    inplace += 1
            for e in self.entries:
                if e.correctedPersonal == t:
                    e.personalPlace = float((place * inplace + inplace - 1)) / inplace
                    scored += 1
            place += inplace
            if scored == last:
                # print("ERROR: personal scoring in:", self.f)
                break

    def datum(self):
        avg = 0
        datum = 0
        for e in self.entries:
            avg += e.corrected
        avg /= len(self.entries)
        cutoff = 1.05 * avg
        valid = 0
        for e in self.entries:
            if e.corrected < cutoff:
                valid += 1
                datum += e.corrected
        datum = datum / valid
        return datum

    def save(self, f):
        with open(f, "w") as out:
            out.write(f + "\n")
            for e in self.entries:
                out.write(
                    e.QE.QE
                    + ","
                    + e.QE.helm
                    + ","
                    + e.QE.crew
                    + ","
                    + e.QE.dinghy
                    + ","
                    + str(e.QE.sailno)
                    + ","
                    + str(e.time)
                    + ","
                    + str(e.laps)
                    + ","
                    + e.finCode
                    + ",\n"
                )
            out.write("<HANDICAPS>\n")
            for h in self.handicaps:
                out.write(h + "\n")
            out.write("<QES>\n")
            for qe in self.QEs:
                out.write(
                    qe.QE
                    + ","
                    + qe.helm
                    + ","
                    + qe.crew
                    + ","
                    + qe.dinghy
                    + ","
                    + str(qe.sailno)
                    + ","
                    + str(qe.personal)
                    + ","
                    + str(qe.ageGroup)
                    + ","
                    + str(qe.fleet)
                    + "\n"
                )

    def load(self, f):
        self.f = f[0:-5]
        QECODE = 0
        HELM = 1
        CREW = 2
        CLASS = 3
        SAILNO = 4
        TIME = 5
        LAPS = 6
        FINCODE = 7
        lines = open(f, "r").readlines()[1:]
        for line in lines:
            line = line.replace("\r", "")
            line = line.replace("\n", "")
            if line == "<HANDICAPS>":
                break
            else:
                try:
                    if self.maxLaps < int(line.split(",")[LAPS]):
                        self.maxLaps = int(line.split(",")[LAPS])
                except:
                    continue
        for line in lines:
            line = line.replace("\r", "")
            line = line.replace("\n", "")
            # print(line)
            if line == "<HANDICAPS>":
                break
            else:
                tokens = line.split(",")
                if len(tokens) == 9:
                    qe = tokens[QECODE]
                    valid = False
                    for QEcode in self.QEs:
                        if qe == QEcode.QE:
                            QuickE = QEcode
                            valid = True
                    if valid & (tokens[FINCODE] == ""):
                        try:
                            laps = int(tokens[LAPS])
                            time = int(tokens[TIME])
                            self.entries.append(
                                Entry(QuickE, laps, time, tokens[FINCODE], self.maxLaps)
                            )
                        except:
                            print(
                                "WARNING:",
                                line,
                                "in file: ",
                                f,
                                "PY, LAPS & TIME must all be integers",
                            )
                    elif valid:
                        self.entries.append(
                            Entry(QuickE, 0, 0, tokens[FINCODE], self.maxLaps)
                        )
                else:
                    if not (",,,,,,," in line):
                        print("WARNING:", line, "in file: ", f, "unknown QE")


# command line app to create and store a .race and output .html
if __name__ == "__main__":
    f = input("race:")
    QEsFile = r"2020_Feb_QE.txt"
    handicapsFile = r"2020.csv"
    handicaps = []
    PYs = dict()
    PYcols = {"CLASS": 0, "PY": 1, "TYPE": 2, "RIG": 3, "CREW": 4, "KITE": 5}
    for line in open(handicapsFile, "r").readlines():
        tokens = line.split(",")
        if tokens[0] != "":
            PYs[tokens[PYcols["CLASS"]]] = int(tokens[PYcols["PY"]])
        if len(tokens) > 3:
            handicaps.append(tokens[0] + "," + tokens[1] + "," + tokens[2])

    QEs = []
    for line in open(QEsFile, "r").readlines():
        QEs.append(QE(line, PYs))
    r = Race([], QEs)
    r.f = f
    r.handicaps = handicaps
    line = " "

    def summary(r):
        name = r.f
        r.save(name + ".race")
        r = Race([], QEs)
        r.load(name + ".race")
        r.score(len(r.entries) + 1)
        # os.system('cls' if os.name == 'nt' else 'clear')
        # print(r.summary())

    while line != "":
        line = input("")
        tokens = line.split(" ")
        # try:
        if len(tokens) == 1:
            if tokens[0].upper() == "HELP":
                print("Race program commands\n")
                print("LOAD xxxx.race (loads the race in file xxxx.race)")
                print("ADDQE ABL	  (adds a new QE code ABL)")
                print("LS			  (lists all entrys in the race)")
                print(
                    "CLASS          (lists all the boats matching the inputed class or part inputed class)"
                )
                print(
                    "SAIL           (lists all boats matching the sail number or part sail number)"
                )
                print("RM             (removes QE from race)")
                print("CLEAR          (clears the terminal)")
            elif tokens[0].upper() == "LOAD":
                val = input("Load: ")
                if os.path.isfile(val + ".race"):
                    r = Race([], QEs)
                    r.load(val + ".race")
                    summary(r)
                else:
                    print("File not found")
            elif tokens[0].upper() == "ADDQE":
                os.system("pluma " + QEsFile)
            elif tokens[0].upper() == "LS":
                summary(r)
            elif tokens[0].upper() == "RM":
                val = input("Remove: ")
                for e in r.entries:
                    if e.QE.QE == val.upper():
                        r.entries.remove(e)
                summary(r)
            elif tokens[0].upper() == "CLASS":
                os.system("cls" if os.name == "nt" else "clear")
                val = input("Class: ")
                for qe in r.QEs:
                    if val.upper() in qe.dinghy.upper():
                        continue
                        # print(qe.QE,qe.helm,qe.crew,qe.dinghy, qe.sailno)
            elif tokens[0].upper() == "SAIL":
                os.system("cls" if os.name == "nt" else "clear")
                val = input("Sail No: ")
                for qe in r.QEs:
                    if val.upper() in qe.sailno.upper():
                        continue
                        # print(qe.QE,qe.helm,qe.crew,qe.dinghy, qe.sailno)
            elif tokens[0].upper() == "CLEAR":
                os.system("cls" if os.name == "nt" else "clear")
            else:
                if tokens[0] != "":
                    print("command unknown")
        if len(tokens) > 2:
            try:
                laps = int(tokens[2])
                time = int(tokens[1])
                if len(tokens) == 4:
                    fincode = tokens[3]
                else:
                    fincode = ""
                    QE = next((x for x in r.QEs if x.QE == tokens[0].upper()), None)
                    if QE != None:
                        r.entries.append(Entry(QE, laps, time, fincode, 0))
                        summary(r)
            except:
                print("Command Invalid")
    r.score(len(r.entries) + 1)
    with open(r.f + ".html", "w") as html:
        html.write("<html>\n")
        html.write(
            """<head><style>
				th{
				font-size: 12px;
				border: 1px solid black;							
				text-align: center;
				padding: 2px;}
				table {border-collapse: collapse;}				
				table#PY tr:nth-child(odd) td{background-color: #f2f2f2;}
				table#personal tr:nth-child(even) td{background-color: #a2a2a2;}
				table#personal {float: left; }
				table#PY {float: left;}
				table#layout {width:100%}		
				td {
				text-align: center;
				font-size: 12px;
				border: 1px solid black;
				padding: 2px;
				}
				}</style></head> \n"""
        )
        html.write(r.PYresult() + "\n")
        html.write(r.personalResult() + "\n")
        html.write("</html>\n")
