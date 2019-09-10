
"""
Teacher will be able to view homework and quiz assigned

"""

import mysql.connector
from tkinter import *
from datetime import datetime as dt
from tkinter import ttk
import base64
from tkinter import messagebox
import set_revision
import Teacher
import Set_hw 
import teacher_progress
from tkinter import ttk
from ttkthemes import themed_tk as tk

class History():

    def __init__(self,GUI):
        GUI.destroy()

    def create_homework(self):
        conn= mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        c=conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS hw_history(id INTEGER AUTO_INCREMENT PRIMARY KEY,name TEXT, content TEXT, deadline TEXT,date DATE)")
        conn.commit()
        conn.close()

    def create_quiz(self):
        conn= mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        c=conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS quiz_history(id INTEGER AUTO_INCREMENT PRIMARY KEY,name TEXT, questions INTEGER, topic TEXT,date DATE)")
        conn.commit()
        conn.close()

    def Main(self):
        self.create_homework()
        self.create_quiz()
        #Notebook

        self.window=tk.ThemedTk()
        self.window.wm_title("History: Homework & Quiz")
        self.window.geometry("680x290")

        self.window.get_themes()
        self.window.set_theme("radiance")

        tab_control = ttk.Notebook(self.window,style='Custom.TNotebook')
 
        tab1 = ttk.Frame(tab_control)
        
        tab2 = ttk.Frame(tab_control)
        
        tab_control.add(tab1, text='HOMEWORK')
        
        tab_control.add(tab2, text='QUIZ')

        tab_control.grid(row=0,column=1,padx=50)

        self.add_menu(self.window,"Navigate", commands = [("Admin", self.ClassAdmin, True), ("Progress", self.Progress, True),("Set Quiz", self.SetQuiz, True),("Set Homework",self.SetHW,True)])#,("Log Out",self.LogOut(self.window),True)])

        #Homework treeview
        #Homework name, url(first part), deadline, day of set
        tree_style = ttk.Style()
        tree_style.configure("mystyle.Treeview", highlightthickness=1, bd=1, font=('Calibri', 12)) # Modify the font of the body
        tree_style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold'))

        hw_tree= ttk.Treeview(tab1,columns=("Title","Content example","Deadline","Day Set"),style="mystyle.Treeview")
        hw_tree.grid(row=1,column=0,rowspan=2,pady=10,padx=15)
        hw_tree.heading('#0', text='Title')
        hw_tree.heading('#1', text='Content Example')
        hw_tree.heading('#2', text='Deadline')
        hw_tree.heading('#3', text='Day Set')
        hw_tree.column("#0",width=150)
        hw_tree.column("#1",width=150)
        hw_tree.column("#2",width=110)
        hw_tree.column("#3",width=110)
        hw_tree.column('#4',width=0)

        vertical_sb = ttk.Scrollbar(tab1, orient="vertical", command=hw_tree.yview)
        vertical_sb.grid(row=2,column=1)
        hw_tree.configure(yscrollcommand=vertical_sb.set)

        self.FillHomeworkTree(hw_tree)

        #Quiz Treeview
        #Quiz Name, Number of questions, Most revelant topic, day set

        quiz_tree= ttk.Treeview(tab2,columns=("Title","N Questions","Main Topic","Day Set"),style="mystyle.Treeview")
        quiz_tree.grid(row=1,column=0,rowspan=2,padx=15,pady=10)
        quiz_tree.heading('#0', text='Title')
        quiz_tree.heading('#1', text='Questions')
        quiz_tree.heading('#2', text='Main Topic')
        quiz_tree.heading('#3', text='Day Set')
        quiz_tree.column("#0",width=120)
        quiz_tree.column("#1",width=80)
        quiz_tree.column("#2",width=180)
        quiz_tree.column("#3",width=110)
        quiz_tree.column('#4',width=0)

        vertical_sc = ttk.Scrollbar(tab2, orient="vertical", command=quiz_tree.yview)
        vertical_sc.grid(row=2,column=1)
        quiz_tree.configure(yscrollcommand=vertical_sc.set)

        def on_click(event):
            item = quiz_tree.selection()[0]
            #print(item)
            self.value=quiz_tree.item(item,"text")
            self.Change(self.value)

        quiz_tree.bind("<Double-1>",on_click)

        self.FillQuizTree(quiz_tree)

        self.window.mainloop()

    def FillHomeworkTree(self,h_tree):
        conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        cur=conn.cursor()
        cur.execute("SELECT * FROM hw_history")
        rows=cur.fetchall()
        conn.close()
        
        for element in range(len(rows)):
            h_tree.insert("","end",text=rows[element][1],values= (rows[element][2],rows[element][3],rows[element][4]))
    
    def FillQuizTree(self,q_tree):
        conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        cur=conn.cursor()
        cur.execute("SELECT * FROM quiz_history")
        rows=cur.fetchall()
        conn.close()
        
        for element in range(len(rows)):
            q_tree.insert("","end",text=rows[element][1],values= (rows[element][2],rows[element][3],rows[element][4]))

    def Change(self,title):
        self.title=title
        summary_page= tk.ThemedTk()
        summary_page.geometry("1200x325")   

        summary_page.get_themes()
        summary_page.set_theme("radiance")

        conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        cur=conn.cursor()
        cur.execute("SELECT * FROM revising WHERE title=%s",(self.title,))
        number= cur.fetchall()
        conn.close()
        list_of_lists=[]
        for element in range(len(number)):
            list_of_lists.append([number[element][2],number[element][3],number[element][4],number[element][5],number[element][-2],number[element][-1]])



        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 12)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 14,'bold')) # Modify the font of the headings
        #style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        
        q_entry= ttk.Entry(summary_page,width= 25)
        q_entry.grid(row=2,column=0,pady=10,padx=6)
        a_entry= ttk.Entry(summary_page,width= 25)
        a_entry.grid(row=2,column=1,pady=10,padx=6)
        m_entry= ttk.Entry(summary_page,width= 25)
        m_entry.grid(row=2,column=2,pady=10,padx=6)
        t_entry= ttk.Entry(summary_page,width= 25)
        t_entry.grid(row=2,column=3,pady=10,padx=6)
        h_entry= ttk.Entry(summary_page,width= 25)
        h_entry.grid(row=2,column=4,pady=10,padx=6)
        i_entry= ttk.Entry(summary_page,width= 25)
        i_entry.grid(row=2,column=5,pady=10,padx=6)

        self.add_menu(summary_page,"Instructions", commands = [("Instructions", self.Instructions, True),("Load Data",lambda: self.Load_Image(summary_page,i_entry),True)])
        
        #style.theme_use("aqua")
        tree= ttk.Treeview(summary_page,columns=("Question","Answer","Marks","Topic","Hint","Image"),style="mystyle.Treeview")
        tree.grid(row=3,column=0,rowspan=2,columnspan=9,padx=10,pady=10)
        tree.heading('#0', text='Question')
        tree.heading('#1', text='Answer')
        tree.heading('#2', text='Marks')
        tree.heading('#3', text='Topic')
        tree.heading('#4', text='Hint')
        tree.heading('#5', text='Image')
        tree.column("#0",width=200)
        tree.column("#1",width=200)
        tree.column("#2",width=80)
        tree.column("#3",width=170)
        tree.column("#4",width=200)
        tree.column("#5",width=200) 
        tree.column("#6",width=0)  


        vertical_sb = ttk.Scrollbar(summary_page, orient="vertical", command=tree.yview)
        vertical_sb.grid(row=4,column=10,padx=5)
        tree.configure(yscrollcommand=vertical_sb.set)

        def get_selected_row(event):
            item = tree.selection()[0]
            self.value=tree.item(item,"values")
            self.question_selected= tree.item(item,"text")
            q_entry.delete(0,END)
            q_entry.insert(END,self.question_selected)

            a_entry.delete(0,END)
            a_entry.insert(END,self.value[0])

            m_entry.delete(0,END)
            m_entry.insert(END,self.value[1])

            t_entry.delete(0,END)
            t_entry.insert(END,self.value[2])

            h_entry.delete(0,END)
            h_entry.insert(END,self.value[3])

            i_entry.delete(0,END)
            i_entry.insert(END,self.value[4])
        
        for questions in range(0,len(list_of_lists)):
            tree.insert("","end",text=list_of_lists[questions][0],values= (list_of_lists[questions][2],list_of_lists[questions][1],list_of_lists[questions][-1],list_of_lists[questions][3],list_of_lists[questions][-2]))

        confirm_b= ttk.Button(summary_page,text= "Confirm",width=14,command= lambda: self.Save(summary_page)).grid(row=6,column=5)
        #Import functions from the set_revision class
        edit_b= ttk.Button(summary_page,text= "Edit",width=20,command=lambda: self.Edit_Question(summary_page,q_entry.get(),m_entry.get(),a_entry.get(),h_entry.get(),t_entry.get(),i_entry.get())).grid(row=6,column=3)

        delete_b= ttk.Button(summary_page,text= "Delete",width=14,command=lambda: self.Delete(summary_page)).grid(row=6,column=1)

        tree.bind("<ButtonRelease-1>",get_selected_row)

        summary_page.mainloop()

    def Save(self,page):
        page.destroy()

    def Edit_Question(self,page,e1,e2,e3,e4,e5,e6):#####
        print(e1,e2,e3,e4,e5,e6)
        conn= mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        c=conn.cursor()
        if e6=="-" or e6==self.value[-2]:
            print("Untouched image")
            c.execute("UPDATE revising SET question=%s,n_marks=%s, correct_answer=%s, hint=%s,topic=%s WHERE question=%s AND title=%s",(e1,e2,e3,e4,e5,self.question_selected,self.title))
        else:
            print(e6)
            extension= e6[-4:]
            with open(e6,"rb") as imageFile:
                str= base64.b64encode(imageFile.read())
                image=str
            c.execute("UPDATE revising SET question=%s,n_marks=%s, correct_answer=%s, hint=%s,topic=%s,image=%s,ext=%s WHERE question=%s AND title=%s",(e1,e2,e3,e4,e5,image,extension,self.question_selected,self.title))
        conn.commit()
        conn.close()
        page.destroy()
        self.Change(self.title)

    def Delete(self,page):
        conn= mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        c=conn.cursor()
        print(self.question_selected,self.title)
        c.execute("DELETE from revising WHERE question=%s AND title=%s",(self.question_selected,self.title))
        conn.commit()
        conn.close()
        page.destroy()
        self.Change(self.title)



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
        classmanage= Teacher.teacher(self.window)
        classmanage.Manage_class()
    
    def Progress(self):
        t= teacher_progress.TeacherProgress(self.window)
        t.MainPage()
    
    def SetQuiz(self):
        set_quiz= set_revision.Revision(self.window)
        set_quiz.Title()

    def SetHW(self):
        set_homew= Set_hw.Set_Homework(self.window)
        set_homew.Set_Homeworks()

    def Instructions(self):
        messagebox.showinfo("Instructions", " To load an image: \n 1. Tick the image/sound check box \n 2. Click Load Data from menu")
    
    def Load_Image(self,window,image_b):
        window.filename= filedialog.askopenfilename(initialdir="/",title="Select file",filetypes= (("All files","*.*"),("png files","*.png*")))
        image_b.delete(0,END)
        image_b.insert(END,window.filename)

    