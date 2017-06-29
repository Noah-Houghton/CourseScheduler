# pages code adapted from https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# form code adapted from http://www.python-course.eu/tkinter_entry_widgets.php

import Tkinter as tk
import tkFont as tkfont
import tkMessageBox as tkm
import tkSimpleDialog as tksd
import main, subfile, settings
import courses as src
import random, string
import professors

class SchedulerAppGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, CoursePage, SchedulePage, EditCoursePage, AddCoursePage, ProfsPage, AddProfsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save", command=lambda: subfile.saveCoursesGUI(tksd.askstring("Saving Data", "Data File Name", initialvalue="data.obj"), tksd.askstring("Writing Markdown", "Markdown File Name", initialvalue="schedule.md")))
        filemenu.add_command(label="Load", command=lambda: self.loadCourses())
        filemenu.add_command(label="Reset to Default", command=lambda: self.confirmReset())
        debugmenu = tk.Menu(filemenu, tearoff=0)
        debugmenu.add_command(label="Random Session", command=lambda: self.confirmRandom())
        filemenu.add_cascade(label="Debug", menu = debugmenu)
        menubar.add_cascade(label="File", menu = filemenu)
        editmenu = tk.Menu(menubar, tearpff=0)
        editmenu.add_command(label="Undo", command=lambda: self.Undo())
        menubar.add_cascade(label="Edit", menu=filemenu)
        viewmenu = tk.Menu(menubar, tearoff=0)
        viewmenu.add_command(label="Home", command = lambda: self.show_frame("StartPage"))
        viewmenu.add_command(label="View Courses", command = lambda: self.show_frame("CoursePage"))
        viewmenu.add_command(label="View Schedule", command = lambda: self.show_frame("SchedulePage"))
        viewmenu.add_command(label="View Professors", command = lambda: self.show_frame("ProfsPage"))
        menubar.add_cascade(label = "View", menu=viewmenu)
        self.config(menu = menubar)

    def undo(self):
        subfile.undo()
        print("reloading -- currently this sets page to startpage")
        self.show_frame("StartPage")

    def confirmRandom(self):
        if tkm.askyesno("Verification", "Are you sure you want to make a random session?") == True:
            subfile.randomSession()
            print("reloading session")
            self.show_frame("StartPage")

    def confirmReset(self):
        if tkm.askyesno("Verification", "Are you sure you want to reset? It will wipe all data.") == True:
            subfile.default()
            print("reloading session")
            self.show_frame("StartPage")

    def loadCourses(self):
        subfile.loadCoursesGUI(tksd.askstring("Loading", "Data File Name", initialvalue="data.obj"))
        print("reloading page")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.updateAll()
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Courses",
                            command=lambda: controller.show_frame("CoursePage"))
        button2 = tk.Button(self, text="Go to Schedule",
                            command=lambda: controller.show_frame("SchedulePage"))
        button3 = tk.Button(self, text="Go to AddCourse", command=lambda: controller.show_frame("AddCoursePage"))
        button4 = tk.Button(self, text="Go to Professors", command=lambda: controller.show_frame("ProfsPage"))
        button1.pack()
        button2.pack()
        button3.pack()
        button4.pack()

        self.coursesTxt = tk.StringVar()
        self.coursesTxt.set(main.coursesToStr())
        self.scheduleTxt = tk.StringVar()
        self.scheduleTxt.set(main.scheduleToStr())

        m1 = tk.PanedWindow(self)
        m1.pack(fill=tk.BOTH, expand=1)

        left = tk.Label(m1, textvariable=self.coursesTxt)
        m1.add(left)

        m2 = tk.PanedWindow(m1, orient=tk.VERTICAL)
        m1.add(m2)

        right = tk.Label(m2, textvariable=self.scheduleTxt)
        m2.add(right)

    def updateCourses(self):
        self.coursesTxt.set(main.coursesToStr())

    def updateSchedule(self):
        self.scheduleTxt.set(main.scheduleToStr())

    def updateAll(self):
        self.updateCourses()
        self.updateSchedule()

class AddCoursePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the Add Course Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        #TODO: have a checkbox for include/exclude and meeting days
        fields = 'Course Name', 'Course ID', 'Course Meetings', 'Course Start Time', 'Course End Time', 'Course Q Score'
        self.ents = self.makeform(fields)
        self.bind('<Return>', (lambda event, e=self.ents: self.fetch(e)))   
        b1 = tk.Button(self, text='Add Course',
              command=(lambda e=self.ents: self.fetch(e)))
        b1.pack(side=tk.LEFT, padx=5, pady=5)
        b2 = tk.Button(self, text='Quit', command=lambda: self.quit(self.ents))
        b2.pack(side=tk.LEFT, padx=5, pady=5)
    
    def updateAll(self):
        pass

    def quit(self, entries):
        for entry in entries:
            entry[1].delete(0, tk.END)
        self.controller.show_frame("StartPage")

    def fetch(self, entries):
        fields = {}
        for entry in entries:
            fields[entry[0]] = entry[1].get()
        # try:
        subfile.addCourseGUI(src.Course(fields["Course Name"], fields["Course Meetings"].split(","), float(fields["Course Start Time"]), float(fields["Course End Time"]), True, int(fields["Course ID"]), float(fields["Course Q Score"])))
        self.quit(self.ents)
        # except Exception:
        #     print("Error adding course")

    def makeform(self, fields):
       entries = []
       for field in fields:
          row = tk.Frame(self)
          lab = tk.Label(row, width=15, text=field, anchor='w')
          ent = tk.Entry(row)
          row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
          lab.pack(side=tk.LEFT)
          ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
          entries.append((field, ent))
       return entries

class EditCoursePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the Edit Course Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        m1 = tk.PanedWindow(self)
        m1.pack(fill=tk.BOTH, expand=1)

    def updateAll(self):
        pass

class CoursePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the course page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        del_button = tk.Button(self, text="Delete Course", command=lambda: self.confirmDelete(int(tksd.askstring("delete", "ID of course to delete"))))
        del_button.pack()
        edit_button = tk.Button(self, text="Edit Course", command=lambda: controller.show_frame("EditCoursePage"))
        edit_button.pack()
        add_button = tk.Button(self, text="Add Course", command=lambda: controller.show_frame("AddCoursePage"))
        add_button.pack()
        m1 = tk.PanedWindow(self)
        m1.pack(fill=tk.BOTH, expand=1)
        self.coursesTxt = tk.StringVar()
        self.coursesTxt.set(main.coursesToStr())
        display = tk.Label(m1, textvariable = self.coursesTxt)
        m1.add(display)

    def confirmDelete(self, ID):
        if tkm.askyesno("del_conf", "Are you sure you want to delete this course? If you do, it cannot be undone (yet).") == True:
            for c in settings.courses:
                if c.ID == ID:
                    subfile.deleteCourse(c)

    def updateCourses(self):
        self.coursesTxt.set(main.coursesToStr())

    def updateAll(self):
        self.updateCourses()

class EditProfsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the Edit Profs Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        m1 = tk.PanedWindow(self)
        m1.pack(fill=tk.BOTH, expand=1)

    def updateAll(self):
        pass

class ProfsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the Profs page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        del_button = tk.Button(self, text="Delete Professor", command=lambda: self.confirmDelete(tksd.askstring("delete", "Name of Prof to delete")))
        del_button.pack()
        edit_button = tk.Button(self, text="Edit Professor", command=lambda: controller.show_frame("EditProfPage"))
        edit_button.pack()
        add_button = tk.Button(self, text="Add Professor", command=lambda: controller.show_frame("AddProfsPage"))
        add_button.pack()
        m1 = tk.PanedWindow(self)
        m1.pack(fill=tk.BOTH, expand=1)
        self.profsTxt = tk.StringVar()
        self.profsTxt.set(main.profsToStr())
        display = tk.Label(m1, textvariable = self.profsTxt)
        m1.add(display)

    def confirmDelete(self, name):
        if tkm.askyesno("del_conf", "Are you sure you want to delete this Professor? If you do, it cannot be undone (yet).") == True:
            for p in settings.professors:
                if p.name == name:
                    subfile.deleteProfGUI(p)
        self.show_frame("ProfsPage")

    def updateProfs(self):
        self.profsTxt.set(main.profsToStr())

    def updateAll(self):
        self.updateProfs()

class AddProfsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the Add Profs Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        #TODO: have a checkbox for include/exclude and meeting days
        fields = 'Professor Name', 'Q Score', 'Department', 'Courses Taught'
        self.ents = self.makeform(fields)
        self.bind('<Return>', (lambda event, e=self.ents: self.fetch(e)))   
        b1 = tk.Button(self, text='Add Course',
              command=(lambda e=self.ents: self.fetch(e)))
        b1.pack(side=tk.LEFT, padx=5, pady=5)
        b2 = tk.Button(self, text='Quit', command=lambda: self.quit(self.ents))
        b2.pack(side=tk.LEFT, padx=5, pady=5)
    
    def updateAll(self):
        pass

    def quit(self, entries):
        for entry in entries:
            entry[1].delete(0, tk.END)
        self.controller.show_frame("StartPage")

    def fetch(self, entries):
        fields = {}
        for entry in entries:
            fields[entry[0]] = entry[1].get()
        # try:
        ids = []
        for i in fields["Courses Taught"].split(","):
            ids.append(int(i))
        
        courses = []
        for i in ids:
            for c in settings.courses:
                if c.ID == i:
                    courses.append(c)

        subfile.addProfGUI(professors.Professor(fields["Professor Name"], int(fields["Q Score"]), fields["Department"], courses))
        self.quit(self.ents)

    def makeform(self, fields):
       entries = []
       for field in fields:
          row = tk.Frame(self)
          lab = tk.Label(row, width=15, text=field, anchor='w')
          ent = tk.Entry(row)
          row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
          lab.pack(side=tk.LEFT)
          ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
          entries.append((field, ent))
       return entries

class SchedulePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the Schedule Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        m1 = tk.PanedWindow(self)
        m1.pack(fill=tk.BOTH, expand=1)
        self.schedTxt = tk.StringVar()
        self.schedTxt.set(main.scheduleToStr())
        display = tk.Label(m1, textvariable = self.schedTxt)
        m1.add(display)

    def updateSchedule(self):
        self.schedTxt.set(main.scheduleToStr())

    def updateAll(self):
        self.updateSchedule()

if __name__ == "___":
    app = SchedulerAppGUI()
    app.mainloop()
