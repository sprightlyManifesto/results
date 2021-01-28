from serise import Series
pth = r"/home/richard/results/2020/"

Series(pth + "2020.csv", pth + "2020_QE_OCT.txt", {pth +"autumn/"},"autumn").summary(True, True, "autumn.html")


"""
Series(pth + "2020.csv", pth + "2020_Feb_QE.txt", {pth +"summer/"},"summer").summary(True, True, "summer.html")

Series(pth + "2020.csv", pth + "2020_Feb_QE.txt", {pth +"wednesdays/"},"wednesdays").summary(False,False, "wednesdays.html")

#2020 boat type
Series(pth + "2020.csv", pth + "2020_Feb_QE.txt", {pth+"summer/"},"singles").filterByBoatType("S").summary(True,True,"singles.html")
Series(pth + "2020.csv", pth + "2020_Feb_QE.txt", {pth +"summer/"},"cats").filterByBoatType("C").summary(True,True,"cats.html")
Series(pth + "2020.csv", pth + "2020_Feb_QE.txt", {pth +"summer/"},"doubles").filterByBoatType("D").summary(True,True,"doubles.html")
Series(pth + "2020.csv", pth + "2020_Feb_QE.txt", {pth +"summer/"},"lasers").filterByBoatType("L").summary(True,True,"lasers.html")

Series(pth + "2020.csv", pth + "2020_Feb_QE.txt", {pth +"summer/"},"juniors").filterByAge("J").summary(True,False,"juniors.html")
Series(pth + "2020.csv", pth + "2020_Feb_QE.txt", {pth +"summer/"},"seniors").filterByAge("S").summary(True,False,"seniors.html")
Series(pth + "2020.csv", pth + "2020_Feb_QE.txt", {pth +"summer/"},"masters").filterByAge("M").summary(True,False,"masters.html")
Series(pth + "2020.csv", pth + "2020_Feb_QE.txt", {pth +"summer/"},"grandmasters").filterByAge("G").summary(True,False,"Grandmasters.html")
"""

#Usage:
#Serise(handicap file,Quick entry code file, list of directorys containing race files)
#series.summary(PYresult, personalResult, output html file) 

#Series(pth + "2019.csv", pth + "2019_APRIL_QE.csv", {pth +"Houghton/"},"Houghton Cup").summary(True, True, "Houghton Cup.html")
#Series(pth + "2019.csv", pth + "2019_APRIL_QE.csv", {pth +"caulcott/"},"Caulcott Cup").summary(True, True, "Caulcott Cup.html")
#Series(pth + "2019.csv", pth + "2019_APRIL_QE.csv", {pth +"watts/"},"Watts Cup").summary(True, True, "Watts Cup.html")
#Series(pth + "2019.csv", pth + "2019_APRIL_QE.csv", {pth +"AM/"},"AM").summary(True, True, "AM.html")
#Series(pth + "2019.csv", pth + "2019_APRIL_QE.csv", {pth +"PM/"},"PM").summary(True, True, "PM.html")

#Series(pth + "2019.csv", pth + "2019_APRIL_QE.csv", {pth +"PM/",pth +"AM/"},"singles").filterByBoatType("S").summary(True,True,"singles.html")
#Series(pth + "2019.csv", pth + "2019_APRIL_QE.csv", {pth +"PM/",pth +"AM/"},"doubles").filterByBoatType("D").summary(True,True,"doubles.html")
#Series(pth + "2019.csv", pth + "2019_APRIL_QE.csv", {pth +"PM/",pth +"AM/"},"cats").filterByBoatType("C").summary(True,False,"cats.html")
#Series(pth + "2019.csv", pth + "2019_APRIL_QE.csv", {pth +"PM/",pth +"AM/"},"Lasers").filterByBoatType("L").summary(True,False,"lasers.html")

#Series(pth + "2019.csv", pth + "2019_APRIL_QE.csv", {pth +"PM/"},"Juniors").filterByAge("J").summary(True,False,"juniors.html")
#Series(pth + "2019.csv", pth + "2019_APRIL_QE.csv", {pth +"PM/",pth +"AM/"},"Seniors").filterByAge("S").summary(True,False,"seniors.html")
#Series(pth + "2019.csv", pth + "2019_APRIL_QE.csv", {pth +"PM/",pth +"AM/"},"Masters").filterByAge("M").summary(True,False,"masters.html")
#Series(pth + "2019.csv", pth + "2019_APRIL_QE.csv", {pth +"PM/",pth +"AM/"},"GrandMasters").filterByAge("G").summary(True,False,"grandmasters.html")

#Series(pth + "2019.csv", pth + "2019_APRIL_QE.csv", {pth +"Wendensday/"},"Wendensday").summary(False,False,"Wendensday.html")
