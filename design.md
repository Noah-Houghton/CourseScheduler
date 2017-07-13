# Application Design

## Database
The Database class holds all session-wide information; all data which is not associated with another class is held by this class. This class also holds a temporary list of deleted objects which is cleared on restart, and tracks a number of the user's last actions for undoing purposes.
### Internal Data
The Database has no data which must be restricted to its own scope.

### Outward Facing Data
* courses {} -> Dict of {"courseID" : Course}
* professors {} -> Dict of {"ProfessorID" : Professor}
* deletedCourses {} -> Dict of {"courseID" : Course}
* deletedProfs {} -> Dict of {"ProfessorID" : Professor}
* lastAction -> type String

### Functions
The Database does not contain functions; accessing the database is the role of subfile.py. Those functions are:

* allCourses() -> returns the current list of all courses in database.courses
* addCourse(course, prof (optional)) -> adds 'course' to database.courses, checking for duplicates. If prof is given, attempts to run assignProf(course, prof)
* getCourse(ID) -> returns a specific course whose ID matches 'ID'. If no match is found, returns None
* deleteCourse(ID) -> accesses database.courses and deletes any course whose ID matches 'ID'. also accesses database.professors and removes 'course' from any prof whose .courses contains 'course'
* editCourse(course, field, value) -> accesses every course in database.courses which is 'course' and sets course.'field' = 'value'
* assignProf(course, Professor) -> adds 'course' to Professor.courses

* allProfs() -> returns the current list of all professors in database.professors
* addProf(professor) -> adds 'professor' to database.professors, checking for duplicates
* getProf(name) -> returns a specific professors whose name matches 'name'. If no match is found, returns None
* deleteProf(name) -> accesses database.professors and deletes any professors whose name matches 'name'. also accesses database.courses and deletes any professor in courses.professors matching 'name' from any list which contains it
* editProf(Professor, field, value) -> accesses every professor in database.professors which is 'Professor' and sets Professor.'field' = 'value'

### Subclasses
The Database is not extended by any class.

## Student
The Student class holds the data which is specific to the student -- which courses are being taken, which requirements are filled or unfilled, and what the Course of Study is -- which determines requirements. A student can have a Concentration or a Joint-Concentration or a Special Concentration, along with a Secondary and/or a Language Citation.

### Internal Data
#### These fields are to track how many are needed, not how many the student has completed. That is dynamically calculated every time the user views their Progress
* genEds {"Req" : # req} -> reqs is a static dict which represents the number of General Education courses required in fields with the "Req" tag
* conc ({"Req" : # req}, {"Req" : # req} -> JConc is a mostly static dict which represents the number of concentration-specific courses required in fields with the "Req" tag. This field can only be edited by the changeConc() method. Non-joint concentrations are represented by (some, none). In Joint Concentrations, the primary concentration is the first element in the tuple.
* sndary {"Req" : # req} -> sndary tracks secondary requirements
* lngCit {"Req" : # req} -> lngCit tracks language citation requirements

### Outward Facing Data
* name -> string, reflects student's name
* student_id -> int, reflects student's university ID
* semesters_left -> int, reflects how many semesters the student has left at school out of a standard 8 semesters
* courses_taken -> list of courses that the student has already completed
* courses_current -> list of courses currently in student's schedule

### Functions
Student fields can be accessed directly as necessary in other functions, therefore no Student functions are necessary.

### Subclasses
Student is not extended by any class.

## CourseOfStudy
This file holds all pre-defined Fields of Study as well as functions for adding, removing, or editing them.

### Internal Data
No internal-only data, as this is a repository of dicts for easy access.

### Outward Facing Data
* concentrations -> Dict of Dict {"CS" : {//dict for CS requirements}}
* secondaries -> Dict of Dict {"CS" : {//dict for CS secondary}}
* langs -> Dict of Dict {"FR" : {//dict for FR citation}}

### Functions
changeConc(student, CID) -> changes 'student'.conc to concentrations["CID"]
changeSec(student, SID) -> changes 'student'.sndary to secondaries["SID"]
changeLng(student, LID) -> changes 'student'.lngCit to langs["LID"]

clearConc(student) -> changes 'student'.conc to concentrations["NONE"]
clearSec(student) -> changes 'student'.sndary to secondaries["NONE"]
clearLng(student) -> changes 'student'.lngCit to langs["NONE"]

### Subclasses
CourseOfStudy is not extended by any classes.

## Courses
This file holds functions which create and edit. Courses can be lectures, lectures with section, or seminars.

### Internal Data
* name -> string
* ID -> int
* desc -> string
* timeS -> float
* timeE -> float

###Outward Facing Data

###Functions

###Subclasses

##Professors

###Internal Data

###Outward Facing Data

###Functions

###Subclasses

##Day

###Internal Data

###Outward Facing Data

###Functions

###Subclasses

##Week

###Internal Data

###Outward Facing Data

###Functions

###Subclasses

