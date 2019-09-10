from tkinter import *
import stud_hw
import mysql.connector
import webbrowser
from quiz_ import CompleteQuiz
from Student_settings import Student_Setting
from progress_page import StudentProgress
#import login_page
from tkinter import ttk
from ttkthemes import themed_tk as tk


class student():

    def __init__(self,name):
        #w.destroy()
        self.width= 0
        self.name= name
        connection=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        cur= connection.cursor()
        cur.execute("SELECT code FROM gclass WHERE name=%s",(self.name,))
        row=cur.fetchall()
        connection.close()
        self.user= row[0][0]

    def StudentPage(self):
        window= tk.ThemedTk()
        for letter in range(len(self.name)):
            self.width+=20
        self.width+=600
        dimensions= str(self.width)+"x100"
        window.geometry(dimensions)
        
        window.get_themes()
        window.wm_title(self.name.title())
        window.set_theme("radiance")

        menubar = Menu(window)
        window.config(menu=menubar)

        #self.add_menu(window,"Log Out", commands = [("Log Out",self.LogOut(window),True)])


        title_frame=ttk.Frame(window)
        title_frame.grid(row=0,column=0,columnspan=4)

        main_frame=ttk.Frame(window)
        main_frame.grid(row=2,column=0,rowspan=6,columnspan=4)

        title= ttk.Label(title_frame,text="Welcome back " + self.name)# Add personalized welcome by passing as paramter list_of_lists[1](in login_page.py)
        title.grid(row=0,column=2,padx=65)
        title.config(font=("Courier",35))

        services= ttk.Combobox(main_frame,width=60)
        services["values"]= ("__________","Do Homework","Do Quiz","Progress","Mysfc","Update Phone Number","Update Email Address")
        services.grid(row=0,column=3,pady=5,padx=15)
        services.config(justify=CENTER)
        
        go=ttk.Button(main_frame,text="Go",width=5,command=lambda:self.go(services,window)).grid(row=0,column=4)
    
        window.mainloop()

    def go(self,cbox,win):
        print(cbox.get())
        if cbox.get()=="Do Homework":
            see_hw= stud_hw.See_Homework(win)
            see_hw.See_hw(self.user)
        elif cbox.get()== "Do Quiz":
            revise= CompleteQuiz(self.name)
            revise.ChooseQuiz(win)
        elif cbox.get()== "Progress":
            s_progress= StudentProgress(self.user,win)
            s_progress.MainPage()
        elif cbox.get()== "Mysfc":
             webbrowser.open_new_tab("mysfc.stokesfc.ac.uk/")
        elif cbox.get()== "Update Phone Number":
            student_changes= Student_Setting(self.user)
            student_changes.Enter_New_Number(win)
        elif cbox.get()== "Update Email Address":
            student_changes= Student_Setting(self.user)
            student_changes.Change_Email(win)
"""
    def add_menu(self,window_name,menuname, commands):
        menubar = Menu(window_name)
        window_name.config(menu=menubar)
        menu = Menu(menubar, tearoff = 0)

        for command in commands:
            menu.add_command(label = command[0], command = command[1])
            if command[2]:
                menu.add_separator()

        menubar.add_cascade(label=menuname, menu=menu)

    def LogOut(self,page):
        log=login_page.Starting()
        log.login(page)

 """       




#stud= student("Joseph")
#stud.StudentPage()
#Back button
