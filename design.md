# Course Scheduler Program Design

## Overview
The Course Scheduler is a web-based app which uses Python and SQL to manage a student's prospective course schedule. The app allows students to visualize courses, notifies the user if courses will conflict, and provides data on credit allocation and meeting requirements.

## Backend
The backend is written in Python. It must handle requests for all loaded courses, the courses which a student has included in their schedule, the chosen course of study and corresponding requirements, and information about the professors who teach those courses.

### courses.db
* Name
* Course ID
* abbreviation
* description
* Professor ID
* isSection
* isSeminar
* department
* number of credits
* credit type
* Q Score

### courses.py
Provides methods for adding, deleting, and editing courses in courses.db.

### professors.db
* Name
* Professor ID
* department
* Q Score

### professors.py
Provides methods for adding, deleting, and editing professors in professors.db.

### concentrations.db

### secondaries.db

### languages.db

### students.db
