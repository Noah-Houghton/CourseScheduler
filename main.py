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
    size = 28
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
 
def viewAll(courses):
    for c in courses:
        print(c)

def include(course):
	course.include = True
	
def notInclude(course):
	course.include = False

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
	
