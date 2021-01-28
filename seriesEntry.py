class SeriesEntry:
    def __init__(self, boat, name):
        self.boats = []
        self.boats.append(boat)
        self.resultsPY = []
        self.resultsPersonal = []
        self.scorePY = 0
        self.scorePersonal = 0
        self.name = name
        self.dnc = 0

    def scoreSeries(self, tocount, dnc):
        #print(len(self.resultsPY))
        self.dnc = dnc
        
        rPY = self.resultsPY[:]
        rPY.sort(reverse=False)
        for i in range(0, tocount):
            self.scorePY += rPY[i]
        
        rPersonal = self.resultsPersonal[:]
        rPersonal.sort(reverse=False)
        for i in range(0 , tocount):
            self.scorePersonal += rPersonal[i]

    def summary(self):
        row = "<tr><td>" + self.name + "</td><td>"
        for b in self.boats:
            row += b + " "
        row += "</td>"
        for r in self.resultsPY:
            if r == self.dnc:
                row += "<td></td>"
            else:
                row += "<td>" + str(r) + "</td>"
        row += "<td>" + str(self.scorePY) + "</td></tr>"
        #print(row)
        return row

    def summaryPersonal(self):
        row = "<tr><td>" + self.name + "</td><td>"
        for b in self.boats:
            row += b + " "
        row += "</td>"
        for r in self.resultsPersonal:
            if r == self.dnc:
                row += "<td></td>"
            else:
                row += "<td>" + str(r) + "</td>"
        row += "<td>" + str(self.scorePersonal) + "</td></tr>"
        #print(row)
        return row
