import settings
import courses as src
import main
import ast
import pickle as dill

def getCourses():
    return settings.courses

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

def randomday():
    return [random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])]

def randomCourse():
    t = random.randint(9, 21)
    settings.courses.append(src.Course(randomword(5), randomday(), t, t+3, True, random.randint(0, 50000)))

def defaultCourses():
    settings.courses = [src.Course("Test",["Monday", "Wednesday"], 16, 17.5, True, 12345)]

def saveCoursesGUI(dfile, sfile):
    with open((dfile), 'wb') as f, open((sfile), 'w') as mkd:
        print("Saving data to " + dfile)
        dill.dump(settings.courses, f)
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
        print("Saving data to " + dfile + ".obj")
        dill.dump(settings.courses, f)
        print("Saving schedule to " + sfile + ".md")
        mkd.write(main.weekToMarkdown())
        f.close()
        mkd.close()

def loadCoursesGUI(filename):
    try:
        with open(filename, 'rb') as f:
            f.seek(0)
            print("loading " + filename)
            settings.courses = dill.load(f)
    except:
        print("issue loading, setting to default")
        defaultCourses()

def loadCourses(filename = "data"):
    try:
        with open((filename+".obj"), 'rb') as f:
            f.seek(0)
            print("loading " + filename)
            settings.courses = dill.load(f)
    except:
        print("issue loading, setting to default")
        defaultCourses()

def viewCourses():
    if len(settings.courses) == 0:
        print("No Courses")
    else:
        for c in settings.courses:
            print(c)

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
    return courses

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
    settings.courses
    ID = int(raw_input("ID of Course to be Deleted: "))
    for c in courses:
        if c.ID == ID:
            deleteCourse(c)
    return updateWeek()

def addCourse():
    settings.courses
    name = raw_input("Name of course: ")
    days = raw_input("Days of course, separated by ',': ")
    start = float(raw_input("Start Time (24H) of course: "))
    end = float(raw_input("End Time (24H) of course: "))
    ID = int(raw_input("Course ID: "))
    for course in courses:
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
    settings.courses.append(src.Course(name,(days.split(",")), start, end, include, ID))

def addCourseGUI(c):
    settings.courses.append(c)