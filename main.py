import numpy
import math
import ast
import pickle as dill
 
def numToTimeS(d):
    minute, hour = math.modf(d)
    m = int(minute * 100)
    if m == 0:
    	m = "00"
    r = str(int(hour)) + ":" + str(m)
    return r
 
class Course (object):
    name = "default name"
    start = 0
    end = 2
    include = False
    ID = 00000
 
    def __init__(self, name, days, start, end, include, ID):
        self.name = name
        self.days = days
        self.start = start
        self.end = end
        self.ID = ID
        self.include = include
 
    def __str__(self):
        return "Course: " + self.name + "\nBegins: " + numToTimeS(self.start) + "\nEnds: " + numToTimeS(self.end) + "\nID: " + str(self.ID) + "\n" + "Included: " + str(self.include)
 
class Day (object):
    size = 24
    name = "day"
    timeslots = numpy.empty(size, dtype=object)
    
    def __init__ (self, name):
        self.name = name

class Conflict(object):
	competitors = []
	
class Week(object):
    days = []
    
    def __init__(self):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for i in days:
            self.days.append(Day(i))
    def __str__(self):
		str = ""
		for day in self.days:
			times = ""
			for t in day.timeslots:
				if t == None:
					times += " | No Class"
				elif t.type != Conflict:
					times += (" | " + t.name) 
				else:
					con = ""
					for c in t.competitors:
						con += c.name + "; "
					times += (" | " + "conflict between " + con )
			str += "| " + day.name + times + " |\n"
		return str

def viewSelected(courses):
	for c in courses:
		if c.include:
			print(c)
		else:
			continue

def deleteCourse(course, courses):
	try:
		courses.remove(course)
	except:
		pass

def removeCourse(courses):
	ID = raw_input("ID of Course to be Deleted: ")
	for c in courses:
		if c.ID == ID:
			deleteCourse(c, courses)

def addCourse(courses):
	name = raw_input("Name of course: ")
	days = raw_input("Days of course, separated by ',': ")
	start = float(raw_input("Start Time of course: "))
	end = float(raw_input("End Time of course: "))
	ID = int(raw_input("Course ID: "))
	include = raw_input("Include in schedule? Y/N")
	if include == "Y" or include == "y":
		include = True
	elif include == "N" or include == "n":
		include = False
	else:
		print("bad input & you should feel bad")
		# TODO: make them go back and change it
	courses.append(Course(name, start, end, include, ID))

def viewCourses(courses):
	for c in courses:
		print(c)

def include(course):
	course.include = True
	
def exclude(course):
	course.include = False
	
# TODO: make this modular
def viewSchedule(week):
	print("| Day | 9:00 - 9:30 AM | 9:30 - 10:00 AM | 10:00 - 10:30 AM | 10:30 - 11:00 AM | 11:00 - 11:30 AM | 11:30 AM - 12:00 PM |" +
	       " 12:00 - 12:30 PM | 12:30 - 1:00 PM | 1:00 - 1:30 PM | 1:30 - 2:00 PM | 2:00 - 2:30 PM | 2:30 PM - 3:00 PM | 3:00 PM - 3:30 PM |" +
	       " 3:30 - 4:00 PM | 4:00 - 4:30 PM | 4:30 - 5:00 PM | 5:00 - 5:30 PM | 5:30 - 6:00 PM | 6:00 - 6:30 PM | 6:30 - 7:00 PM | 7:00 - 7:30 PM |" +
	       " 7:30 - 8:00 PM | 8:00 PM - 8:30 PM | 8:30 - 9:00 PM |\n")
	print(week)

