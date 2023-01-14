import sys
import os
import csv
import re
import json
from os import path
from collections import namedtuple
from QE import QE
from race import Race
from entry import Entry as raceEntry
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QEvent
from datetime import datetime
from pathlib import Path


class tempQE:
    def __init__(self, code, helm, crew, py, dinghy):
        self.QE = code
        self.helm = helm
        self.crew = crew
        self.personal = 0
        self.PY = py
        self.dinghy = dinghy
        self.sailno = ""
        self.fleet = "S"
        self.ageGroup = "S"
        self.message = ""


class MyLineEdit(QLineEdit):
    def __init__(self, *args):
        QLineEdit.__init__(self, *args)
        self.onFocusGainedText = ""

    def event(self, event):
        if (event.type() == QEvent.KeyPress) and (event.key() == QtCore.Qt.Key_Right):
            if self.text() == self.onFocusGainedText:
                parent.fooRight()
            print(">", self.onFocusGainedText, self.text())
            return True
        elif (event.type() == QEvent.KeyPress) and (event.key() == QtCore.Qt.Key_Left):
            if self.text() == self.onFocusGainedText:
                parent.fooLeft()
            print("<", self.onFocusGainedText, self.text())
            return True
        elif (
            (event.type() == QEvent.KeyPress)
            and (event.key() == QtCore.Qt.Key_Up)
            and self.text == self.onFocusGainedText
        ):
            parent.fooUp()
            return True
        elif (
            (event.type() == QEvent.KeyPress)
            and (event.key() == QtCore.Qt.Key_Down)
            and self.text == self.onFocusGainedText
        ):
            parent.fooDown()
            return True

        return QLineEdit.event(self, event)


