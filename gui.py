# code adapted from https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
import Tkinter as tk     # python 2
import tkFont as tkfont  # python 2
import tkMessageBox as tkm
import tkSimpleDialog as tksd
import main
import courses as src
import random, string

courses = main.getCourses()

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
        for F in (StartPage, CoursePage, SchedulePage, EditCoursePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

        menubar = tk.Menu(self)
        viewmenu = tk.Menu(menubar, tearoff=0)
        viewmenu.add_command(label="View Courses", command = lambda: self.show_frame("CoursePage"))
        viewmenu.add_command(label="View Schedule", command = lambda: self.show_frame("SchedulePage"))
        menubar.add_cascade(label = "View", menu=viewmenu)
        self.config(menu = menubar)

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

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("CoursePage"))
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("SchedulePage"))
        update_button = tk.Button(self, text="update page", command = lambda: self.updateAll)
        button1.pack()
        button2.pack()

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
        self.coursesTxt.set(main.scheduleToStr())

    def updateAll(self):
        self.updateCourses()
        self.updateSchedule()

class AddCoursePage(tk.Frame):
    pass

class EditCoursePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the Edit Course Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

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
        del_button = tk.Button(self, text="Delete Course", command=lambda: self.confirmDelete(tksd.askstring("delete", "ID of course to delete")))
        del_button.pack()
        edit_button = tk.Button(self, text="Edit Course", command=lambda: controller.show_frame("EditCoursePage"))
        edit_button.pack()

    def confirmDelete(self, ID):
        if tkm.askyesno("del_conf", "Are you sure you want to delete this course? If you do, it cannot be undone (yet).") == True:
            for c in courses:
                if c.ID == ID:
                    courses.remove(c)

    def updateAll(self):
        pass

class SchedulePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the Schedule Page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
    def updateAll(self):
        pass

if __name__ == "__main__":
    # week = src.Week()
    # try:
    #     courses = loadCourses()
    # except:
    #     courses = []
    #     print("No save found, blank schedule created...")
    # main.addCourse(courses)
    app = SchedulerAppGUI()
    app.mainloop()