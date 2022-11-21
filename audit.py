import os
import datetime

handicaps,QEfile = json.loads(open("config.json","r").read())

class Race:
    def __init__(self):
        self.entries = []

    def datum(self):
        avg = 0
        datum = 0
        for e in self.entries:
            avg += e.corrected
        avg /= len(self.entries)
        cutoff = 1.05*avg
        valid = 0
        for e in self.entries:
            if e.corrected < cutoff:
                valid += 1
                datum += e.corrected
        datum = datum/valid
        return datum

class Entry:
    def __init__(self,qe,py,laps,time):
        self.corrected = time*1000/laps/py
        self.QE = qe

    def audit(self,avg):
        return int(self.corrected / avg * 1000)

PYcols = {'CLASS': 0, 'PY': 1,'TYPE': 2, 'RIG': 3, 'CREW': 4, 'KITE': 5}
QEcols = {'QE': 0, 'HELM': 1, 'CREW': 2, 'CLASS': 3, 'SAILNO': 4, 'PERSONAL': 5, 'AGEGROUP': 6, 'FLEET': 7}
raceEntryCols = {'QE': 0, 'HELM': 1, 'CREW': 2, 'CLASS': 3, 'SAILNO': 4, 'TIME': 5, 'LAPS': 6, 'FINCODE': 7, 'what':8}

QES = []
Classes = []
PYs = dict()

fleets = ["G", "S"]
ageGroups = ["J", "S", "M", "G"]

for line in open(handicaps, "r").readlines():
    tokens = line.split(",")
    if tokens[0] != "":
        Classes.append(tokens[PYcols['CLASS']])
        PYs[tokens[PYcols['CLASS']]] = (int(tokens[PYcols['PY']]))
#parses and verify QES
for line in open(QEfile, "r").readlines():
   line = line.replace('\r', '')
   line = line.replace('\n', '')
   tokens = line.split(",")

   if len(tokens) == len(QEcols):
        if tokens[QEcols['CLASS']] in Classes:
            if tokens[QEcols['AGEGROUP']] in ageGroups:
                if tokens[QEcols['FLEET']] in fleets:
                    try:
                        int(tokens[QEcols['PERSONAL']])
                        QES.append([tokens[QEcols['QE']],
                                    int(tokens[QEcols['PERSONAL']]),
                                    [],
                                    tokens])
                    except:
                        print("ERROR:", line, "personal is not a number", tokens[QEcols['PERSONAL']])
                else:
                    print("ERROR:" , line, "unknown fleet", "'" + tokens[QEcols['FLEET']] + "'")
            else:
                print("ERROR:", line, "unknown age group")
        else:
            print("ERROR:", line, "unknown class", tokens[QEcols['CLASS']])


   elif len(tokens) != 1:
       print("ERROR:", line, "\n should have 7 tokens QE,HELM,CREW,CLASS,SAILNO,PERSONAL,AGERGROUP, Contains:", len(tokens))



files = os.listdir()
for f in files:
    if f[-5:] == ".race":
        race = Race()
        #print(f)
        for line in open(f,"r").readlines()[1:]:
            line = line.replace("\r", "")
            line = line.replace("\n", "")
            if line == "<HANDICAPS>":
                break
            else:
                tokens = line.split(",")
                if len(tokens) == len(raceEntryCols):
                    qe = tokens[raceEntryCols['QE']]
                    valid = False
                    for QE in QES:
                        if qe == QE[0]:
                            valid = True

                    if valid & (tokens[raceEntryCols['FINCODE']] == ""):
                        try:
                            py = int(PYs[tokens[raceEntryCols['CLASS']]])
                            laps = int(tokens[raceEntryCols['LAPS']])
                            time = int(tokens[raceEntryCols['TIME']])
                            race.entries.append(Entry(qe, py, laps, time))
                        except:
                            print("WARNING:", line, "in file: ", f, "PY, LAPS & TIME must all be integers")
                else:
                    if not (",,,,,,," in line):
                        print("WARNING:", line, "in file: ", f, "unknown QE")
        if len(race.entries) > 1:
            datum = race.datum()
            for e in race.entries:
                for qe in QES:
                    if qe[0] == e.QE:
                        qe[2].append(e.audit(datum))