class MyTable(QTableWidget):
    def __init__(self, r, headings, filename):
        super().__init__(r, len(headings))
        self.onFocusGainedText = ""
        self.headings = headings
        self.setColumnWidth(0, 70)
        self.setColumnWidth(1, 200)
        self.setColumnWidth(2, 200)
        self.setColumnWidth(3, 200)
        self.setColumnWidth(4, 70)
        self.setColumnWidth(5, 70)
        self.setColumnWidth(6, 70)
        self.setHorizontalHeaderLabels(headings)
        self.check_change = True
        self.cellChanged.connect(self.c_current)
        handicapsFile, QEsFile, self.browserPath = json.loads(
            open("config.json", "r").read()
        )
        self.filename = filename
        handicaps = []
        self.PYdict = {}
        self.dinghyLst = []
        self.cols = dict()
        for h in headings:
            self.cols[h] = []

        for line in open(handicapsFile, "r").readlines():
            tokens = line.split(",")
            if tokens[0] != "" and len(tokens) > 3:
                self.dinghyLst.append(tokens[0])
                handicaps.append(tokens[0] + "," + tokens[1] + "," + tokens[2])
                self.PYdict[tokens[0]] = int(tokens[1])

        QEs = []

        for line in open(QEsFile, "r").readlines():
            QEs.append(QE(line, self.PYdict))
        self.race = Race([], QEs)
        self.race.handicaps = handicaps
        self.completerLsts = {"QE": [], "Class": [], "Code": []}
        for qe in QEs:
            self.completerLsts["QE"].append(qe.QE)
        for c in self.PYdict.keys():
            self.completerLsts["Class"].append(c)
        self.completerLsts["Code"] = ["DNF", "OCS", "DNC"]
        self.completers = dict()
        for k in self.completerLsts.keys():
            self.completers[k] = QCompleter(self.completerLsts[k])
            self.completers[k].setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        people = set()

        for Q in QEs:
            people.add(Q.helm)
            people.add(Q.crew)
        self.peopleLst = list(people)
        self.show()

    def getCurrentCell(self):
        return self.cols[self.headings[self.currentColumn()]][self.currentRow()]

    def selectCell(self, row, col):
        if row >= 0 and row < self.rowCount() and col >= 0 and col < self.columnCount():
            self.cols[self.headings[col]][row - 1].setFocus()
            self.cols[self.headings[col]][row].onFocusGainedText = self.cols[
                self.headings[col]
            ][row].text()

    def fooEnter(self):
        cell = self.getCurrentCell()
        print("Enter")
        cell.onFocusGainedText = cell.text()

    def fooUp(self):
        self.selectCell(self.currentRow() - 1, self.currentColumn())

    def fooDown(self):
        self.selectCell(self.currentRow() + 1, self.currentColumn())

    def fooLeft(self):
        self.selectCell(self.currentRow(), self.currentColumn() - 1)

    def fooRight(self):
        self.selectCell(self.currentRow(), self.currentColumn() + 1)

    def score(self):
        ZZ = 0
        self.race.entries = []
        for r in range(0, self.rowCount()):
            QEfound = False
            helm = self.cols["Helm"][r].text()
            crew = self.cols["Crew"][r].text()
            dinghy = self.cols["Class"][r].text().upper()
            try:
                laps = int(self.cols["Laps"][r].text())
                time = int(self.cols["Time"][r].text())
            except:
                laps = 0
                time = 0
            fincode = self.cols["Code"][r].text()
            if ((fincode != "") or (laps != 0 and time != 0)) and (
                dinghy in self.dinghyLst
            ):
                for Q in self.race.QEs:
                    if (Q.helm.upper() == helm.upper()) and (
                        Q.dinghy.upper() == dinghy
                    ):
                        QEfound = True
                        qe = Q
                if QEfound == False:
                    print("ZZ: ", helm, dinghy)
                    py = 9999
                    if dinghy.upper() in self.PYdict.keys():
                        py = self.PYdict[dinghy]
                    else:
                        print("PY not found")
                    qe = tempQE("ZZ" + str(ZZ), helm, crew, py, dinghy)
                    ZZ += 1
                    self.race.QEs.append(qe)
                    print(qe, laps, time, fincode, 0)
                self.race.entries.append(raceEntry(qe, laps, time, fincode, 0))
        raceFileName = self.filename
        if not raceFileName.endswith(".race"):
            self.race.save(self.filename + ".race")
        else:
            self.race.save(self.filename)
        self.race.score(len(self.race.entries) + 1)
        html = (
            """<html> 
        <head><style>
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
				}
                </style></head>"""
            + self.race.PYresult()
            + self.race.personalResult()
            + "</html>"
        )
        htmlFileName = Path(self.filename).name.replace(" ","_")
        if htmlFileName.endswith(".race"):
            htmlFileName = htmlFileName[:-5] 
        htmlFileName += ".html"
        open(htmlFileName, "w").write(html)
        os.system(self.browserPath + " " + os.getcwd() + "/" + htmlFileName)
        

    def c_current(self):
        row = self.currentRow()
        col = self.currentColumn()
        h = self.headings

        value = self.cols[self.headings[col]][row].text()
        if self.headings[col] == "QE":
            for qe in self.race.QEs:
                if qe.QE == value.upper():
                    print(self.cols["QE"])
                    self.cols["QE"][row].setText(qe.QE)
                    self.cols["Helm"][row].setText(qe.helm)
                    self.cols["Crew"][row].setText(qe.crew)
                    self.cols["Class"][row].setText(qe.dinghy)
        elif self.headings[col] == "Class" or self.headings[col] == "Helm":
            self.cols["QE"][row].setText("")

    def addItem(self):
        h = self.headings
        row = self.rowCount()
        self.insertRow(row)
        for i in range(0, len(h)):
            le = MyLineEdit()
            le.returnPressed.connect(self.fooEnter)
            self.cols[h[i]].append(le)
            if h[i] in self.completers.keys():
                self.cols[h[i]][-1].setCompleter(self.completers[h[i]])
            self.setCellWidget(row, i, self.cols[h[i]][-1])
            self.cols[h[i]][-1].textChanged.connect(self.c_current)

    def open_sheet(self):
        row = 0
        endOfEntrys = False
        self.check_change = False
        path = QFileDialog.getOpenFileName(
            self, "Open race", os.getcwd(), "RACE(*.race)"
        )
        if path[0] != "":
            self.filename = path[0]
            print(self,self.parent())
            self.parent().setWindowTitle(self.filename)
            with open(path[0], newline="") as csv_file:
                #self.setRowCount(0)
                #self.setColumnCount(10)
                my_file = csv.reader(csv_file, delimiter=",", quotechar="|")
                skip = True
                for row_data in my_file:
                    if skip:
                        skip = False
                    else:
                        if "<HANDICAPS>" in row_data[0]: 
                            endOfEntrys = True
                            print("end of race entries")
                        #row = self.rowCount()
                        #self.insertRow(row)
                        if len(row_data) > 7 and (not endOfEntrys):
                            #self.setColumnCount(len(row_data))
                            #for column, stuff in enumerate(row_data):
                            #    item = QTableWidgetItem(stuff)
                            #    self.setItem(row, column, item)
                            print("row_data",row_data)
                            print('len(self.cols)',len(self.cols))
                            print('len(self.cols["QE"])',len(self.cols["QE"]))
                            self.cols["QE"][row].setText(row_data[0])
                            self.cols["Helm"][row].setText(row_data[1])
                            self.cols["Crew"][row].setText(row_data[2])
                            self.cols["Class"][row].setText(row_data[3])
                            self.cols["Time"][row].setText(row_data[5])
                            self.cols["Laps"][row].setText(row_data[6])
                            self.cols["Code"][row].setText(row_data[7])
                            row +=1
        self.check_change = True


