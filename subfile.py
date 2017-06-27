# contains functions to modify data initialized in settings.py

import random, string
import settings
import courses as src
import professors as profs
import main
import ast
import pickle as dill

# def restoreDeleted():

# def undo():

def getProfs(names):
    profs = []
    for name in names:
        for p in settings.professors:
            if p.name == name:
                profs.append(p)
    return profs

def addProfGUI(p):
    settings.professors.append(p)

def addProf():
    name = raw_input("Name of professor: ")
    q = int(raw_input("Q Score: "))
    dept = raw_input("Department: ")
    course_ids = raw_input("IDs of Taught Courses: ")
    cids = course_ids.split(",")
    courses = []
    prof = profs.Professor(name, q, dept)
    for cid in cids:
        for course in settings.courses:
            if course.ID == int(cid):
                prof.addCourseDirectc(course)
                course.addProf(prof)
    settings.professors.append(prof)

def deleteProfGUI(p):
    for c in p.courses:
        c.removeProf(p)
    settings.professors.remove(p)

def deleteProf():
    name = raw_input("Enter name of prof to delete: ")
    for p in settings.professors:
        if p.name == name:
            print("Removing " + p.name)
            for c in p.courses:
                print("removing prof from " + c.name)
                c.removeProf(p)
            settings.professors.remove(p)
        else:
            pass

def assignProf():
    name = raw_input("Enter name of prof to assign: ")
    course = int(raw_input("Enter ID of course to assign to: "))
    for p in settings.professors:
        if p.name == name:
            for c in settings.courses:
                if c.ID == course:
                    c.addProf(p)
                    p.addCourseDirect(c)


def getCourses():
    return settings.courses

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

def randomday():
    return [random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])]

def randomCourse():
    t = random.randint(9, 21)
    q = random.randint(0, 5)
    return src.Course(randomword(5), randomday(), t, t+3, True, random.randint(0, 50000), q)

def randomProf():
    q = random.randint(0, 5)
    subjects = ["History", "Science"]
    return profs.Professor(randomword(5), q, random.choice(subjects))

def assignRandProf(c):
    c.addProf(random.choice(settings.professors))

def assignRandCourse(p):
    p.addCourseDirect(random.choice(settings.courses))

def default():
    prof = profs.Professor("Jill Lepore", 5, "History")
    course = src.Course("Test",["Monday", "Wednesday"], 16, 17.5, True, 12345, [prof], 5)
    prof.addCourseDirect(course)
    settings.courses = [course]
    settings.professors = [prof]

def randomSession():
    default()
    for i in range(3):
        settings.courses.append(randomCourse())
    for i in range(3):
        p = randomProf()
        assignRandCourse(p)
        settings.professors.append(p)

def saveCoursesGUI(dfile, sfile):
    with open((dfile), 'wb') as f, open((sfile), 'w') as mkd:
        print("Saving data to " + dfile)
        dill.dump(settings.courses, f)
        dill.dump(settings.professors, f)
        print("Saving schedule to " + sfile)
        mkd.write(main.weekToMarkdown())
        f.close()
        mkd.close()

def saveCourses():
    dfile = raw_input("Name of data file? For default leave blank.")
    if dfile == "":
        dfile = "data.obj"
    sfile = raw_input("Name of schedule file? For default leave blank.")
    if sfile == "":
        sfile = "schedule.md"
    with open((dfile), 'wb') as f, open((sfile), 'w') as mkd:
        print("Saving data to " + dfile)
        dill.dump(settings.courses, f)
        dill.dump(settings.professors, f)
        print("Saving schedule to " + sfile)
        mkd.write(main.weekToMarkdown())
        f.close()
        mkd.close()

def loadCoursesGUI(filename):
    try:
        with open(filename, 'rb') as f:
            f.seek(0)
            print("loading " + filename)
            settings.courses = dill.load(f)
            settings.professors = dill.load(f)
    except:
        print("issue loading, setting to default")
        default()

def loadCourses(filename = "data"):
    try:
        with open((filename+".obj"), 'rb') as f:
            f.seek(0)
            print("loading " + filename)
            settings.courses = dill.load(f)
            settings.professors = dill.load(f)
    except:
        print("issue loading, setting to default")
        default()

def include():
    courseID = int(raw_input("Input the ID of the course you want to include."))
    for c in settings.courses:
        if c.ID == courseID:
            print("Including: " + c.name)
            c.include = True
    
def exclude():
    courseID = int(raw_input("Input the ID of the course you want to exclude."))
    for c in settings.courses:
        if c.ID == courseID:
            c.include = False

def excludeAll():
    for c in settings.courses:
        c.include = False

def deleteCourse(course):
    try:
        settings.courses.remove(course)
    except:
        pass

def deleteCourseGUI(ID):
    for c in settings.courses:
        if c.ID == ID:
            settings.courses.remove(c)

def removeCourse():
    ID = int(raw_input("ID of Course to be Deleted: "))
    for c in settings.courses:
        if c.ID == ID:
            deleteCourse(c)
    return updateWeek()

def addCourse():
    name = raw_input("Name of course: ")
    days = raw_input("Days of course, separated by ',': ")
    start = float(raw_input("Start Time (24H) of course: "))
    end = float(raw_input("End Time (24H) of course: "))
    ID = int(raw_input("Course ID: "))
    profs = raw_input("Professors who teach this course, separated by ',': ")
    q = int(raw_input("Course Q score: "))
    for course in settings.courses:
        # TODO make this loop
        if course.ID == ID:
            print("ID already exists, cannot add course. Input new ID: ")
            ID = int(raw_input("Course ID: "))
    include = raw_input("Include in schedule? Y/N")
    if include == "Y" or include == "y":
        include = True
    elif include == "N" or include == "n":
       include = False
    else:
        print("bad input & you should feel bad")
        # TODO: make them go back and change it
    settings.courses.append(src.Course(name,(days.split(",")), start, end, include, ID, getProfs(profs.split(",")), q))

def addCourseGUI(c):
    settings.courses.append(c)
