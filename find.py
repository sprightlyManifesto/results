import os

for f in os.listdir():
    if f.endswith(".py"):
        for i, l in enumerate(open(f).readlines()):
            if 'json.loads(open("config.json","r").read())' in l:
                print(f.ljust(20), f"line: {i}")
