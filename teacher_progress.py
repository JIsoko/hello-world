"""
Teacher can see individual student progress and class progress
"""

from tkinter import *
import mysql.connector
import matplotlib
matplotlib.use("TkAgg")
from pandas import DataFrame
from matplotlib import *
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
#from matplotlib import style
from tkinter import ttk
from collections import Counter
#import login_page
import matplotlib.pyplot as plt
import Set_hw 
import Teacher
import History
import set_revision
from ttkthemes import themed_tk as tk

 
"""
Teacher here will be able to visualise progress as a class, answers students got correctly and which not
Also by clicking to a listbox with studen names,he will be able to see the students progress page

Need to database for individual result and algo to show class progress (stack each result on each quiz)
"""


class TeacherProgress():

    def __init__(self,GUI):
        GUI.destroy()
        self.list_of_lists=[]
        self.Average_score=[]
        self.userIDs=[] #Will hold all user ids within the progress table
        self.avg_worstopic=[]
        self.name_meg=[]
        self.bad_topics=[]
        self.name_of_quizzes=[]

        conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        cur=conn.cursor()
        cur.execute("SELECT * FROM progress") #Fetches all data from progress table
        self.h=cur.fetchall()
        conn.close()
        for n in range(len(self.h)):
            self.userIDs.append(self.h[n][1]) #User IDs inserted into list
            self.name_of_quizzes.append(self.h[n][3]) #Quiz titles inserted in list
        count = Counter(self.userIDs) #Redundancy within user id list removed so each element is unique
        users=list(count) 
        for userId in range(len(users)): #Iterating each student
            score=0 #Used in holding total score per student
            checker=0 #Used to know by how many to divide to find average
            for n in range(len(self.h)): 
                if self.h[n][1]== users[userId]: #self.h[n][1] is user id of a student
                    checker+=1
                    score+=self.h[n][2] #Adding up score from each student (self.h[n][2] holds score)
            avg_score=int(score/checker) #Student's average
            self.Average_score.append([users[userId],avg_score])

        for usercode in range(len(users)):
            worstopic=[]
            for element in range(len(self.h)):
                if self.h[element][1]== users[usercode]:
                    worstopic.append(self.h[element][-1]) #Inserting all worst topics into list
            count = Counter(worstopic) #Removing redundancy within list
            topics=list(count) 
            max_cnt = max(topics) #Highest number of counts of an element
            total=0
            for element in range(0,len(topics)):
                if topics[element]==max_cnt: #Looking for topic with most counts
                    total+=1
            most_common = count.most_common(total) 
            self.most_common=most_common
            for topic in range(0,len(self.most_common)):
                topic_to_work=most_common[topic][0]
                if len(self.most_common)> 1:#Most common worst topics, in case there are 2 of equal frequency in lit
                    worsttopic= topic_to_work+","
                else:
                    worsttopic=topic_to_work #Most common worst topic
            self.avg_worstopic.append([users[usercode],worsttopic])
            self.bad_topics.append(self.most_common[0][0])

            conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
            cur=conn.cursor()
            cur.execute("SELECT code,name,meg FROM gclass WHERE code=%s",(users[usercode],)) #Fetching user ids, names and target grades from db
            rows=cur.fetchall()
            conn.close()
            self.name_meg.append(list(rows[0]))
        
        #Grade system 
        self.grade_system={"A*":80,"A":70,"B":60,"C":50,"D":40,"E":30}

    #Class record in tree is filled
    def FillTreeClass(self,treeview):
        average_of_average=0
        #Class average is found by adding all students' average and finding the mean
        for element in range(len(self.Average_score)):
            average_of_average+=self.Average_score[element][1]
        average_of_average= int(average_of_average/len(self.Average_score))

        #Finding the worst topic as a class
        count = Counter(self.bad_topics)
        topics=list(count)
        max_cnt = max(topics)
        total=0
        for element in range(0,len(topics)):
            if topics[element]==max_cnt: #Checking if specific topic has the highest frequency in the list
                total+=1
        most_common = count.most_common(total)
        worst_of_worst= most_common[0][0]

        tag= "Class" 
        treeview.insert("","end",text="Class",values= (" ",average_of_average,worst_of_worst),tags=(tag,)) #Class' average and worst topic are inserted in treeview
        #Gives the record a golden colour
        treeview.tag_configure(tag,background= "#F2A343")

        

    #Fills treeview of student records
    def FillTree(self,treeview):
        for element in range(len(self.name_meg)): #Iterating through the number of students
            tag= " "+ str(self.name_meg[element][0])
            #Inserting name,meg,average and worst topic (in this order)
            treeview.insert("","end",text=self.name_meg[element][1],values= (self.name_meg[element][2],self.Average_score[element][1],self.avg_worstopic[element][1]),tags=(tag,))

            target= self.grade_system[self.name_meg[element][2]]
            if self.Average_score[element][1]>target:
                treeview.tag_configure(tag,background= "#CD69C9")#  if student's average is above target grade, record is shown in purple
            elif target== self.Average_score[element][1]:
                treeview.tag_configure(tag,background= "#006400")#  if student's average is equal target grade, record is shown in green
            elif target- self.Average_score[element][1] <= 5:
                treeview.tag_configure(tag,background= "#FF8C00")#  if student's average is slightly below target grade, record is shown in amber/yellow
            else:
                treeview.tag_configure(tag,background= "#FF0000")#  if student's average is below target grade, record is shown in red

    def LoadStudentProgress(self,name_selected):
        for c in range(len(self.name_meg)):
            print(self.name_meg[c],name_selected)
            if self.name_meg[c][1]== name_selected:
                userID= self.name_meg[c][0]
                conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
                cur=conn.cursor()
                cur.execute("SELECT * FROM progress WHERE code=%s",(userID,))
                self.info=cur.fetchall()
                conn.commit()
                conn.close()
                print(self.info,"Info")

                
                meg_data=[]
                count = Counter(self.name_of_quizzes)
                names_quizzes=list(count)
                print(names_quizzes)
                data_=[]
                x_axis=[]
                # Add up scores of specific quiz and append to list that will be plotted
                for n in range(len(names_quizzes)):
                    score=0
                    checker=0
                    within= False
                    for l in range(len(self.info)):
                        if names_quizzes[n]== self.info[l][3]:
                            within=True
                            print(self.info[l][2])
                            score+=self.info[l][2]
                            print("Score",score)
                            checker+=1
                            print(checker)
                    if score==0 and within==True:
                        data_.append(0)
                        x_axis.append(str(names_quizzes[n]))
                    elif score!=0 and checker!=0:
                        data_.append(int(score/checker))
                        x_axis.append(names_quizzes[n])
                print(data_,x_axis,"Final")
                
                for score in range(len(data_)):
                    meg_data.append(self.grade_system[self.name_meg[c][2]])#
                    #print(score_data,index_data,meg_data)

                plt.bar(x_axis, data_, color='b', linewidth=2,label='Quiz Score')
                plt.plot(x_axis,meg_data,color="r",dashes=[30, 5, 10, 5],label='MEG')
                plt.title("Progress: "+ name_selected, fontsize=18)
                plt.xlabel('Quizzes', fontsize=14)
                plt.ylabel('Score %', fontsize=14)
                plt.grid(True)
                plt.legend(loc='lower right')

                plt.show()
                


    def MainPage(self):
        win= tk.ThemedTk()
        self.win= win
        self.win.wm_title("Overall Progress")
        self.win.geometry("900x550")

        self.win.get_themes()
        self.win.set_theme("radiance")


        #Treeview with score and quiz title and worst topic

        tree_style = ttk.Style()
        tree_style.configure("mystyle.Treeview", highlightthickness=1, bd=1, font=('Calibri', 12)) # Modify the font of the body
        tree_style.configure("mystyle.Treeview.Heading", font=('Calibri', 14,'bold'))

        tree= ttk.Treeview(self.win,columns=("Name","MEG","Average Score","Worst Topic"),style="mystyle.Treeview")
        tree.pack(side=LEFT,fill=Y)
        tree.heading('#0', text='Name')
        tree.heading('#1', text='MEG')
        tree.heading('#2', text='Avg Score')
        tree.heading('#3', text='Worst Topic')
        tree.column("#0",width=150)
        tree.column("#1",width=50)
        tree.column("#2",width=80)
        tree.column("#3",width=150)
        tree.column('#4',width=0)

        vertical_sb = ttk.Scrollbar(self.win, orient="vertical", command=tree.yview)
        vertical_sb.pack(side=LEFT)
        tree.configure(yscrollcommand=vertical_sb.set)
        
        style.use("ggplot")

        self.FillTreeClass(tree)
        self.FillTree(tree)
        self.add_menu(self.win,"Navigate", commands = [("Instructions",self.on_enter,True),("Admin", self.ClassAdmin, True), ("Set Homework", self.SetHW, True),("Set Quiz", self.SetQuiz, True),("Assigned Work",self.History,True)])#,("Log Out",self.LogOut(self.win),True)])

        def OnDoubleClick(event):
            item = tree.selection()[0]
            print(item,tree.item(item,"text"))
            self.LoadStudentProgress(tree.item(item,"text"))

        tree.bind("<Double-1>",OnDoubleClick)

        count = Counter(self.name_of_quizzes)
        quizzes=list(count)
        print(quizzes)
        score_info=[]
        # Add up scores of specific quiz and append to list that will be plotted
        for n in range(len(quizzes)):
            score=0
            checker=0
            for l in range(len(self.h)):
                if quizzes[n]== self.h[l][3]:
                    #print(self.h[l][3])
                    score+=self.h[l][2]
                    checker+=1
            score_info.append(int(score/checker))
                    
                
        class_= Figure(figsize=(6,5),dpi=100)
        class_.clf()######Remove previous graph
        b= class_.add_subplot(111)
        bar1 = FigureCanvasTkAgg(class_, self.win)

        data= {"Index":quizzes,"Score":score_info }
                        
        df1= DataFrame(data,columns=["Index","Score"])
        df1= df1[["Index","Score"]].groupby("Index").sum()

        toolbar= NavigationToolbar2Tk(bar1,self.win)
        toolbar.update()
        bar1._tkcanvas.pack(anchor= NE)#,expand= True)

        bar1.get_tk_widget().pack(anchor=N,expand=True)
        df1.plot(kind="bar",legend=True,ax= b,color="b")

        self.win.mainloop()
    
    def add_menu(self,window_name,menuname, commands):
        menubar = Menu(window_name)
        window_name.config(menu=menubar)
        menu = Menu(menubar, tearoff = 0)

        for command in commands:
            menu.add_command(label = command[0], command = command[1])
            if command[2]:
                menu.add_separator()

        menubar.add_cascade(label=menuname, menu=menu)

    def ClassAdmin(self):
        classmanage= Teacher.teacher(self.win)
        classmanage.Manage_class()
    
    def SetHW(self):
        set_homew= Set_hw.Set_Homework(self.win)
        set_homew.Set_Homeworks()
    
    def SetQuiz(self):
        set_quiz= set_revision.Revision(self.win)
        set_quiz.Title()

    def History(self):
        h= History.History(self.win)
        h.Main()

    def on_enter(self):
        messagebox.showinfo("Instructions", "Double click any student record and his/her results.")
    
    """def LogOut(self,page):
        log=login_page.Starting()
        log.login(page)"""
        

    
#t= TeacherProgress()
#t.MainPage()

#Display quiz names properly