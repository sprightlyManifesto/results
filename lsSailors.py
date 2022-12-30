import os

dirs = (
    "Autumn",
    "blackaby",
    "caulcott",
    "fastnet",
    "houghton",
    "Icicle",
    "portland",
    "rockall",
    "shortCourse1",
    "shortCourse2",
    "shortCourse3",
    "shortCourse4",
    "Watts",
    "wednesday",
)
sailors = set()

for d in dirs:
    for f in os.listdir("d"):
        if f.endswith(".race"):
            file = open(f)
            line = file.readline()
            while not ("<HANDICAPS>" in line):
                line = file.readline()
                toks = line.split(",")
                if len(toks) > 3:
                    sailors.add(toks[1])

for s in sailors:
    print(s)
