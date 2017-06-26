import numpy
import math

def numToTimeS(d):
    minute, hr = math.modf(d)
    am = True
    m = int(minute * 60)
    if m == 0:
        m = "00"
    if hr > 12:
        hr = hr - 12
        am = False
    if hr == 12:
        am = False
    r = str(int(hr)) + ":" + str(m)
    if am == True:
        r += " AM"
    else:
        r += " PM"
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
        for i in range(len(self.days[0].timeslots)):
            s = ""
            for day in self.days:
                if day.timeslots[i] == None:
                    s+= "| No Class "
                elif type(day.timeslots[i]) is Course:
                    s+="| " + day.timeslots[i].name
                else: 
                    con = ""
                    for c in day.timeslots[i].competitors:
                        con += c.name + "; "
                    s+="| conflict between " + con
            st += "| " + numToTimeS((i*.5) + day.start) + " - " + numToTimeS((i*.5) + .5 + day.start) + s + " |\n"
        return st