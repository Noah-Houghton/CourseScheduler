import numpy
import math
import pickle as dill
 
def numToTimeS(d):
    minute, hour = math.modf(d)
    return string(hour) + ":" + string(minute)
 
class Course (object):
    name = "default name"
    start = 0
    end = 2
    include = False
    ID = 00000
 
    def __init__(self, name, start, end, include, ID):
        self.name = name
        self.start = start
        self.end = end
        self.ID = ID
        self.include = include
 
    def __str__(self):
        return "Course: " + self.name + "\nBegins: " + numToTimeS(self.start) + "\nEnds: " + numToTimeS(self.end) + "\n"
 
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
						con += c.name + ";"
					times += (" | " + "conflict between " + con )
			str += " | " + day.name + " | " + times + " |"
		return str

def viewAll(courses):
    for c in courses:
        print(c)

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
	start = double(raw_input("Start Time of course: "))
	end = double(raw_input("End Time of course: "))
	ID = int(raw_input("Course ID: "))
	include = raw_input("Include in schedule? Y/N")
	if include == "Y" or include == "y":
		include = True
	elif include == "N" or include == "n":
		include = False
	else:
		print("bad input & you should feel bad")
		# TODO: make them go back and change it
	courses.append(Course(name, start, end, ID, include))

def viewCourses(courses):
	pass

def include(course):
	course.include = True
	
def notInclude(course):
	course.include = False
	
# TODO: make this modular
def drawSchedule(week):
	print("| 9:00 - 9:30 AM | 9:30 - 10:00 AM | 10:00 - 10:30 AM | 10:30 - 11:00 AM | 11:00 - 11:30 AM | 11:30 AM - 12:00 PM |" +
	       " | 12:00 - 12:30 PM | 12:30 - 1:00 PM | 1:00 - 1:30 PM | 1:30 - 2:00 PM | 2:00 - 2:30 PM | 2:30 PM - 3:00 PM | 3:00 PM - 3:30 PM |" +
	       " | 3:30 - 4:00 PM | 4:00 - 4:30 PM | 4:30 - 5:00 PM | 5:00 - 5:30 PM | 5:30 - 6:00 PM | 6:00 - 6:30 PM | 6:30 - 7:00 PM |")
	print(week)
	
def weekToMarkdown(week):
	mkd = ("| 9:00 - 9:30 AM | 9:30 - 10:00 AM | 10:00 - 10:30 AM | 10:30 - 11:00 AM | 11:00 - 11:30 AM | 11:30 AM - 12:00 PM |" +
	       " | 12:00 - 12:30 PM | 12:30 - 1:00 PM | 1:00 - 1:30 PM | 1:30 - 2:00 PM | 2:00 - 2:30 PM | 2:30 PM - 3:00 PM | 3:00 PM - 3:30 PM |" +
	       " | 3:30 - 4:00 PM | 4:00 - 4:30 PM | 4:30 - 5:00 PM | 5:00 - 5:30 PM | 5:30 - 6:00 PM | 6:00 - 6:30 PM | 6:30 - 7:00 PM |" +
	      "\n | ---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |")
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

def waitForInput():
	action = raw_input("Add Course | Remove Course | View Courses | View Schedule | Edit Schedule | Help")
	if action == "Add Course" or action == "Add" or aciton == "a":
		addCourse()
		waitForInput()
	elif action == "Remove Course" or action == "Remove" or action == "r":
		removeCourse()
		waitForInput()
	elif action == "View Courses" or action == "View C" or action == "vc":
		pass
	elif action == "Edit Courses" or action == "Edit C" or action == "ec":
		pass
	elif action == "View Schedule" or action == "View S" or action == "vs":
		pass
	elif action == "Edit Schedule" or action == "Edit S" or action == "es":
		pass
	elif action == "Help" or action == "h":
		pass

def main():
	print("Opening save...")
	try: 
		week, courses = loadSchedule()
		print("Save loaded")
	except Exception:
		week = Week()
		courses = []
		print("No save found, blank save loaded")
	viewAll(courses)
	drawSchedule(week)
	saveSchedule(week, courses)

if __name__ == "__main__":
    main()
