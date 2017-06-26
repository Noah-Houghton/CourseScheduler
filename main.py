import courses as src
import ast
import pickle as dill
import gui
import random, string

useGUI = True

courses = []

def getCourses():
    return courses

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

def randomday():
    return [random.choice(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])]

def randomCourse():
    t = random.randint(9, 21)
    return src.Course(randomword(5), randomday(), t, t+3, True, random.randint(0, 50000))

def defaultCourses():
    courses = [src.Course("Test",["Monday", "Wednesday"], 16, 17.5, True, 12345)]

# use for stub-code
def donothing():
    pass

def coursesToStr():
    if len(courses) == 0:
        return "No Courses Loaded"
    st = ""
    for c in courses:
        st += str(c)
    return st

def scheduleToStr():
    st = ("| Time | Monday | Tuesday | Wednesday | Thursday | Friday |\n")
    st += str(updateWeek())
    return st

def openGUI():
    app = gui.SchedulerAppGUI()
    app.mainloop()

def help():
    with open("help.txt", r) as help:
        print(help)

def viewSelected():
    for c in courses:
        if c.include:
            print(c)
        else:
            continue

def deleteCourse(course):
    try:
        courses.remove(course)
    except:
        pass

def removeCourse():
    ID = int(raw_input("ID of Course to be Deleted: "))
    for c in courses:
        if c.ID == ID:
            deleteCourse(c)
    return updateWeek(courses)

def addCourse():
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
    courses.append(src.Course(name,(days.split(",")), start, end, include, ID))

def updateWeek():
    # start with a blank week
    wk = src.Week()
    for course in courses:
        for meeting in course.meetings:
            for day in wk.days:
                if meeting == day.name:
                    # check times
                    for indx, time in enumerate(day.timeslots):
                        if indx >= (course.start - 9) * 2 and indx < (course.end - 9) * 2:
                            if type(time) is src.Course:
                                if time is course and course.include == True:
                                    pass
                                elif time is course and course.include == False:
                                    day.timeslots[indx] = None
                                elif course.include == True:
                                    day.timeslots[indx] = src.Conflict(time)
                                    day.timeslots[indx].competitors.append(course)
                                else:
                                    pass
                            elif type(time) is src.Conflict:
                                if course in time.competitors and course.include == True:
                                    pass
                                elif course in time.competitors and course.include == False:
                                    day.timeslots[indx].competitors.remove(course)
                                    if len(day.timeslots[indx].competitors) == 1:
                                        day.timeslots[indx] = day.timeslots[indx].competitors[0]
                                elif course.include == True:
                                    day.timeslots[indx].competitors.append(course)
                                else:
                                    pass
                            elif course.include == True:
                                day.timeslots[indx] = course
                            else:
                                pass
    return wk

def viewCourses():
    if len(courses) == 0:
        print("No Courses")
    else:
        for c in courses:
            print(c)

def include():
    courseID = int(raw_input("Input the ID of the course you want to include."))
    for c in courses:
        if c.ID == courseID:
            print("Including: " + c.name)
            c.include = True
    
def exclude():
    courseID = int(raw_input("Input the ID of the course you want to exclude."))
    for c in courses:
        if c.ID == courseID:
            c.include = False

def excludeAll():
    for c in courses:
        c.include = False
    return courses

# TODO: make header modular based on # of timeslots
def viewSchedule():
    print("| Day | 9:00 - 9:30 AM | 9:30 - 10:00 AM | 10:00 - 10:30 AM | 10:30 - 11:00 AM | 11:00 - 11:30 AM | 11:30 AM - 12:00 PM |" +
           " 12:00 - 12:30 PM | 12:30 - 1:00 PM | 1:00 - 1:30 PM | 1:30 - 2:00 PM | 2:00 - 2:30 PM | 2:30 PM - 3:00 PM | 3:00 PM - 3:30 PM |" +
           " 3:30 - 4:00 PM | 4:00 - 4:30 PM | 4:30 - 5:00 PM | 5:00 - 5:30 PM | 5:30 - 6:00 PM | 6:00 - 6:30 PM | 6:30 - 7:00 PM | 7:00 - 7:30 PM |" +
           " 7:30 - 8:00 PM | 8:00 PM - 8:30 PM | 8:30 - 9:00 PM |\n")
    print(updateWeek())

# for command-line interface
def editSInput():
    action = raw_input("| Include | Exclude | Replace | Clear | Back | Help |")
    if action == "Include":
        include()
    elif action == "Exclude":
        exclude()
    elif action == "Replace":
        exclude()
        include()
    elif action == "Clear Courses":
        answer = raw_input("Are you sure you want to clear the schedule? This change is irreversible. Y/N")
        if answer == "Y":
            print("Clearing...")
            waitForInput(excludeAll())
        elif answer == "N":
            editSInput()
        else:
            print("Did not understand input, returning to edit menu.")
            editSInput()
    elif action == "Back":
        waitForInput()
    elif action == "Help":
        help()
    else:
        print("Command not recognized, please try again")
        editSInput()
    waitForInput(updateWeek())

def editSchedule():
    print("|__ Current Schedule __|")
    viewSchedule()
    editSInput()

def weekToMarkdown():
    mkd = ("| Time | Monday | Tuesday | Wednesday | Thursday | Friday |\n" +
           ("|---" + ("|---" * 4) + "|---|\n"))
    return (mkd + str(updateWeek()))

def saveCoursesGUI(dfile, sfile):
    with open((dfile), 'wb') as f, open((sfile), 'w') as mkd:
        print("Saving data to " + dfile)
        dill.dump(courses, f)
        print("Saving schedule to " + sfile)
        mkd.write(weekToMarkdown())
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
        dill.dump(courses, f)
        print("Saving schedule to " + sfile + ".md")
        mkd.write(weekToMarkdown())
        f.close()
        mkd.close()

def loadCoursesGUI(filename):
    print(filename)
    try:
        with open(filename, 'rb') as f:
            f.seek(0)
            courses = dill.load(f)
    except:
        print("issue loading")
        courses = defaultCourses()

def loadCourses(filename = "data"):
    try:
        with open((filename+".obj"), 'rb') as f:
            f.seek(0)
            courses = dill.load(f)
    except:
        print("issue loading")
        courses = defaultCourses()

# for command-line interface
def waitForInput():
    action = raw_input("| Add Course | Remove Course | View Courses | View Schedule | Edit Schedule | Save | Quit | Help |\n")
    if action == "Add Course" or action == "Add" or action == "a":
        addCourse()
        waitForInput()
    elif action == "Remove Course" or action == "Remove" or action == "r":
        waitForInput(removeCourse())
    elif action == "View Courses" or action == "View C" or action == "vc":
        viewCourses()
        waitForInput()
    elif action == "Edit Courses" or action == "Edit C" or action == "ec":
        pass
    elif action == "View Schedule" or action == "View S" or action == "vs":
        viewSchedule()
        waitForInput()
    elif action == "Edit Schedule" or action == "Edit S" or action == "es":
        editSchedule()
        waitForInput()
    elif action == "Help" or action == "h":
        pass
    elif action == "Quit" or action == "q":
        print("Exiting...")
        saveCourses()
        quit()
    elif action == "Save" or action == "s":
        print("Saving...")
        try:
            saveCourses()
        except:
            print("Save unsuccessful")
            waitForInput()
        print("Save successful!")
        waitForInput()
    else:
        print("Command not recognized. Try again, or enter 'Help' for instructions.")
        waitForInput()

def main():
    loadCourses()
    if useGUI == True:
        openGUI()
    else:
        waitForInput()

if __name__ == "__main__":
    main()
