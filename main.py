import numpy
import math
import dill
 
def numToTimeS(d):
    minute, hour = math.modf(d)
    return string(hour) + ":" + string(minute)
 
class Course (object):
    name = "default name"
    start = 0
    end = 2
    include = False
 
    def __init__(self, name, start, end, include):
        self.name = name
        self.start = start
        self.end = end
        self.include = include
 
    def __str__(self):
        return "Course: " + self.name + "\nBegins: " + numToTimeS(self.start) + "\nEnds: " + numToTimeS(self.end) + "\n"
 
class Day (object):
    size = 24
    name = "day"
    timeslots = numpy.empty(size, dtype=object)
    
    def __init__ (self, name):
        self.name = name
 
class Week (object):
    days = []
    
    def __init__(self):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for i in days:
            self.days.append(Day(days[i]))
    def __str__(self):
	str = ""
	for day in self.days:
		times = ""
		for t in day.timeslots:
			if t = NULL:
				times += "| No Class |"
			else:
				times += ("| " + t.name + " |") 
		str += day.name + "|" + times

def viewAll(courses):
    for c in courses:
        print(c)

def viewSelected(courses):
	for c in courses:
		if c.include:
			print(c)
		else:
			continue
	
def include(course):
	course.include = True
	
def notInclude(course):
	course.include = False
	
# TODO: make this modular
def drawSchedule(week):
	print ("| 9:00 - 9:30 AM | 9:30 - 10:00 AM | 10:00 - 10:30 AM | 10:30 - 11:00 AM | 11:00 - 11:30 AM | 11:30 AM - 12:00 PM |" +
	       " | 12:00 - 12:30 PM | 12:30 - 1:00 PM | 1:00 - 1:30 PM | 1:30 - 2:00 PM | 2:00 - 2:30 PM | 2:30 PM - 3:00 PM | 3:00 PM - 3:30 PM |" +
	       " | 3:30 - 4:00 PM | 4:00 - 4:30 PM | 4:30 - 5:00 PM | 5:00 - 5:30 PM | 5:30 - 6:00 PM | 6:00 - 6:30 PM | 6:30 - 7:00 PM |")
	print(week)
# saveSchedule(current_week, all_courses)
def saveSchedule(week, courses, filename = "data.pkl"):
	with open(filename, 'wb') as f:
		dill.dump(week, f)
		dill.dump(courses, f)
    	
# returns (week, all_courses)
def loadSchedule(filename = "data.pkl"):
	with open(filename, 'rb') as f:
		week = dill.load(f)
		courses = dill.load(f)
		return (week, courses)
        
def __main__():
	try: 
		week, courses = loadSchedule()
	except Exception:
		week = Week()
		courses = []
	viewAll(courses)
	drawSchedule(week)
	