def editSInput(week, courses):
	action = raw_input("| Include | Exclude | Replace | Clear | Back | Help |")
	if action == "Include":
		courseID = raw_input("Input the ID of the course you want to include.")
		for c in courses:
			if c.ID == courseID:
				include(c)
			else:
				continue
	elif action == "Exclude":
		courseID = raw_input("Input the ID of the course you want to exclude.")
		for c in courses:
			if c.ID == courseID:
				exclude(c)
			else:
				continue
	elif action == "Replace":
		courseID = raw_input("Input the ID of the course you want to replace.")
		for c in courses:
			if c.ID == courseID:
				exclude(c)
			else:
				continue
		replaceID = raw_input("Now, input the ID of the course you want to replace it with.")
		for c in courses:
			if c.ID == replaceID:
				include(c)
			else:
				continue
	elif action == "Clear":
		answer = raw_input("Are you sure you want to clear the schedule? This change is irreversible. Y/N")
		if answer == "Y":
			print("Clearing...")
			del week
			waitForInput(courses, Week())
		elif answer == "N":
			editSInput(week, courses)
		else:
			print("Did not understand input, returning to edit menu.")
			editSInput(week, courses)
	elif action == "Back":
		waitForInput(courses, week)
	elif action == "Help":
		pass
	else:
		print("Command not recognized, please try again")
		editSInput(week, courses)

def editSchedule(week, courses):
	print("|__ Current Schedule __|")
	viewSchedule(week)
	editSInput(week, courses)

def weekToMarkdown(week):
	mkd = ("| Day | 9:00 - 9:30 AM | 9:30 - 10:00 AM | 10:00 - 10:30 AM | 10:30 - 11:00 AM | 11:00 - 11:30 AM | 11:30 AM - 12:00 PM |" +
	       " 12:00 - 12:30 PM | 12:30 - 1:00 PM | 1:00 - 1:30 PM | 1:30 - 2:00 PM | 2:00 - 2:30 PM | 2:30 PM - 3:00 PM | 3:00 PM - 3:30 PM |" +
	       " 3:30 - 4:00 PM | 4:00 - 4:30 PM | 4:30 - 5:00 PM | 5:00 - 5:30 PM | 5:30 - 6:00 PM | 6:00 - 6:30 PM | 6:30 - 7:00 PM | 7:00 - 7:30 PM |" +
	       " 7:30 - 8:00 PM | 8:00 PM - 8:30 PM | 8:30 - 9:00 PM |\n" +
	      "| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n")
	return (mkd + str(week))
	
# saveSchedule(current_week, all_courses)
def saveSchedule(week, courses):
	dfile = raw_input("Name of data file? For default leave blank.")
	if dfile == "":
		dfile = "data"
	sfile = raw_input("Name of schedule file? For default leave blank.")
	if sfile == "":
		sfile = "schedule"
	with open((dfile+".pkl"), 'wb') as f, open((sfile+".md"), 'w') as mkd:
		dill.dump(week, f)
		dill.dump(courses, f)
		mkd.write(weekToMarkdown(week))
    	
# returns (week, all_courses)
def loadSchedule():
	with open(filename, 'rb') as f:
		week = dill.load(f)
		courses = dill.load(f)
		return (week, courses)

def waitForInput(courses, week):
	action = raw_input("| Add Course | Remove Course | View Courses | View Schedule | Edit Schedule | Quit | Help |\n")
	if action == "Add Course" or action == "Add" or action == "a":
		addCourse(courses)
		waitForInput(courses, week)
	elif action == "Remove Course" or action == "Remove" or action == "r":
		removeCourse(courses)
		waitForInput(courses, week)
	elif action == "View Courses" or action == "View C" or action == "vc":
		viewCourses(courses)
		waitForInput(courses, week)
	elif action == "Edit Courses" or action == "Edit C" or action == "ec":
		pass
	elif action == "View Schedule" or action == "View S" or action == "vs":
		viewSchedule(week)
		waitForInput(courses, week)
	elif action == "Edit Schedule" or action == "Edit S" or action == "es":
		editSchedule(week, courses)
		waitForInput(courses, week)
	elif action == "Help" or action == "h":
		pass
	elif action == "Quit" or action == "q":
		print("Exiting...")
		quit()
	else:
		print("Command not recognized. Try again, or enter 'Help' for instructions.")
		waitForInput(courses, week)

def main():
	print("Opening save...")
	try: 
		week, courses = loadSchedule()
		print("Save loaded...")
	except Exception:
		week = Week()
		courses = []
		print("No save found, blank save created...")
	waitForInput(courses, week)
	saveSchedule(week, courses)

if __name__ == "__main__":
    main()