class Sheet(QMainWindow):
    def __init__(self, fileName):
        super().__init__()
        headings = ["QE", "Helm", "Crew", "Class", "Time", "Laps", "Code"]
        self.form_widget = MyTable(0, headings, fileName)
        self.setCentralWidget(self.form_widget)
        for i in range(0, 50):
            self.form_widget.addItem()
        scoreAct = QAction("&Score", self)
        scoreAct.triggered.connect(self.form_widget.score)
        openAct = QAction("&Re Open Exisiting File", self)
        openAct.triggered.connect(self.form_widget.open_sheet)
        exitAct = QAction("&Exit", self)
        exitAct.setShortcut("Ctrl+Q")
        exitAct.setStatusTip("Exit application")
        exitAct.triggered.connect(qApp.quit)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        AdminMenu = menubar.addMenu("&Admin")
        fileMenu.addAction(scoreAct)
        AdminMenu.addAction(openAct)
        self.setGeometry(100, 100, 940, 600)
        self.setWindowTitle("Results Sheet")
        self.fn = fileNameCreator(self)
        self.fn.show()
        self.show()
        self.hide()


class fileNameCreator(QMainWindow):
    def __init__(self, parnt):
        super().__init__()
        self.fileName = ""
        self.setGeometry(200, 200, 300, 180)
        self.setWindowTitle("Results")
        self.parnt = parnt

        self.Series = QLineEdit(self)
        self.Race = QLineEdit(self)
        self.Date = QLineEdit(self)
        self.RO = QLineEdit(self)
        self.Date.setText(datetime.now().strftime("%d-%m-%Y"))

        seriesL = QLabel("Series:", self)
        raceL = QLabel("  Race:", self)
        dateL = QLabel("  Date:", self)
        ROL = QLabel("    RO:", self)
        qbtn = QPushButton("Create", self)

        self.Series.setFixedWidth(220)
        self.Race.setFixedWidth(220)
        self.Date.setFixedWidth(220)
        self.RO.setFixedWidth(220)
        qbtn.setFixedSize(280, 30)
        seriesL.move(10, 10)
        raceL.move(10, 40)
        dateL.move(10, 70)
        ROL.move(10, 100)
        self.Series.move(70, 10)
        self.Race.move(70, 40)
        self.Date.move(70, 70)
        self.RO.move(70, 100)
        qbtn.move(10, 140)
        qbtn.pressed.connect(self.buttonPress)

    def buttonPress(self):
        if self.RO.text() != "" and self.Series.text() != "" and self.Race.text() != "":
            fileName = (
                self.Series.text()
                + "_"
                + self.Race.text()
                + "_"
                + self.RO.text()
                + "_"
                + self.Date.text()
            )
            re.sub("[^-a-zA-Z0-9_. ]", "", fileName)
            print("sheet")
            self.parnt.form_widget.filename = fileName
            self.parnt.fileName = fileName
            self.parnt.setWindowTitle(fileName)
            self.parnt.show()
            self.close()


class top:
    def __init__(self):
        app = QApplication(sys.argv)
        sheet = Sheet("test")
        app.exec_()


t = top()
