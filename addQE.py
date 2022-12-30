import tkinter as tk
from tkinter import Listbox, Button, StringVar, Radiobutton, Frame, Label, Entry
from tkinter.ttk import Combobox
from QE import QE

top = tk.Tk()
top.geometry("800x600")

QEcode = StringVar()
helm = StringVar()
crew = StringVar()
dinghy = StringVar()
sailNo = StringVar()
personal = StringVar()
ageGroup = StringVar()
goldSilverGroup = StringVar()
message = StringVar()

handicapsFile = "2020.csv"
recordsFile = "2022_QE_NOV.txt"

classes = {c.split(",")[0]: None for c in open(handicapsFile, "r").readlines()}
records = [r for r in open(recordsFile, "r").read().split("\n") if len(r.strip()) > 0]
records.sort(key=lambda x: x.split(",")[1])

recordIndex = 0


def GUItoLine():
    line = f"{QEcode.get()},{helm.get()},{crew.get()},{dinghy.get()},"
    line += f"{sailNo.get()},{personal.get()},{ageGroup.get()},{goldSilverGroup.get()}"
    return line


def findRecordIndex(line):
    recordIndex = None
    for idx, r in enumerate(records):
        if line == r:
            recordIndex = idx


def setReadMode():
    editButton.config(state="normal")
    submitButton.config(state="disabled")
    cancelButton.config(state="disabled")
    addButton.config(state="normal")
    Lb1.config(state="normal")
    for c in recordControls:
        c.config(state="disabled")


def setEditMode():
    editButton.config(state="disabled")
    submitButton.config(state="normal")
    cancelButton.config(state="normal")
    addButton.config(state="disabled")
    Lb1.config(state="disabled")
    for c in recordControls:
        c.config(state="normal")
    line = GUItoLine()
    print(line)
    findRecordIndex(line)
    Lb1.state = "disabled"


def listChangeCallback(caller):
    line = Lb1.get("active")
    qe = QE(line, classes)
    QEcode.set(qe.QE)
    helm.set(qe.helm)
    crew.set(qe.crew)
    dinghy.set(qe.dinghy)
    sailNo.set(qe.sailno)
    personal.set(qe.personal)
    goldSilverGroup.set(qe.fleet)
    ageGroup.set(qe.ageGroup)


def addButtonCallBack():
    setEditMode()
    QEcode.set("")
    helm.set("")
    crew.set("")
    dinghy.set("LASER")
    sailNo.set("")
    personal.set("")
    ageGroup.set(None)
    goldSilverGroup.set(None)
    recordIndex = None


def submitButtonCallBack():
    line = GUItoLine()
    msg = QE(line, classes).message
    message.set(msg)
    if message == "":
        Lb1.config(state="normal")
        Lb1.delete(0, "end")
        print("Submit sucseeded")
        if recordIndex == None:
            records.append(line)
        else:
            records[recordIndex] = line
        records.sort(key=lambda x: x.split(",")[1])
        for i, record in enumerate(records):
            Lb1.insert(i, record)
        Lb1.select_set(recordIndex, recordIndex)
        setReadMode()
    else:
        print(msg)


def cancelButtonCallBack():
    listChangeCallback(None)
    setReadMode()


topFrame = Frame(top)
rowsFrame = Frame(topFrame, highlightthickness=0)
col1Frame = Frame(rowsFrame, highlightthickness=0)
col2Frame = Frame(rowsFrame, highlightthickness=0)
ButtonFrame = Frame(topFrame, highlightthickness=0)
AgeGroupFrame = Frame(topFrame, highlightbackground="blue", highlightthickness=1)
GoldSilverFrame = Frame(topFrame, highlightbackground="blue", highlightthickness=1)

QEcodeEntry = Entry(col1Frame, width=30, textvariable=QEcode)
HelmEntry = Entry(col1Frame, width=30, textvariable=helm)
CrewEntry = Entry(col1Frame, width=30, textvariable=crew)
SailNoEntry = Entry(col2Frame, width=20, textvariable=sailNo)
PersonalEntry = Entry(col2Frame, width=20, textvariable=personal)
DinghyClassEntry = Combobox(
    col2Frame, width=20, textvariable=dinghy, values=list(classes.keys())
)

JuniorRadio = Radiobutton(AgeGroupFrame, text="Junior", variable=ageGroup, value="J")
SeniorRadio = Radiobutton(AgeGroupFrame, text="Senior", variable=ageGroup, value="S")
MastersRadio = Radiobutton(AgeGroupFrame, text="Master", variable=ageGroup, value="M")
GrandMastersRadio = Radiobutton(
    AgeGroupFrame, text="Grandmaster", variable=ageGroup, value="G"
)
GoldRadio = Radiobutton(
    GoldSilverFrame, text="Gold", variable=goldSilverGroup, value="G"
)
SilverRadio = Radiobutton(
    GoldSilverFrame, text="Silver", variable=goldSilverGroup, value="S"
)

recordControls = [
    QEcodeEntry,
    HelmEntry,
    CrewEntry,
    SailNoEntry,
    PersonalEntry,
    DinghyClassEntry,
    JuniorRadio,
    SeniorRadio,
    MastersRadio,
    GrandMastersRadio,
    GoldRadio,
    SilverRadio,
]

editButton = Button(ButtonFrame, text="Edit", command=setEditMode)
submitButton = Button(
    ButtonFrame, text="Submit", command=submitButtonCallBack, state="disabled"
)
cancelButton = Button(
    ButtonFrame, text="Cancel", command=cancelButtonCallBack, state="disabled"
)
addButton = Button(ButtonFrame, text="Add new", command=addButtonCallBack)

messageLabel = Label(top, textvariable=message)

Lb1 = Listbox(top, width=800, height=20)
for i, record in enumerate(records):
    Lb1.insert(i, record)
Lb1.select_set(0)
Lb1.bind("<<ListboxSelect>>", listChangeCallback)
listChangeCallback(None)

# Layout
Label(top, text=f"handicaps: {handicapsFile}  Qes: {recordsFile}").pack(
    fill="x", side="top"
)
messageLabel.pack()
for l, e in [("QE", QEcodeEntry), ("Helm", HelmEntry), ("Crew", CrewEntry)]:
    Label(col1Frame, text=l).pack(side="top", anchor="w")
    e.pack(side="top", anchor="w")

for l, e in [
    ("Class", DinghyClassEntry),
    ("SailNo", SailNoEntry),
    ("Personal", PersonalEntry),
]:
    Label(col2Frame, text=l).pack(side="top", anchor="w")
    e.pack(side="top", anchor="w")

topFrame.pack(side="top", fill="x", pady=10)

for f in (
    JuniorRadio,
    SeniorRadio,
    MastersRadio,
    GrandMastersRadio,
    GoldRadio,
    SilverRadio,
):
    f.pack(padx=5)

for f in (editButton, submitButton, cancelButton, addButton):
    f.pack(side="top", fill="x")

for f in (col1Frame, col2Frame, rowsFrame):
    f.pack(side="left", padx=5)

for f in (AgeGroupFrame, GoldSilverFrame, ButtonFrame):
    f.pack(side="left", padx=5, fill="y")

Lb1.pack()

top.title("Quick Entry Code Editor")
setReadMode()
top.mainloop()
