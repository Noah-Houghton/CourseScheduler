# contains classes and helper methods to construct and print Professors
import settings

def coursesNames(courses):
    st = ""
    for ix, c in enumerate(courses):
        if ix < len(courses) - 3:
            st += c.name + ", "
        elif ix > 0 and len(courses) == 2:
            st += "and " + c.name
        elif ix < len(courses) - 2:
            st += c.name + ", and "
        else:
            st += c.name
    return st

class Professor(object):
    def __init__(self, name = "default", q = 0, department = "default", courses = None):
        self.name = name
        self.q = q
        self.department = department
        if courses == None:
            self.courses = []
        else:
            self.courses = courses
            for c in courses:
                if self not in c.profs:
                    c.addProf(self)


    def addCourseByID(self, ID):
        for course in settings.courses:
            if ID == course.ID:
                self.courses.append(course)
                if self in course.profs:
                    course.removeProf(self)

    def addCourseDirect(self, c):
        self.courses.append(c)
        if self not in c.profs:
            c.addProf(self)

    def __str__(self):
        return ("Prof. "+ self.name + "\nQ Score: " + str(self.q) + "\nDepartment: " + self.department + "\nTeaches: " + coursesNames(self.courses) + "\n")
