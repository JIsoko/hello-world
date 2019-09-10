from tkinter import *
import mysql.connector
import matplotlib
matplotlib.use("TkAgg")
from pandas import DataFrame #TO deal with tables and data
from collections import Counter# To remove redunancy in lists and find most common element
from matplotlib import * #FOr plotting
from matplotlib import style 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk #To bind canvas to interface and to create navigation toolbar
from matplotlib.figure import Figure
from tkinter import ttk
from ttkthemes import themed_tk as tk
import quiz_
import Student_settings
import stud_hw
import webbrowser #To open websites

 
"""
Teacher here will be able to visualise progress as a class, answers students got correctly and which not
Also by clicking to a listbox with studen names,he will be able to see the students progress page

Need to database for individual result and algo to show class progress (stack each result on each quiz)
"""


class StudentProgress():

    def __init__(self,userID,GUI):
        GUI.destroy()
        self.userID=userID
        self.list_of_lists=[] #Will hold all data from progress
        conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        cur=conn.cursor()
        cur.execute("SELECT name,meg FROM gclass WHERE code=%s",(self.userID,))# Names and target grades are fetched from the db
        self.rows=cur.fetchall()
        conn.commit()
        conn.close()
        
        grade_system={"A*":80,"A":70,"B":60,"C":50,"D":40,"E":30} #Dictionary giving a value to specific target grades
        self.target= grade_system[self.rows[0][1]]

    #Populates tree with records
    def FillTree(self,treeview):
        conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        cur=conn.cursor()
        cur.execute("SELECT * FROM progress WHERE code=%s",(self.userID,))#Fetches all data from progress table
        rows=cur.fetchall()
        conn.commit()
        conn.close()
        for tuple in range(len(rows)):
            self.list_of_lists.append(list(rows[tuple])) #Tuples from the db are turned into lists
            index=0
        for element in range(len(self.list_of_lists)):
            index+=1 
            tag= " "+ str(index) #Record tag needed to individualise and assign specific colours
            treeview.insert("","end",text=index,values= (self.list_of_lists[element][3],self.list_of_lists[element][2],self.list_of_lists[element][4]),tags=(tag,))
            if self.list_of_lists[element][2]>self.target: #Checks if quiz result is above target grade
                print("Above target")
                treeview.tag_configure(tag,background= "#CD69C9")# Record is shown in Purple
            elif self.target== self.list_of_lists[element][2]: #Checks if quiz result is equal target grade
                print("On target")
                treeview.tag_configure(tag,background= "#006400")# Record is shown in green
            elif self.target- self.list_of_lists[element][2] <= 5:#Checks if quiz result is below target grade by 5
                print("Just slightly below")
                treeview.tag_configure(tag,background= "#FF8C00")# Record is shown in Amber/Yellowish
            else:
                print("Below target")
                treeview.tag_configure(tag,background= "#FF0000") #Record is shown in red

    def MainPage(self):
        win= tk.ThemedTk() #Window created
        self.win= win
        self.win.wm_title("Progress: "+self.rows[0][0].title()) #Title of window with student name
        self.win.geometry("900x550") #Sizing of window

        self.win.get_themes()
        self.win.set_theme("radiance")

        #Styling the treeview
        tree_style = ttk.Style()
        tree_style.configure("mystyle.Treeview", highlightthickness=1, bd=1, font=('Calibri', 12)) # 
        tree_style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) 

        #Treeview with score and quiz title and worst topic
        tree= ttk.Treeview(self.win,columns=("Index","Quiz","Score","Worst Topic"),style="mystyle.Treeview")
        tree.pack(side=LEFT,fill=Y)
        tree.heading('#0', text='Index')
        tree.heading('#1', text='Quiz')
        tree.heading('#2', text='Score')
        tree.heading('#3', text='Worst Topic')
        tree.column("#0",width=50)
        tree.column("#1",width=150)
        tree.column("#2",width=46)
        tree.column("#3",width=150)
        tree.column('#4',width=0)

        #Scrollbar placed on side of tree
        vertical_sb = ttk.Scrollbar(self.win, orient="vertical", command=tree.yview)
        vertical_sb.pack(side=LEFT)
        tree.configure(yscrollcommand=vertical_sb.set) #Binding tree to scrollbar

        style.use("ggplot") #Style of graph plot

        self.FillTree(tree)

        #Menubar linking to other pages
        self.add_menu(self.win,"Navigate", commands = [("Quiz", self.Quiz_Page, True), ("Homework", self.Homework, True),("MySFC", self.MYSFC, True),("Update Phone Number",self.Change_Phone,True),("Update Email Address",self.Change_Email,True)])#,("Log Out",self.LogOut(self.win),True)])

        print(self.list_of_lists)
        quiz_name=[]
        #Storing all quiz titles mentioned in the db
        for score in range(len(self.list_of_lists)):
            quiz_name.append(self.list_of_lists[score][3])

        
        count = Counter(quiz_name)
        names_quizzes=list(count) #List of individual quiz names (not one repeated) which student completed
        print(names_quizzes)
        data_=[]
        # Finds average of the student on a specific quiz
        for n in range(len(names_quizzes)):
            score=0 #TO find the sum of the collective scores 
            checker=0 #TO know how many to divide against
            for l in range(len(self.list_of_lists)):
                if names_quizzes[n]== self.list_of_lists[l][3]:
                    #print(self.h[l][3])
                    score+=self.list_of_lists[l][2]
                    checker+=1
            data_.append(int(score/checker))
        print(data_)

        #Student's target grade
        meg_data=[]
        for element in range(len(names_quizzes)): #MEG is plotted for the same x-axis as the scores
            meg_data.append(self.target) 
        print(meg_data)

        #Preparing the data for the plotting
        data= {"Quiz":names_quizzes, #xaxis
               "Score":data_ } #yaxis
        
        df1= DataFrame(data,columns=["Quiz","Score"])
        df1= df1[["Quiz","Score"]].groupby("Quiz").sum() #Grouped by quiz name
        
        data2= {"Quiz":names_quizzes,
                "MEG":meg_data}

        df2= DataFrame(data2,columns=["Quiz","MEG"])
        df2= df2[["Quiz","MEG"]].groupby("Quiz").sum() #Grouped by quiz name

        f= Figure(figsize=(6,5),dpi=100)
        a= f.add_subplot(111)
        bar1 = FigureCanvasTkAgg(f, self.win) #Canvas graph attached to tkinter interface

        #navigation toolbar which is below the graph
        toolbar= NavigationToolbar2Tk(bar1,self.win)
        toolbar.update()
        bar1._tkcanvas.pack(anchor= NE)

        bar1.get_tk_widget().pack(anchor=N,expand=True)
        df1.plot(kind="bar",legend=True,ax= a,color="b") #Quiz Results are plotted as bar chart
        df2.plot(kind="line",legend=True,ax=a,color="r") # Student target grade plotted on same canvas as a red line

        self.win.mainloop()

    #Creates menubar
    def add_menu(self,window_name,menuname, commands):
        menubar = Menu(window_name)
        window_name.config(menu=menubar)
        menu = Menu(menubar, tearoff = 0)

        for command in commands:
            menu.add_command(label = command[0], command = command[1])
            if command[2]:
                menu.add_separator()

        menubar.add_cascade(label=menuname, menu=menu)

    #Opens college website
    def MYSFC(self):
        webbrowser.open_new_tab("mysfc.stokesfc.ac.uk/")
    #Opens quiz page
    def Quiz_Page(self):
        quiz= quiz_.CompleteQuiz(self.rows[0][0])
        quiz.ChooseQuiz(self.win)
    #Opens homework section
    def Homework(self):
        see_hw= stud_hw.See_Homework(self.win)
        see_hw.See_hw(self.userID)
    #Opens email modification page
    def Change_Email(self):
        student_changes= Student_settings.Student_Setting(self.userID)
        student_changes.Change_Email(self.win)
    #Opens phone number modification page
    def Change_Phone(self):
        student_changes= Student_settings.Student_Setting(self.userID)
        student_changes.Enter_New_Number(self.win)