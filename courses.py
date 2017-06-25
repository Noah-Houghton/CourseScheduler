import numpy
import math

def numToTimeS(d):
    minute, hr = math.modf(d)
    m = int(minute * 60)
    if m == 0:
        m = "00"
    if hr > 12:
        hr = hr - 12
    r = str(int(hr)) + ":" + str(m)
    return r

class Course(object):
    name = "default name"
    start = 0
    end = 2
    meetings = []
    include = False
    ID = 00000
 
    def __init__(self, name, meetings, start, end, include, ID):
        self.name = name
        self.meetings = meetings
        self.start = start
        self.end = end
        self.ID = ID
        self.include = include
 
    def __str__(self):
        return "Course: " + self.name + "\nMeets: " + str(self.meetings) + "\nBegins: " + numToTimeS(self.start) + "\nEnds: " + numToTimeS(self.end) + "\nID: " + str(self.ID) + "\n" + "Included: " + str(self.include) + "\n"

class Day(object):
    size = 24
    name = "day"
    start = 0.0
    
    def __init__ (self, name, start):
        self.name = name
        self.timeslots = numpy.empty(self.size, dtype=object)
        self.start = start

class Conflict(object):

    def __init__(self, seed):
        self.competitors = [seed]

    def __str__(self):
        st = "Conflicting courses: "
        for c in self.competitors:
            st += (c.name + ";")
        return st

class Week(object):
    days = [Day("Monday", 9), Day("Tuesday", 9), Day("Wednesday", 9), Day("Thursday", 9), Day("Friday", 9)]

    def __str__(self):
		st = ""
		for day in self.days:
			times = ""
			for t in day.timeslots:
				if t == None:
					times += " | No Class "
				elif type(t) is Course:
					times += (" | " + t.name) 
				else:
					con = ""
					for c in t.competitors:
						con += c.name + "; "
					times += (" | " + "conflict between " + con )
			st += "| " + day.name + times + " |\n"
		return st