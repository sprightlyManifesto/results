import os
import datetime
import json

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
        self.PY = py
        self.laps = laps
        self.time = time

    def audit(self,avg):
        return int(self.corrected / avg * 1000)


QES = []
Classes = []
PYs = dict()
Rigs = dict()
Types = dict()
Crews = dict()
Kites = dict()

fleets = ["G", "S"]
ageGroups = ["J", "S", "M", "G"]
PYcols = {'CLASS': 0, 'PY': 1,'TYPE': 2, 'RIG': 3, 'CREW': 4, 'KITE': 5}
QEcols = {'QE': 0, 'HELM': 1, 'CREW': 2, 'CLASS': 3, 'SAILNO': 4, 'PERSONAL': 5, 'AGEGROUP': 6, 'FLEET': 7}
raceEntryCols = {'QE': 0, 'HELM': 1, 'CREW': 2, 'CLASS': 3, 'SAILNO': 4, 'TIME': 5, 'LAPS': 6, 'FINCODE': 7, 'what':8}

for line in open(handicaps, "r").readlines():
    tokens = line.split(",")
    if tokens[0] != "":
        Classes.append(tokens[PYcols['CLASS']])
        PYs[tokens[PYcols['CLASS']]] = (int(tokens[PYcols['PY']]))
        Rigs[tokens[PYcols['CLASS']]] = tokens[PYcols['RIG']]
        Types[tokens[PYcols['CLASS']]] = tokens[PYcols['TYPE']]
        Crews[tokens[PYcols['CLASS']]] = tokens[PYcols['CREW']]
        Kites[tokens[PYcols['CLASS']]] = tokens[PYcols['KITE']]

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
            print("ERROR:", line, "unknown class")


   elif len(tokens) != 1:
       print("ERROR:", line, "\n should have 7 tokens QE,HELM,CREW,CLASS,SAILNO,PERSONAL,AGERGROUP, Contains:", len(tokens))


XMLfile = open("return.xml","w")

xmlHeader = '''                        
<RYAPY>
<admin>
  <source>return.py</source>
  <sourcever>1</sourcever>
  <xmlver>1.3</xmlver>
  <submittedon>2018-03-27</submittedon>
  <submittedat>22:35</submittedat>
</admin>
<event>
  <clubid>8101226</clubid>
  <clubname>Stewartby Sailing Club</clubname>
  <eventid>2018</eventid>
  <eventname>2018</eventname>
</event>
<races>'''

XMLfile.write(xmlHeader)

files = os.listdir()
i = 1
for f in files:
    if f[-5:] == ".race":
        race = Race()
        #print(f)
        lines = open(f,"r").readlines()
        date = f.split(" ")[2]
        
        i +=1


        for line in lines[1:]:
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
        if len(race.entries) > 3:
            raceXML = '\n<race>\n<date>' + date + '</date>\n<raceno>' + str(i) + '</raceno>\n<starts>\n<start> \
                                    \n <name>Start 1</name>\n\
                                    <windspeed-units>knots</windspeed-units>\n\
                                    <windspeed></windspeed>\n\
                                    <winddir-units>degrees</winddir-units>\n\
                                    <winddir></winddir>\n\
                                    <starttime-format>hh:mm:ss</starttime-format>\n\
                                    <starttime></starttime>\n\
                                    <entries>\n'
            for e in race.entries:
                for qe in QES:
                    if qe[0] == e.QE:
                        c = qe[3][raceEntryCols['CLASS']]
                        raceXML += '\n<entry>\n<classid>' + c + '</classid>\n\
                        <persons>' + Crews[c] + '</persons>\n\
                        <category>' + Types[c] + '</category>\n\
                        <rig>' + Rigs[c] + '</rig>\n\
                        <spinnaker>' + Kites[c].strip() + '</spinnaker>\n<engine></engine>\n \
        <keel></keel>\n<scheme>RYA-PYS</scheme>\n<sailno></sailno>\n\
        <helmid>' + qe[3][raceEntryCols['HELM']] + '</helmid>\n<crewid1></crewid1>\n\
        <rating>' + str(e.PY) + '</rating>\n<elapsed-units>seconds</elapsed-units>\n\
        <elapsed>' + str(e.time) + '</elapsed>\n<corrected-units>seconds</corrected-units>\n\
        <corrected></corrected>\n\
        <laps>' + str(e.laps) + '</laps>\n<rank></rank>\n</entry>\n'

            raceXML += '</entries>\n</start>\n</starts>\n</race>'
            XMLfile.write(raceXML)
            print(raceXML)

footer = '\n</races>\n</RYAPY>'
XMLfile.write(footer)
XMLfile.close()