html = '''<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" type="text/css" href="http://stewartby-watersports.org.uk/sailing/css/styles.css">
<script src="http://stewartby-watersports.org.uk/sailing/scripts.js"></script>
<img src=http://stewartby-watersports.org.uk/sailing/images/logo.jpg class="center">
<style>
th, td {border: 1px solid black;}
table tr:nth-child(odd) td{background-color: #f2f2f2;}
th, td {padding: 5px;text-align: left;}
</style>

</head>

<div w3-include-html="menu.html"></div>

<script>includeHTML();</script>

<p>How personal handicaps are calculated: </p>
<p>For each race in a rolling years worth of races (including Wednesday evenings but not short course) all the Portsmouth Yardstick corrected times are averaged and multiplied by 1.05
to give a cut off time any times greater than this value are discarded, because they are most likely the result of someone having a really bad race so is not representative and will unduly influence the handicaps.
</p>

Sample race:

<table><tr><th>Competitor</th><th>Corrected Time (s)</th></tr>
<tr><td>Ade</td><td>3000</td></tr>
<tr><td>Bob</td><td>3100</td></tr>
<tr><td>Carl</td><td>3200</td></tr>
<tr><td>Drew</td><td>3300</td></tr>
<tr><td>Earl</td><td>4000</td></tr>
</table>

<p>so for our sample race the calculated cut off is (3000+3100+3200+3300+4000)*1.05/5 = 3320</p>
<p>we then calculate the average for all results under the threshold:</p>
<p>"Race Average" = (3000+3100*3200+3300) = 3150 </p>
<p>each competitors score is then audited against this number by (competiors corrected time / Race Average) * 1000 rounded to the nearest whole number</p>
<p>so for our sample race:</p>

<table><tr><th>Competitor</th><th>Audit</th></tr>
<tr><td>Ade</td><td>3000/3150*1000 = 952</td></tr>
<tr><td>Bob</td><td>3100/3150*1000 = 984</td></tr>
<tr><td>Carl</td><td>3200/3150*1000 = 1016</td></tr>
<tr><td>Drew</td><td>3300/3150*1000 = 1048</td></tr>
<tr><td>Earl</td><td>4000/3150*1000 = 1269</td></tr>
</table>

<p>For each competitor the average of all there Audits is taken to determine their personal number,  any audits greater than 1500 are not included in the average,  to discard particularly bad races where a competitor has lost a lap due to being OCS  or capsized a lot!</p>
<p>To use the personal handicap the formular is:</p>
<p>Personal correct time = PY corrected time / Personal handicap * 1000</p>

<p>Current personal handcap list ('''

html += str(datetime.date.today())

html += ''')</p>
note a personal number of 0 doesn't mean your infinately fast it just means i don't have any data for you yet
'''

html += "<table><tr><th>QE</th><th>Sailor</th><th>Class</th><th>Personal Handicap</th><th>No Races</th></tr>\n"
csv = ""

for qe in QES:
    newPersonal = 0
    if len(qe[2]) > 0:
        for e in qe[2]:
            if e < 1500:
                newPersonal += e
            else:
                newPersonal += 1500
        newPersonal = int(newPersonal / len(qe[2]))
    if newPersonal == 0:
        newPersonal = qe[1]
    print(qe[0], newPersonal, len(qe[2]))
    html += "<tr><td>" + qe[0] + "</td><td>"  + qe[3][QEcols['HELM']] + "</td><td>" \
    + qe[3][QEcols['CLASS']] + "</td><td>" + str(newPersonal) \
    + "</td><td>" + str(len(qe[2])) + "</td></tr>\n"
    csv += qe[0] + "," + qe[3][1] + "," + qe[3][2] + "," + qe[3][3] + "," + qe[3][4] +\
           "," + str(newPersonal) + "," + qe[3][6] + "," + qe[3][7] +"\n"

html += "</table></html>\n"

open("audit.csv","w").write(csv)
open("personalHandicaps.html", "w").write(html)
