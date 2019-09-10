"""
Teacher can set revision questions and images 

"""

import mysql.connector
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import Set_hw 
import History
import teacher_progress
import Teacher
import base64
from ttkthemes import themed_tk as tk




class Revision():
    def __init__(self,GUI):
        GUI.destroy()
        self.individual_quiz= []
        self.quiz_name= " "

    def Title(self):
        self.frame= tk.ThemedTk()
        self.frame.geometry("380x105")
        self.frame.wm_title("Give your quiz a title!")

        self.frame.get_themes()
        self.frame.set_theme("radiance")
        
        intro=ttk.Label(self.frame,text="Set up a Quiz").grid(row=0,column=2,padx=8,pady=5)

        title_label= ttk.Label(self.frame, text= "Title").grid(row=1,column=1,padx=8,pady=5)
        self.title_var= StringVar() 
        self.title_e= ttk.Entry(self.frame,width= 45,textvariable= self.title_var,justify="center")
        self.title_e.grid(row=1,column=2)

        self.add_menu(self.frame,"Navigate", commands = [("Admin", self.ClassAdmin, True), ("Set Homework", self.SetHW, True),("Progress", self.Progress, True),("Assigned Work",self.History,True)])#,("Log Out",self.LogOut(self.frame),True)])


        next_step_b=ttk.Button(self.frame,text="Next",width=30,command=lambda: self.AfterTitle()).grid(row=3,column=2)

        self.frame.mainloop()


    def AfterTitle(self):
        self.quiz_name=self.title_e.get()
        print(self.title_var.get(),self.quiz_name)
        self.frame.destroy()
        self.SetQuiz()

    def SetQuiz(self):
        self.win= tk.ThemedTk()
        self.win.wm_title("Question: "+str(len(self.individual_quiz)+1))
        self.win.geometry("750x250")
        self.win.get_themes()
        self.win.set_theme("radiance")

        question_label= ttk.Label(self.win, text= "Question").grid(row=2,column=1,padx=8,pady=5)
        marks_label= ttk.Label(self.win, text= "Marks").grid(row=5,column=1,padx=8,pady=5)
        correct_label= ttk.Label(self.win, text= "Correct Answer").grid(row=4,column=1,padx=8,pady=5)
        topic_label= ttk.Label(self.win, text= "Topic").grid(row=7,column=1,padx=8,pady=5)

        self.question_var= StringVar()
        self.question_e= ttk.Entry(self.win,width= 45,textvariable= self.question_var,justify="center")
        self.question_e.grid(row=2,column=2)
        self.correct_var= StringVar()
        self.correct_e= ttk.Entry(self.win,width= 45,textvariable= self.correct_var,justify="center")
        self.correct_e.grid(row=4,column=2)
        self.check_hint= IntVar()
        self.check_image=IntVar()
        hint_b= ttk.Checkbutton(self.win, variable=self.check_hint, onvalue=1, offvalue=0, text= "Hint")
        hint_b.grid(row=3,column=1,padx=8,pady=5)
        self.hint_var= StringVar()
        self.hint_e=ttk.Entry(self.win,width= 45,textvariable= self.hint_var,justify="center")
        self.hint_e.grid(row=3,column=2)
        self.marks_var= StringVar()
        self.marks_e=ttk.Entry(self.win,width= 5,textvariable= self.marks_var,justify="center")
        self.marks_e.grid(row=5,column=2)
        self.topic_var= StringVar()
        self.topic_e= ttk.Combobox(self.win,width=45,textvariable=self.topic_var,font="Helvetica 10 bold",justify="center")
        self.topic_e["values"]= ("Home","Family","Holiday","Past Tense","Present Tense","Future Tense","Yourself","Environment","World","Education")
        self.topic_e.grid(row=7,column=2,padx=8,pady=5)
        image_b= ttk.Checkbutton(self.win, variable=self.check_image, onvalue=1, offvalue=0, text= "Image/Sound").grid(row=6,column=1,padx=8,pady=5)
        self.image_var= StringVar()
        self.image_e=ttk.Entry(self.win,width= 45,textvariable= self.image_var,justify="center")
        self.image_e.grid(row=6,column=2)

        self.add_menu(self.win,"Instructions", commands = [("Instructions", self.Instructions, True),("Load Data",self.Load_Image,True)])

        next_b= ttk.Button(self.win, text= "Another",width=18,command= lambda: self.NextQuestion()).grid(row=9,column=1,padx=6,pady=4)
        finish_b= ttk.Button(self.win, text= "Finish",width=18,command= lambda: self.Finish()).grid(row=9,column=3,padx=6,pady=4)

        print(self.topic_e.get())
        
        self.win.mainloop()

    def create(self):
        conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        cur=conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS revising(id INTEGER PRIMARY KEY AUTO_INCREMENT ,title TEXT,question TEXT, n_marks INTEGER,correct_answer TEXT, hint TEXT, image_check INTEGER, image LONGBLOB,ext TEXT,topic TEXT)")
        conn.close()



    def INSERTER(self):# Allows records to be inserted in the database
        print("In Inserter fucntion")
        print("Question E",self.question_e.get())
        print("Question Var",self.question_var.get())
        if self.hint_e.get()=="":
            self.check_image=0
        else:
            self.check_image=1
        if self.image_e.get()== "":
            self.im= "-"
        else:
            self.im = self.image_e.get()
        print(self.quiz_name,self.question_e.get(),self.marks_e.get(),self.correct_e.get(),self.hint_e.get(),self.check_image,self.im,self.topic_e.get())
        if self.question_e.get()!= '' and self.marks_e.get()!= '' and self.correct_e.get()!= '':
            question_tuple= [self.quiz_name,self.question_e.get(),self.marks_e.get(),self.correct_e.get(),self.hint_e.get(),self.check_image,self.im,self.topic_e.get()]
            print(question_tuple)
            self.individual_quiz.append(question_tuple)
        print(self.individual_quiz)

    def Finish(self):
        # Treeview. click button and actually finish
        self.INSERTER()
        self.QuizSummary(self.win)
        print(self.individual_quiz)

    def Confirm(self,window):
        self.create()
        for element in range(0,len(self.individual_quiz)):
            if self.individual_quiz[element][6]== "" or self.individual_quiz[element][6]== "-":
                ext= "-"
                image=self.individual_quiz[element][6]
            else:
                ext= self.individual_quiz[element][6][-4:]
                with open(self.individual_quiz[element][6],"rb") as imageFile:
                    str= base64.b64encode(imageFile.read())
                    image=str
            print(ext)
            conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
            cur=conn.cursor()
            cur.execute("INSERT INTO revising VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(self.quiz_name,self.individual_quiz[element][1],self.individual_quiz[element][2],self.individual_quiz[element][3],self.individual_quiz[element][4],self.individual_quiz[element][5],image,ext,self.individual_quiz[element][7]))
            conn.commit()
            conn.close()
        messagebox.showinfo("Quiz Set","Quiz has been set successfully")
        self.Add_to_History()
        window.destroy()# Try and link back to teacher page

    def Delete_Question(self,window,e1,e2,e3,e4,e5,e6):
        for element in range(0,len(self.individual_quiz)):
            #indexing of next line are based on the structure of the list [title,question,marks,answer,hint,image_checkbox,image_link, topic]
            if self.individual_quiz[element][1]== e1 and self.individual_quiz[element][3]==e2 and self.individual_quiz[element][2]==e3 and self.individual_quiz[element][7]== e4 and self.individual_quiz[element][4]==e5 and self.individual_quiz[element][6]==e6:
                #print(self.individual_quiz[element])
                self.individual_quiz.remove(self.individual_quiz[element])
                self.QuizSummary(window)
                break

    def Edit_Question(self,window,e1,e2,e3,e4,e5,e6,v1,v2,v3,v4,v5,v6):
        for element in range(0,len(self.individual_quiz)):
            #indexing of next line are based on the structure of the list [title,question,marks,answer,hint,image_checkbox,image_link, topic]
            if self.individual_quiz[element][1]== e1 and self.individual_quiz[element][3]==e2 and self.individual_quiz[element][2]==e3 and self.individual_quiz[element][7]== e4 and self.individual_quiz[element][4]==e5 and self.individual_quiz[element][6]==e6:
                #Edit existing values with new ones  
                self.individual_quiz[element][1]= v1
                self.individual_quiz[element][3]= v2
                self.individual_quiz[element][2]= v3
                self.individual_quiz[element][7]= v4
                self.individual_quiz[element][4]= v5
                self.individual_quiz[element][6]= v6
                self.QuizSummary(window)
                break
    
    def QuizSummary(self,win):
        win.destroy()
        summary_page= tk.ThemedTk()
        summary_page.geometry("1200x325")
        summary_page.wm_title(self.quiz_name+": "+str(len(self.individual_quiz)+1)+" Questions")

        summary_page.get_themes()
        summary_page.set_theme("radiance")

        list_of_lists=[]

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 12)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 14,'bold')) # Modify the font of the headings
        #style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        
        q_entry= ttk.Entry(summary_page,width= 25)
        q_entry.grid(row=2,column=0,padx=6)
        a_entry= ttk.Entry(summary_page,width= 25)
        a_entry.grid(row=2,column=1,padx=6)
        m_entry= ttk.Entry(summary_page,width= 25)
        m_entry.grid(row=2,column=2,padx=6)
        t_entry= ttk.Entry(summary_page,width= 25)
        t_entry.grid(row=2,column=3,padx=6)
        h_entry= ttk.Entry(summary_page,width= 25)
        h_entry.grid(row=2,column=4,padx=6)
        i_entry= ttk.Entry(summary_page,width= 25)
        i_entry.grid(row=2,column=5,padx=6)



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
            



        tree.bind("<ButtonRelease-1>",get_selected_row)

        for questions in range(0,len(self.individual_quiz)):
            tree.insert("","end",text=self.individual_quiz[questions][1],values= (self.individual_quiz[questions][3],self.individual_quiz[questions][2],self.individual_quiz[questions][-1],self.individual_quiz[questions][4],self.individual_quiz[questions][6]))

        confirm_b= ttk.Button(summary_page,text= "Confirm",width=14,command= lambda: self.Confirm(summary_page)).grid(row=6,column=5)

        edit_b= ttk.Button(summary_page,text= "Edit",width=20,command=lambda: self.Edit_Question(summary_page,self.question_selected,self.value[0],self.value[1],self.value[2],self.value[3],self.value[4],q_entry.get(),a_entry.get(),m_entry.get(),t_entry.get(),h_entry.get(),i_entry.get(),)).grid(row=6,column=3)

        delete_b= ttk.Button(summary_page,text= "Delete",width=14,command=lambda: self.Delete_Question(summary_page,self.question_selected,self.value[0],self.value[1],self.value[2],self.value[3],self.value[4])).grid(row=6,column=1)

        


        summary_page.mainloop()
    

    def NextQuestion(self):
        print("In NextQuestion")
        print(self.quiz_name)
        self.INSERTER()
        self.win.destroy()
        self.SetQuiz()

    def Add_to_History(self):

        from datetime import datetime as dt
        from collections import Counter

        topics__=[]
        for element in range(len(self.individual_quiz)):
            topics__.append(self.individual_quiz[element][-1])
        print(topics__)

        count= Counter(topics__)
        print("count",count)
        topics=list(count)
        print(topics,"topics")
        max_cnt = max(topics)
        print(max_cnt,"max counts")  
        print(topics)
        total=0
        for element in range(0,len(topics)):
            if topics[element]==max_cnt:
                total+=1
                print(topics[element])
                most_common = count.most_common(total)
    
        print(most_common[0][0])

        conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        cur=conn.cursor()
        cur.execute("INSERT INTO quiz_history VALUES(NULL,%s,%s,%s,%s)",(self.quiz_name,len(self.individual_quiz),most_common[0][0],dt.now().date()))
        conn.commit()
        conn.close()

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
        classmanage= Teacher.teacher(self.frame)
        classmanage.Manage_class()
    
    def SetHW(self):
        set_homew= Set_hw.Set_Homework(self.frame)
        set_homew.Set_Homeworks()
    
    def Progress(self):
        progress=teacher_progress.TeacherProgress(self.frame)
        progress.MainPage()

    def History(self):
        h= History.History(self.frame)
        h.Main()

    def Instructions(self):
        messagebox.showinfo("Instructions", " To load an image: \n 1. Tick the image/sound check box \n 2. Click Load Data from menu")
    
    def Load_Image(self):
        self.win.filename= filedialog.askopenfilename(initialdir="/",title="Select file",filetypes= (("All files","*.*"),("png files","*.png*")))
        self.image_e.delete(0,END)
        self.image_e.insert(END,self.win.filename)
    """def LogOut(self,page):
        log=login_page.Starting()
        log.login(page)"""
    
