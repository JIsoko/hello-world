"""
Where Teacher will set homework after inputting url code, hw title and deadline
"""

# WORKS

import mysql.connector
from tkinter import *
from bs4 import BeautifulSoup
import requests
from datetime import datetime as dt
#import login_page
from tkinter import ttk
from tkinter import messagebox
import set_revision
import History
import Teacher
import teacher_progress
from tkinter import ttk
from ttkthemes import themed_tk as tk

conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
cur=conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS set_homework(code VARCHAR(6) ,title TEXT,text TEXT, deadline DATE)")
conn.commit()
conn.close()



class Set_Homework():

    def __init__(self,GUI):
        GUI.destroy()
        self.date=""

    def Set_Homeworks(self):

        self.window= tk.ThemedTk()
        self.window.geometry("729x165")
        self.window.wm_title("Set Homework")

        self.window.get_themes()
        self.window.set_theme("radiance")


        title= ttk.Label(self.window,text="Set Homework")
        title.grid(row=0,column=1)
        #title.config(font=("Courier bold",30))


        title_la= ttk.Label(self.window,text= "Title")
        title_la.grid(row=1,column=0,padx=10,pady=8)
        #title_la.config(font=("Courier bold",20))

        title_e= ttk.Entry(self.window,width=30)
        title_e.grid(row=2, column=0,padx=6)

        url_la=ttk.Label(self.window, text="Website link")
        url_la.grid(row=1,column=1,pady=8)
        #url_la.config(font=("Courier bold",20))

        url_e= ttk.Entry(self.window,width=50)
        url_e.grid(row=2, column=1)

        deadline_la= ttk.Label(self.window,text= "Deadline")
        deadline_la.grid(row=1,column=3)#,padx=5)
        #deadline_la.config(font=("Courier bold",20))

        day_e= ttk.Combobox(self.window,width=6)
        day_e["values"]= (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31)
        day_e.grid(row=2,column=2,padx=3)

        month_e= ttk.Combobox(self.window,width=6)
        month_e["values"]= ("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")
        month_e.grid(row=2,column=3,padx=3)

        year_e= ttk.Combobox(self.window,width=6)
        year_e["values"]= (dt.now().year, dt.now().year+1,dt.now().year+2)
        year_e.grid(row=2,column=4,padx=3)

        set_b= ttk.Button(self.window, text= "Set",width=30,command= lambda:self.PreConfirm(title_e.get(),url_e.get(),day_e.get(),month_e.get(),year_e.get()))
        set_b.grid(row=3,column=1,padx=20, pady=20)

        self.add_menu(self.window,"Navigate", commands = [("Admin", self.ClassAdmin, True), ("Progress", self.Progress, True),("Set Quiz", self.SetQuiz, True),("Assigned Work",self.History,True)])#,("Log Out",self.LogOut(self.window),True)])


        self.window.mainloop()

    def Confirm_page(self,title,url,deadline):

        try:
            requests.get(url)

            page=tk.ThemedTk()
            page.wm_title("Confirm Homework: "+title)
            page.geometry("480x550")
            
            page.get_themes()
            page.set_theme("radiance")

            r= requests.get(url)
            c= r.content

            soup= BeautifulSoup(c,"html.parser")

            h1=soup.find_all("h1")
            h2=soup.find_all("h2")
            al= soup.find_all("p")

            confirm_title= ttk.Label(page, text= title+": "+self.date)
            confirm_title.grid(row=0,column=0,padx=10,pady=5)
            confirm_title.config(font=("Calibri",20))

            self.year= ttk.Combobox(page,width=16)
            self.year["values"]= ("1","2")
            self.year.insert(END,"Year_")
            self.year.grid(row=0,column=1,padx=10,pady=5)

            def on_enter(event):
                self.year.delete(0,END)


            self.year.bind("<Button-1>",on_enter)



            n= Text(page, width=50,height=25,borderwidth=3, relief="sunken")
            n.grid(row=1,column=0,rowspan=5,columnspan=2,pady= 10,padx=20)


            scrollb = ttk.Scrollbar(page, command=n.yview)
            scrollb.grid(row=3, column=2,padx=3)
            n['yscrollcommand'] = scrollb.set

            def put():#
                n.delete("1.0",END)
                content=""
                for items in h1,h2,al:
                    for item in range(0,len(items)):
                        n.insert(END,str(items[item].text))

            put()

            confirm_frame= ttk.Frame(page)
            confirm_frame.grid(row=7,column=0,rowspan=2,columnspan=4)

            confirm_b= ttk.Button(confirm_frame,text="Confirm",width=15,command=lambda:self.INSERTER(title,url,deadline,page))
            confirm_b.grid(row=8,column=1,padx=8)

            shred_b= ttk.Button(confirm_frame,text="Cancel",width=15,command=page.destroy)
            shred_b.grid(row=8,column=3)

            page.mainloop()
        
        except Exception as e:
            print(str(e))
            page.destroy()
            messagebox.showinfo("Error","Check the weblink")
            #url_e.delete(0,END)
            #url_e.configure({"background":"#DC231F"})

    def INSERTER(self,title,text,deadline,page):# Allows records to be inserted in the database
        print(title,text,deadline)
        conn= mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        cur=conn.cursor()
        cur.execute("SELECT code,email FROM gclass WHERE role=%s AND year=%s",("Student",int(self.year.get())))
        rows=cur.fetchall()
        for element in range(len(rows)):
            print(rows[element][0])##### check
            cur.execute("INSERT INTO set_homework VALUES(%s,%s,%s,%s)",(rows[element][0],title,text,deadline))
            conn.commit()

            import smtplib

            server= smtplib.SMTP("smtp.gmail.com",587)
            server.starttls()
            server.login("germanrevisestudy@gmail.com","NuncaFumar01")
            msg= "Homework: "+ title +" has been set for: "+ self.date
            subject= "Homework: "+ title +" has been set"
            body= "Subject: {} \n\n {}".format(subject,msg)

            server.sendmail("germanrevisestudy@gmail.com",rows[element][1],body)
            server.quit()

        character = '/'
        g=[pos for pos, char in enumerate(text) if char == character]
        text_history= text[g[1]+1:g[2]]#Gets name of website from long url
        print(text_history)

        cur.execute("INSERT INTO hw_history VALUES(NULL,%s,%s,%s,%s)",(title,text_history,self.date,dt.now().date()))
        conn.commit()
        conn.close()
        page.destroy()
        messagebox.showinfo("SUCCESS","Homework: "+title + " has been assigned")


    def PreConfirm(self,title,url, day,month,year):
        print("Ok here")
        if int(day)> 28 and month== "Feb":
            messagebox.showinfo("Wrong Entry","Check your date entries")
        else:
            self.date= str(day)+" "+str(month)+ " "+ str(year)
            deadline=""
            deadline= dt.strptime(str(day)+" " + month+" "+str(year), "%d %b %Y")
            print(deadline,type(deadline.day),type(deadline.month),type(deadline.year))
            if deadline > dt.now():
                print("About to send off")
                self.Confirm_page(title,url, deadline)
                print("Sent")
            else:
                messagebox.showinfo("Wrong Entry","Check your date entries")

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

    def History(self):
        h= History.History(self.window)
        h.Main()

    """def LogOut(self,page):
        log=login_page.Starting()
        log.login(page)"""

        






