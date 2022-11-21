import os
from serise import Series

pyFile = "2020.csv"

#Icicle
Series(pyFile, "2021_QE_OCT.txt", {"Icicle"},"Icicle").filterByBoatType("M").summary(True, True, "IcicleMonos.html")
Series(pyFile, "2021_QE_OCT.txt", {"Icicle"},"Icicle").filterByBoatType("C").summary(True, True, "IcicleCats.html")

#shortCourse
Series(pyFile, "2022_QE_APRIL.txt", {"shortCourse1"},"shortCourse1",countAll=True).summary(True, True, "shortCourse1.html")
Series(pyFile, "2022_QE_APRIL.txt", {"shortCourse2"},"shortCourse2",countAll=True).summary(True, True, "shortCourse2.html")
Series(pyFile, "2022_QE_APRIL.txt", {"shortCourse3"},"shortCourse3",countAll=True).summary(True, True, "shortCourse3.html")
Series(pyFile, "2022_QE_JUNE.txt",  {"shortCourse4"},"shortCourse4",countAll=True).summary(True, True, "shortCourse4.html")

#normal Sundays
Series(pyFile, "2022_QE_APRIL.txt", {"fastnet"},"fastnet").filterByBoatType("M").summary(True, True, "fastnetMonos.html")
Series(pyFile, "2022_QE_APRIL.txt", {"fastnet"},"fastnet").filterByBoatType("C").summary(True, True, "fastnetCats.html")
Series(pyFile, "2022_QE_JUNE.txt",  {"portland"},"portland").filterByBoatType("M").summary(True, True, "portlandMonos.html")
Series(pyFile, "2022_QE_JUNE.txt",  {"portland"},"portland").filterByBoatType("C").summary(True, True, "portlandCats.html")
Series(pyFile, "2022_QE_JUNE.txt",  {"rockall"},"rockall").filterByBoatType("M").summary(True, True, "rockallMonos.html")
Series(pyFile, "2022_QE_JUNE.txt",  {"rockall"},"rockall").filterByBoatType("C").summary(True, True, "rockallCats.html")

#Championship and cups
for type,filter in [("Monos","M"), ("Cats","C")]:
    Series(pyFile, "2022_QE_APRIL.txt", {"houghton"},"Houghton").filterByBoatType(filter).summary(True, False, f"Houghton{type}.html")
    Series(pyFile, "2022_QE_APRIL.txt", {"caulcott"},"Caulcott").filterByBoatType(filter).summary(True, False, f"Caulcott{type}.html")
    Series(pyFile, "2022_QE_JUNE.txt",  {"Watts"},"Watts").filterByBoatType(filter).summary(True, False, f"WattsMonos{type}.html")
    Series(pyFile, "2022_QE_JUNE.txt",  {"blackaby"},"blackaby").filterByBoatType(filter).summary(True, False, f"Blackaby{type}.html")

Series(pyFile, "2022_QE_JUNE.txt",  {"houghton","caulcott","Watts","blackaby"},"Championship").summary(True, False, "Championship.html")

#Wednesdays
Series(pyFile, "2022_QE_JUNE.txt",  {"wednesday"},"wednesday").summary(False, False, "wednesday.html",score=False)

#BoatTypes
for type,filter in [("singles","S"), ("Doubles","D"),("lasers","L"),("cats","C")]:
    Series(pyFile, "2022_QE_JUNE.txt",  {"fastnet","portland","rockall"},"type").filterByBoatType("S").summary(True,False,f"{type}.html")
#AgeGroups
for type,filter in [("juniors","J"),("seniors","S"),("masters","M"),("grandmasters","G")]:
    Series(pyFile, "2022_QE_JUNE.txt",  {"fastnet","portland","rockall"},type).filterByAge(filter).summary(True,False,f"{type}.html")

for type,filter in [("Monos","M"), ("Cats","C")]:
    Series(pyFile, "2022_QE_NOV.txt", {"Autumn"},"Autumn").filterByBoatType(filter).summary(True, False, f"Autumn{type}.html")
