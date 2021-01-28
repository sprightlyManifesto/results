from tkinter import *
import datetime
import re


class createRace:

	def buttonCallback(self):
		RO = self.ROEntry.get()
		date = self.dateEntry.get()
		race = self.raceEntry.get()
		AM = self.AM.get()
		PM = self.PM.get()
		#First parameter is the replacement, second parameter is your input string

		
		if (PM != AM) and RO != "" and date != "" and race != "":
			fileName = date.replace("_","-") + "_"  + race.replace("_","-") + "_" + RO.replace("_","-") 
			fileName = re.sub('[^a-z0-9_-]', '-', fileName.lower())
			if AM: fileName += "AM"
			else: fileName += "PM"
			print(fileName)
		else:
			print("all fields must be populated")
		
	def AMCallback(self):
		self.checkPM.deselect()
		self.checkAM.select()
		print("AM" , self.AM)
	
	def PMCallback(self):
		self.checkPM.select()
		self.checkAM.deselect()
		print("PM", self.PM)
		
	def __init__(self):
		self.root = Tk()
		self.AM = BooleanVar()
		self.PM = BooleanVar()
		
		#widgets
		self.createButton = Button(self.root,text ="Create",command=self.buttonCallback)#button1.bind("<Button-1>",eCallback)
		self.dateEntry = Entry(self.root) 
		self.dateEntry.delete(0,END)
		self.dateEntry.insert(0,datetime.datetime.now().strftime("%Y-%m-%d"))
		self.raceEntry = Entry(self.root)
		self.ROEntry= Entry(self.root)
		self.checkAM = Checkbutton(self.root,text = "AM",  variable=self.AM,command = self.AMCallback)
		self.checkPM = Checkbutton(self.root,text = "PM", variable=self.PM, command = self.PMCallback)
		
		#layout
		Label(self.root, text="Date").grid(row=0, sticky=E)
		self.dateEntry.grid(row=0,column= 1)
		Label(self.root, text="Race").grid(row=1, sticky=E)
		self.raceEntry.grid(row=1,column= 1)
		Label(self.root, text="RO").grid(row =2,sticky=E)
		self.ROEntry.grid(row=2,column = 1)
		self.checkAM.grid(row=3)
		self.checkPM.grid(row=3,column = 1)
		self.createButton.grid(row =4, columnspan=2)
		#entry_1.grid(row =0,columnspan = 3)
		#entry_2.grid(row =0,columnspan = 3)
		
		self.root.mainloop()
		

		
		
	
if __name__ == "__main__":
	createRace()
	