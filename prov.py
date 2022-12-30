import os
import argparse
from datetime import datetime

SCP = False

parser = argparse.ArgumentParser()
parser.add_argument("ip", help="last byte of PI's IP address")
args = parser.parse_args()

html = "<html><head></head><body><H1>Provisional Results</H1>\n"
os.chdir("prov")
if SCP:
    os.system(f"scp ro@192.168.1.{args.ip}:~/results/results/*.html .")
if SCP:
    os.system(f"scp ro@192.168.1.{args.ip}:~/results/races/*.race .")
os.system("chmod 666 ~/results/prov/*")
print(os.getcwd())
files = []
for f in os.listdir():
    if f.endswith(".html") and f != "index.html":
        try:
            dt = datetime.strptime(f.split("_")[-1], "%d-%m-%Y.html")
        except:
            dt = datetime.now()
        files.append((f, dt))

dt = datetime.now()

for f in sorted(files, key=lambda x: x[1], reverse=True):
    fn = f[0]
    if dt != f[1]:
        html += "<br>"
        dt = f[1]
    html += f'<a href="{fn}">{fn[:-5]}</a><br>'
    html += "\n"
    print(f"indexing: {fn} {f[1]}")

html += "</body></html>\n"

open("index.html", "w").write(html)

if SCP:
    os.system(
        "scp *.html stewartby-watersports.org.uk@web9.extendcp.co.uk:~/public_html/sailing/Results/prov"
    )
if SCP:
    os.system(
        "ssh stewartby-watersports.org.uk@web9.extendcp.co.uk chmod 666 ~/public_html/sailing/Results/prov/*.html"
    )

os.chdir("..")
