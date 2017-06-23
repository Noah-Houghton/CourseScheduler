import courses as src
import ast
import pickle as dill

def help():
	with open("help.txt", r) as help:
		print(help)

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
    ID = int(raw_input("ID of Course to be Deleted: "))
    for c in courses:
        if c.ID == ID:
            deleteCourse(c, courses)
        return updateWeek(courses)

def addCourse(courses):
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

def updateWeek(courses):
    # start with a blank week
    wk = src.Week()
    for course in courses:
        if course.include:
            for meeting in course.meetings:
                for day in wk.days:
                    if meeting == day.name:
                        # check times
                        for indx, time in enumerate(day.timeslots):
                            if indx >= (course.start - 9) * 2 and indx < (course.end - 9) * 2:
                                if type(time) is src.Course:
                                    if time is course:
                                        pass
                                    else:
                                        day.timeslots[indx] = src.Conflict(time)
                                        day.timeslots[indx].competitors.append(course)
                                elif type(time) is src.Conflict:
                                    if course in time.competitors:
                                        pass
                                    else:
                                        day.timeslots[indx].competitors.append(course)
                                else:
                                    day.timeslots[indx] = course
    return wk

def viewCourses(courses):
    for c in courses:
        print(c)

def include(course):
	course.include = True
	
def exclude(course):
	course.include = False
	
# TODO: make header modular based on # of timeslots
def viewSchedule(week, courses):
    print("| Day | 9:00 - 9:30 AM | 9:30 - 10:00 AM | 10:00 - 10:30 AM | 10:30 - 11:00 AM | 11:00 - 11:30 AM | 11:30 AM - 12:00 PM |" +
	       " 12:00 - 12:30 PM | 12:30 - 1:00 PM | 1:00 - 1:30 PM | 1:30 - 2:00 PM | 2:00 - 2:30 PM | 2:30 PM - 3:00 PM | 3:00 PM - 3:30 PM |" +
	       " 3:30 - 4:00 PM | 4:00 - 4:30 PM | 4:30 - 5:00 PM | 5:00 - 5:30 PM | 5:30 - 6:00 PM | 6:00 - 6:30 PM | 6:30 - 7:00 PM | 7:00 - 7:30 PM |" +
	       " 7:30 - 8:00 PM | 8:00 PM - 8:30 PM | 8:30 - 9:00 PM |\n")
    print(updateWeek(courses))

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
			waitForInput(courses, src.Week())
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
    waitForInput(courses, updateWeek(courses))

def editSchedule(week, courses):
	print("|__ Current Schedule __|")
	viewSchedule(week, courses)
	editSInput(week, courses)

def weekToMarkdown(week, courses):
	mkd = ("| Day | 9:00 - 9:30 AM | 9:30 - 10:00 AM | 10:00 - 10:30 AM | 10:30 - 11:00 AM | 11:00 - 11:30 AM | 11:30 AM - 12:00 PM |" +
	       " 12:00 - 12:30 PM | 12:30 - 1:00 PM | 1:00 - 1:30 PM | 1:30 - 2:00 PM | 2:00 - 2:30 PM | 2:30 - 3:00 PM | 3:00 - 3:30 PM |" +
	       " 3:30 - 4:00 PM | 4:00 - 4:30 PM | 4:30 - 5:00 PM | 5:00 - 5:30 PM | 5:30 - 6:00 PM | 6:00 - 6:30 PM | 6:30 - 7:00 PM | 7:00 - 7:30 PM |" +
	       " 7:30 - 8:00 PM | 8:00 - 8:30 PM | 8:30 - 9:00 PM |\n" +
           ("|---" + ("|---" * 23) + "|---|\n"))
	return (mkd + str(week))
	
# saveCourses(current_week, all_courses)
def saveCourses(courses, week):
	dfile = raw_input("Name of data file? For default leave blank.")
	if dfile == "":
		dfile = "data"
	sfile = raw_input("Name of schedule file? For default leave blank.")
	if sfile == "":
		sfile = "schedule"
	with open((dfile+".obj"), 'wb') as f, open((sfile+".md"), 'w') as mkd:
		print("Saving data to " + dfile + ".obj")
		dill.dump(courses, f)
		print("Saving schedule to " + sfile + ".md")
		mkd.write(weekToMarkdown(updateWeek(courses), courses))
		f.close()
		mkd.close()
    	
# returns (week, all_courses)
def loadCourses(filename = "data"):
	with open((filename+".obj"), 'rb') as f:
		f.seek(0)
		courses = dill.load(f)
		return courses

def waitForInput(courses, week):
	action = raw_input("| Add Course | Remove Course | View Courses | View Schedule | Edit Schedule | Save | Quit | Help |\n")
	if action == "Add Course" or action == "Add" or action == "a":
		addCourse(courses)
		waitForInput(courses, week)
	elif action == "Remove Course" or action == "Remove" or action == "r":
		waitForInput(courses, removeCourse(courses))
	elif action == "View Courses" or action == "View C" or action == "vc":
		viewCourses(courses)
		waitForInput(courses, week)
	elif action == "Edit Courses" or action == "Edit C" or action == "ec":
		pass
	elif action == "View Schedule" or action == "View S" or action == "vs":
		viewSchedule(week, courses)
		waitForInput(courses, week)
	elif action == "Edit Schedule" or action == "Edit S" or action == "es":
		editSchedule(week, courses)
		waitForInput(courses, week)
	elif action == "Help" or action == "h":
		pass
	elif action == "Quit" or action == "q":
		print("Exiting...")
		saveCourses(courses, week)
		quit()
	elif action == "Save" or action == "s":
		print("Saving...")
		try:
			saveCourses(courses, week)
		except:
			print("Save unsuccessful")
			waitForInput(courses, week)
		print("Save successful!")
		waitForInput(courses, week)
	else:
		print("Command not recognized. Try again, or enter 'Help' for instructions.")
		waitForInput(courses, week)

def main():
    week = src.Week()
    try:
		courses = loadCourses()
    except:
		courses = []
		print("No save found, blank save created...")
    waitForInput(courses, week)

if __name__ == "__main__":
    main()
