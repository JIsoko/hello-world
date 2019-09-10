import mysql.connector
from tkinter import *
from tkinter import ttk
from ttkthemes import themed_tk as tk
from tkinter import messagebox
import base64
from tkinter import font
from collections import Counter
import progress_page 
import stud_hw
import webbrowser
import Student_settings
from PIL import Image, ImageTk
from pygame import mixer
from mutagen.mp3 import MP3
import os
from difflib import SequenceMatcher



class CompleteQuiz():
    
    def __init__(self,student_name):
        self.question_title= ""
        self.question_number= 1
        self.tot=0
        self.answers=[]
        self.correct_answers=[]
        self.list_of_lists=[]
        self.selected_tuple=[]
        self.student_name= student_name
        self.bad_topics=[]
        self.list_of_quizzes=[]
        self.userID= ""
        self.check= True
        self.sound= False
        self.no_quiz=False
        self.paused = False
        self.muted=False
        self.active=False
        self.n_questions=""


        connection=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        cur= connection.cursor()
        cur.execute("SELECT code FROM gclass WHERE name=%s",(self.student_name,))
        userID= cur.fetchall()
        self.userID= userID[0][0]
        connection.close()

    #Fills listbox with quizzes title
    def FillTreeview(self,treeview):
        try:
            list_of_quizzes=[]
            list_of_topics=[]
            values=[]
            conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
            cur=conn.cursor()
            cur.execute("SELECT title FROM revising")
            titles=cur.fetchall()

            for quiz_title in range(len(titles)):
                #print(titles[quiz_title])#
                list_of_quizzes.append(titles[quiz_title][0])
            #print(list_of_quizzes)

            count = Counter(list_of_quizzes)
            #print(count)
            quizzes=list(count.keys())
            print(quizzes)
            for element in range(len(quizzes)):
                #print(quizzes[element])
                cur.execute("SELECT topic FROM revising WHERE title=%s",(quizzes[element],))
                topics_of_quiz=cur.fetchall()
                #print(topics_of_quiz)
                temp_list=[]
                for l in range(len(topics_of_quiz)):
                    temp_list.append(topics_of_quiz[l][0])
                print(temp_list,"Temp LIST")
                count = Counter(temp_list)
                topics=list(count)
                print(topics)
                max_cnt = max(topics)
                #print(max_cnt)  
                print(topics)
                total=0
                for element in range(0,len(topics)):
                    if topics[element]==max_cnt:
                        total+=1
                        print(topics[element])
                        most_common = count.most_common(total)
                print(quizzes[element])
                        #print(most_common)
                values.append(most_common[0][0])
                        #print(values)


            #print(values)
            for element in range(len(values)):
                treeview.insert("","end",text=quizzes[element],values=(values[element],))

        except:
            self.no_quiz=True

    #Listox with all different quizzes
    def ChooseQuiz(self,GUI):
        GUI.destroy()
        quizzes_page=tk.ThemedTk()
        quizzes_page.wm_title("Choose a Quiz")
        quizzes_page.geometry("590x290")

        quizzes_page.get_themes()
        quizzes_page.set_theme("radiance")

        print(self.no_quiz)

        if self.no_quiz== True:
            messagebox.showinfo("No Quiz Available", "No quiz available at this moment")

        la= ttk.Label(quizzes_page,text="Pick a Quiz!")
        #la.config(font=("Courier",30))
        la.grid(row=0,column=3)

        styling = ttk.Style()
        styling.configure("mystyle.Treeview", highlightthickness=0, bd=1, font=('Calibri', 10)) # Modify the font of the body
        styling.configure("mystyle.Treeview.Heading", font=('Calibri', 14,'bold'))

        tree= ttk.Treeview(quizzes_page,columns=("Quiz","Most Frequent Topic"),style="mystyle.Treeview")
        tree.grid(row=3,column=2,rowspan=1,columnspan=3,padx=30,pady=10)
        tree.heading('#0', text='Quiz')
        tree.heading('#1', text='Most Frequent Topic')
        tree.column("#0",width=200)
        tree.column("#1",width=280)
        tree.column('#2',width=0)

        self.FillTreeview(tree)
        self.add_menu(quizzes_page,"Navigate", commands = [("Progress", lambda: self.Progress_Page(quizzes_page), True), ("Homework", lambda: self.Homework(quizzes_page), True),("MySFC", self.MYSFC, True),("Update Phone Number",lambda: self.Change_Phone(quizzes_page),True),("Update Email Address",lambda:self.Change_Email(quizzes_page),True)])
        sb1=Scrollbar(quizzes_page, orient="vertical", command=tree.yview)
        sb1.grid(row=3,column=6)
        tree.configure(yscrollcommand=sb1.set)

        def OnDoubleClick(event):
            item = tree.selection()[0]
            self.question_title=tree.item(item,"text")
            quizzes_page.destroy()
            self.Quiz_N_Image()
        
        tree.bind("<Double-1>",OnDoubleClick)
        
        
        quizzes_page.mainloop()
    
    #Function to load and group questions with same question title
    def LoadQuestion(self):
        conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        cur=conn.cursor()
        cur.execute("SELECT question FROM revising WHERE title=%s ",(self.question_title,))
        self.rows=cur.fetchall()
        cur.execute("SELECT image,ext FROM revising WHERE title=%s ",(self.question_title,))
        self.images=cur.fetchall()
        conn.close()
        self.n_questions= str(len(self.rows))
        print(self.rows[self.question_number-1])
        self.question= self.rows[self.question_number-1][0]
        print(self.question_number)
        if self.images[self.question_number-1][0]== "-":
            self.check= False
        else:
            self.check= True
            self.photo= self.images[self.question_number-1][0]
            self.extension= self.images[self.question_number-1][1]
            print(self.extension)
            if self.extension== ".wav" or self.extension== ".mp3" or self.extension== ".mp4":
                self.sound= True
        if self.question_number>1:
            self.Quiz_N_Image()
            

    def Quiz_N_Image(self):
        self.win= tk.ThemedTk()
        self.win.get_themes()
        self.win.set_theme("radiance")
        #self.win.wm_title(self.question_title+": "+str(self.question_number)+"/"+str(len(self.rows)))
        
        if self.tot==0:
            self.LoadQuestion()
            self.tot+=1
        
        page_title=str(self.question_title)+ ": "+str(self.question_number)+"/"+self.n_questions
        self.win.wm_title(page_title)
        #print(self.n_questions)

        if self.check==True:
            width= 0
            self.answer_width=0
            if len(self.question)>15 and len(self.question)<25:
                for letter in range(len(self.question)):
                    width+=26
                    self.answer_width+=2.5
                width= width+350
                dimensions= str(width)+"x386"
            elif len(self.question)>25:
                for letter in range(len(self.question)):
                    width+=21
                    self.answer_width+=2.5
                width= width+400
                dimensions= str(width)+"x386"
            else:
                dimensions="900x380"
                self.answer_width=60
            self.win.geometry(dimensions)
            fh= open("Quiz_Data"+self.extension,"wb") #-4: means extension of photo which could vary
            fh.write(base64.b64decode(self.photo))
            print(fh)
            fh.close()
            if self.sound== False:
                img= Image.open('Quiz_Data'+self.extension)
                resized = img.resize((400, 300),Image.ANTIALIAS)
                img3 = ImageTk.PhotoImage(resized)
                l1=ttk.Label(self.win,image=img3)
                l1.grid(row=0,column=0,rowspan=3,columnspan=2,padx=10)
            else:
                mixer.init()
                self.active=True
                self.lenghtlabel=ttk.Label(self.win,text="Total Length : --:--")
                self.lenghtlabel.grid(row=0,column=1)

                self.scale=ttk.Scale(self.win,from_=0,to=100,orient=HORIZONTAL,command=self.Set_Volume)
                self.scale.set(70)
                mixer.music.set_volume(0.7)
                self.scale.grid(row=0,column=0,padx=10,pady=20)

                self.Show_Details()

                play_image= PhotoImage(file="play button.png")
                pause_image= PhotoImage(file="pause_icon.png")
                rewind_image= PhotoImage(file="rewind_button.png")
                mute_image=PhotoImage(file="mute-button.png")
                play_b= ttk.Button(self.win,image=play_image,command= self.Play_Sound).grid(row=1,column=0,padx=10)
                pause_b= ttk.Button(self.win,image=pause_image,command= self.Stop).grid(row=1,column=1)
                rewind_b=ttk.Button(self.win,image=rewind_image,command=self.Rewind).grid(row=2,column=0)
                mute_b=ttk.Button(self.win,image=mute_image,command=self.Mute).grid(row=2,column=1)
            #create sound buttons (play and stop)

            question_l= ttk.Label(self.win,text="Question: "+ self.question)
            #question_l.config(font=("Courier",25))
            question_l.grid(row=0,column=2,padx=10)

            #Entry Box for answer to be compiled
            answer_b= ttk.Entry(self.win,width= int(self.answer_width))
            answer_b.grid(row=1,column=2,padx=10)#Make width according to question length


            #Hint box is initially empty
            self.hint_bo= ttk.Entry(self.win)
            self.hint_bo.grid(row=3,column=2,padx=10,pady=5)

            #Button to be next to hint box
            hint_button=ttk.Button(self.win,text="Hint",width=7,command=lambda: self.ShowHint(self.hint_bo))
            hint_button.grid(row=3,column=1)
            # Button to Finish
            finish_button=ttk.Button(self.win,text="Finish",width=19,command=lambda: self.FinishQuiz(answer_b.get()))
            finish_button.grid(row=7,column=1,pady=5)

            #Button for next question
            next_button=ttk.Button(self.win,text="Next",width=19,command=lambda: self.LoadNextQuestion(answer_b.get()))
            next_button.grid(row=7,column=2,pady=5,padx=10)

            #temp_b=Button(self.win,text="Measurements",command=self.Get_Measurements)
            #temp_b.grid(row=6,column=1)


        else:
        #Label that displays question
            self.width=0
            if len(self.question)>7:
                for letter in range(len(self.question)):
                    self.width+=22
                dimensions= str(self.width-50)+"x150"
            else:
                dimensions=("400x150")
            self.win.geometry(dimensions)#make iteration to adjust window size if question longer

            question_label= ttk.Label(self.win,text=self.question)
            #question_label.config(font=("Courier",25))
            question_label.grid(row=0,column=0,columnspan=2,pady=5,padx=10)

            #Entry Box for answer to be compiled
            answer_box= ttk.Entry(self.win,width= 60)
            answer_box.grid(row=2,column=0,columnspan=2,padx=10)


            #Hint box is initially empty
            self.hint_box= ttk.Entry(self.win)
            self.hint_box.grid(row=5,column=1,padx=10,pady=5)

            #Button to be next to hint box
            hint_b=ttk.Button(self.win,text="Hint",width=5,command=lambda: self.ShowHint(self.hint_box))
            hint_b.grid(row=5,column=0)
            # Button to Finish
            finish_b=ttk.Button(self.win,text="Finish",width=10,command=lambda: self.FinishQuiz(answer_box.get()))
            finish_b.grid(row=7,column=0)

            #Button for next question
            next_b=ttk.Button(self.win,text="Next",width=10,command=lambda: self.LoadNextQuestion(answer_box.get()))
            next_b.grid(row=7,column=1)
    
        self.win.mainloop()

    def Get_Measurements(self):
        print(self.win.winfo_height())
        print(self.win.winfo_width())

    def Play_Sound(self):
        if self.paused== True:
            mixer.music.unpause()
        else:
            mixer.music.load("Quiz_Data"+self.extension)
            mixer.music.play()

    def Show_Details(self):
        file_data=os.path.splitext("Quiz_Data"+self.extension)

        if file_data[1]==".mp3":
            audio=MP3("Quiz_Data"+self.extension)
            total_length= audio.info.length
        else:
            a=mixer.Sound("Quiz_Data"+self.extension)
            total_length= a.get_length()

        mins,secs= divmod(total_length,60)
        mins=round(mins)
        secs=round(secs)
        timeformat='{:02d}:{:02d}'.format(mins,secs)
        self.lenghtlabel['text']="Total Length"+"-"+timeformat


    def Stop(self):
        self.paused=True
        mixer.music.pause()

    def Set_Volume(self,val):
        volume=float(val)/100
        mixer.music.set_volume(volume)

    def Rewind(self):
        self.paused=False
        self.Play_Sound()

    def Mute(self):
        if self.muted==True:
            self.scale.set(70)
            mixer.music.set_volume(0.7)
        else:
            self.scale.set(0)
            mixer.music.set_volume(0.0)
            self.muted=True

    #Function to show hint when clicked   
    def ShowHint(self,hint_box):
        conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        cur=conn.cursor()
        cur.execute("SELECT hint FROM revising WHERE question=%s ",(self.question,))
        self.hint=cur.fetchall()
        conn.close()
        print(self.hint[0][0])
        hint_box.delete(0,END)
        hint_box.insert(END,self.hint[0][0])     

    #Function to load next question
    def LoadNextQuestion(self,answer):
        self.sound= False
        if self.active== True:
            mixer.music.stop()

        if self.question_number < len(self.rows):
            print(True)
            self.answers.append(answer)
            print(self.answers)
            self.question_number+=1
            self.win.destroy()
            self.LoadQuestion()
        else:
            self.FinishQuiz(answer)


    #Function to conclude quiz showing results
    def FinishQuiz(self,answe):
        if self.active== True:
            mixer.music.stop()

        self.answers.append(answe)
        conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        cur=conn.cursor()
        cur.execute("SELECT correct_answer FROM revising WHERE title=%s",(self.question_title,))
        rows=cur.fetchall()

        for row in range(0,len(rows)):
            self.correct_answers.append(rows[row][0])
        for i in range(0,len(self.correct_answers)-len(self.answers)):
            self.answers.append("BLANK")
        self.marks=0
        for response in range(len(self.answers)):
            cur.execute("SELECT n_marks FROM revising WHERE correct_answer=%s",(self.correct_answers[response],))
            points=cur.fetchall()
            result= SequenceMatcher(None,self.correct_answers[response].upper(),self.answers[response].upper()).ratio()
            if int(result*100)>=90:
                self.marks+=points[0][0]
            elif int(result*100) >= 75 and int(result*100)<90:
                self.marks+= (points[0][0]*3//4)
            elif int(result*100) >= 50 and int(result*100)<75:
                self.marks+= (points[0][0]//2)
            elif int(result*100) >=25 and int(result*100)<50:
                self.marks+= (points[0][0]//4)
            else:
                self.marks+=0
            #print(self.marks,type(self.marks))
        cur.execute("SELECT n_marks FROM revising WHERE title=%s",(self.question_title,))
        total_p= cur.fetchall()
        conn.commit()
        conn.close()
        self.total_marks=0
        for mark in range(len(total_p)):
            self.total_marks+=total_p[mark][0]

        print(self.total_marks,type(self.total_marks))

        self.Results()

    def FillTree(self,treeview):
        conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        cur=conn.cursor()
        cur.execute("SELECT * FROM revising WHERE title=%s",(self.question_title,))
        rows=cur.fetchall()
        conn.commit()
        conn.close()
        for tuple in range(len(rows)):
            self.list_of_lists.append(list(rows[tuple]))
        for element in range(len(self.correct_answers)):
            tag= " "+ self.list_of_lists[element][2] #question of each record
            treeview.insert("","end",text=self.list_of_lists[element][2],values= (self.answers[element],self.list_of_lists[element][4],self.list_of_lists[element][3],self.list_of_lists[element][-1]),tags=(tag,))
            result= SequenceMatcher(None,self.list_of_lists[element][4].upper(),self.answers[element].upper()).ratio()
            if int(result*100)>=90:
                treeview.tag_configure(tag,background= "#228B22")#228B22
            elif int(result*100) >= 75 and int(result*100)<90:
                treeview.tag_configure(tag,background= "#98FF98")
            elif int(result*100) >= 50 and int(result*100)<75:
                self.bad_topics.append(self.list_of_lists[element][-1])
                treeview.tag_configure(tag,background= "#FF8C00")#FF8C00
            elif int(result*100) >=25 and int(result*100)<50:
                self.bad_topics.append(self.list_of_lists[element][-1])
                treeview.tag_configure(tag,background= "#FF4500")#FF4500
            else:
                treeview.tag_configure(tag,background= "#FE140F")
                self.bad_topics.append(self.list_of_lists[element][-1])#Topic of question incorrectly answered
        print(self.bad_topics)

    def Results(self):
        self.win.destroy()
        results_page= tk.ThemedTk()
        results_page.get_themes()
        results_page.set_theme("radiance")


        results= ttk.Label(results_page, text=str(self.question_title)+":" +str(self.marks)+ "/"+ str(self.total_marks)) 
        results.grid(row=0,column=2)
        results.config(font=("Courier",45))

        self.mark_percentage= int((self.marks/self.total_marks)*100) 
        print(str(self.mark_percentage)+"%")

        results_page.wm_title(self.question_title+": "+str(self.mark_percentage)+"%")

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 12)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 14,'bold'))

        tree= ttk.Treeview(results_page,columns=("Question","Your Answer","Correct Answer","Marks","Topic"),style="mystyle.Treeview")
        tree.grid(row=3,column=0,rowspan=1,columnspan=5,padx=10,pady=10)
        tree.heading('#0', text='Question')
        tree.heading('#1', text='Your Answer')
        tree.heading('#2', text='Correct Answer')
        tree.heading('#3', text='Marks')
        tree.heading('#4', text='Topic')
        tree.column("#0",width=280)
        tree.column("#1",width=280)
        tree.column("#2",width=300)
        tree.column("#3",width=80)
        tree.column('#4',width=200)
        tree.column('#5',width=0)

        self.FillTree(tree)
        self.add_menu(results_page,"Navigate", commands = [("Progress", lambda: self.Progress_Page(results_page), True), ("Homework", lambda: self.Homework(results_page), True),("MySFC", self.MYSFC, True),("Update Phone Number",lambda: self.Change_Phone(results_page),True),("Update Email Address",lambda:self.Change_Email(results_page),True)])#,("Log Out",self.LogOut(results_page),True)])


        ####Shows which topic(s) is the worst among the topics of questions answered incorrectly
        if len(self.bad_topics)>=1:
            count = Counter(self.bad_topics)
            freq_list = list(count.values())
            max_cnt = max(freq_list)
            total=0
            for element in range(0,len(freq_list)):
                if freq_list[element]==max_cnt:
                    total+=1
            most_common = count.most_common(total)

            print(most_common)
            for topic in range(0,len(most_common)):
                topic_to_work=most_common[topic][0]
                if len(most_common)> 1:
                    worsttopic= topic_to_work+","
                else:
                    worsttopic=topic_to_work

            
        else:
            worsttopic= "NONE"
        
        print(worsttopic)

        
        ### code that inserts userID, quiz name, score and worsttopic to table called progress
        connection=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        cur= connection.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS progress(id INTEGER AUTO_INCREMENT PRIMARY KEY,code VARCHAR(6), score INTEGER,quiz_name TEXT,worsttopic TEXT) ")
        cur.execute("SELECT code FROM gclass WHERE name=%s",(self.student_name,))
        userID= cur.fetchall()
        self.userID= userID[0][0]
        cur.execute("INSERT INTO progress VALUES(NULL,%s,%s,%s,%s)",(self.userID,self.mark_percentage,self.question_title,worsttopic))
        connection.commit()
        connection.close()
        vertical_sb = ttk.Scrollbar(results_page, orient="vertical", command=tree.yview)
        vertical_sb.grid(row=3,column=5,padx=5)
        tree.configure(yscrollcommand=vertical_sb.set)
        
        
        progress_b= ttk.Button(results_page,text="Progress",width=20,command= lambda:self.Progress_Page(results_page)).grid(row=5,column=4)# Linked to progress page

        results_page.mainloop()
        

    def add_menu(self,window_name,menuname, commands):
        menubar = Menu(window_name)
        window_name.config(menu=menubar)
        menu = Menu(menubar, tearoff = 0)

        for command in commands:
            menu.add_command(label = command[0], command = command[1])
            if command[2]:
                menu.add_separator()

        menubar.add_cascade(label=menuname, menu=menu)

    def MYSFC(self):
        webbrowser.open_new_tab("mysfc.stokesfc.ac.uk/")
    def Progress_Page(self,win):
        student_prog= progress_page.StudentProgress(self.userID,win)
        student_prog.MainPage()
    def Homework(self,win):
        see_hw= stud_hw.See_Homework(win)
        see_hw.See_hw(self.userID)
    def Change_Email(self,win):
        student_changes= Student_settings.Student_Setting(self.userID)
        student_changes.Change_Email(win)
    def Change_Phone(self,win):
        student_changes= Student_settings.Student_Setting(self.userID)
        student_changes.Enter_New_Number(win)
    """def LogOut(self,page):
        log=login_page.Starting()
        log.login(page)"""

