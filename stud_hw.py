"""
Student will be able to access homework and after clicking a selected leads to another section
"""
from tkinter import *
from tkinter import messagebox
import mysql.connector
from datetime import datetime as dt
from bs4 import BeautifulSoup
import requests
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import progress_page
import quiz_
import Student_settings
import webbrowser
from tkinter import ttk
from ttkthemes import themed_tk as tk

class See_Homework():

    def __init__(self,GUI):
        GUI.destroy()
        self.list_of_lists=[]

    def See_hw(self,code):
        self.code=code

        self.window= tk.ThemedTk()
        self.window.geometry("625x315")
        self.window.wm_title("Complete Homework")

        self.window.get_themes()
        self.window.set_theme("radiance")

        hwk_title= ttk.Label(self.window,text=" Homework")
        hwk_title.config(font=("Calibri",40))
        hwk_title.grid(row=0,column=2,padx=50)

        self.add_menu(self.window,"Navigate", commands = [("Instructions",self.on_enter,True),("Quiz", self.Quiz_Page, True), ("Progress", self.Progress_Page, True),("MySFC", self.MYSFC, True),("Update Phone Number",self.Change_Phone,True),("Update Email Address",self.Change_Email,True)])#,("Log Out",self.LogOut(self.window),True)])

        style = ttk.Style()
        style.configure("mystyle.self.treeview", highlightthickness=0, bd=0, font=('Calibri', 12)) # Modify the font of the body
        style.configure("mystyle.self.treeview.Heading", font=('Calibri', 14,'bold')) # Modify the font of the headings
        #style.layout("mystyle.self.treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders

        #style.theme_use("aqua")
        self.tree= ttk.Treeview(self.window,columns=3,style="mystyle.Treeview")
        self.tree.grid(row=1,column=2,rowspan=2,columnspan=2,padx=10,pady=10)
        self.tree.heading('#0', text='Homework')
        self.tree.heading('#1', text='Deadline')
        self.tree.column("#0",width=280)
        self.tree.column("#1",width=280)


        vsb = ttk.Scrollbar(self.window, orient="vertical", command=self.tree.yview)
        vsb.grid(row=2,column=5,padx=5)
        self.tree.configure(yscrollcommand=vsb.set)

        self.Viewer()

        def OnDoubleClick(event):
            item = self.tree.selection()[0]
            value=self.tree.item(item,"values")[0]
            self.find_url(self.tree.item(item,"text"),str(value))

        self.tree.bind("<Double-1>",OnDoubleClick)

        conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        cur=conn.cursor()
        cur.execute("SELECT name FROM gclass WHERE code=%s",(self.code,))
        name= cur.fetchall()
        conn.close()
        self.name=name[0][0]

        self.window.mainloop()

    def find_url(self,title,deadline):
        conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        cur=conn.cursor()
        cur.execute("SELECT text FROM set_homework WHERE title=%s AND deadline=%s",(title,deadline))
        rows=cur.fetchall()
        conn.close()
        self.hw_section(title,rows[0][0])

    def hw_section(self,headtext,url):

        page=tk.ThemedTk()
        page.geometry("980x465")
        page.wm_title("Homework: " + headtext)

        page.get_themes()
        page.set_theme("radiance")


        r= requests.get(url)
        c= r.content

        soup= BeautifulSoup(c,"html.parser")

        h1=soup.find_all("h1")
        h2=soup.find_all("h2")
        al= soup.find_all("p")


        sec1= Text(page,height=25,width=55,borderwidth= 3,relief="sunken")
        sec1.grid(row=0,column=0,rowspan=6,padx=15,pady=10)

        sec2=Text(page,height=25,width=55,borderwidth= 3,relief="sunken")
        sec2.grid(row=0,column=2,rowspan=6,padx=15,pady=10)


        scrollb = ttk.Scrollbar(page, command=sec1.yview)
        scrollb.grid(row=3, column=1)
        sec1['yscrollcommand'] = scrollb.set

        def put():#
            sec1.delete("1.0",END)
            content=""
            for items in h1,h2,al:
                for item in range(0,len(items)):
                    sec1.insert(END,str(items[item].text))

        put()

        submit_frame= ttk.Frame(page)
        submit_frame.grid(row=7,column=0,rowspan=2,columnspan=4)

        submit_bn=ttk.Button(submit_frame,text="Submit",width=30,command= lambda: self.Send_Mail(url,sec2.get(1.0, "end-1c"),page))
        submit_bn.grid(row=8,column=2)

        page.mainloop()

    def Viewer(self):# Takes everything from the database to be displayed in a listbox
        conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        cur=conn.cursor()
        cur.execute("SELECT * FROM set_homework")
        rows= cur.fetchall()
        conn.close()
        self.get_list_of_lists(rows)
        print(rows)
        #Take disticntive homeworks

    def get_list_of_lists(self,list_of_tuples):
        for tuple in list_of_tuples:
            self.list_of_lists.append(list(tuple))
        print(self.list_of_lists)
        for l in range(0,len(self.list_of_lists)):
            if self.list_of_lists[l][0]== self.code:
                tag=" "+str(self.list_of_lists[l][3])
                self.tree.insert("","0",text=self.list_of_lists[l][1],values= self.list_of_lists[l][3],tags=(tag,))
                print(self.list_of_lists[l][3],type(self.list_of_lists[l][3]))
                print(dt.now(),type(dt.now()))
                #list_of_lists[l][3]= dt.strptime(list_of_lists[l][3].replace("-"," "), "%d %m %Y")
                if dt.now().date()> self.list_of_lists[l][3]:
                    self.tree.tag_configure(tag,background= "#FE140F")
                
                #Send messgage if deadline date is 1 day away
                time= dt.combine(self.list_of_lists[l][3], datetime.time.min)
                x=time- dt.now()
                duration_in_s = x.total_seconds()   
                days  = x.days   
                days  = int(divmod(duration_in_s, 86400)[0])
                #print(days)
                if days==1:
                    # Get phone number with self.code
                    conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
                    cur=conn.cursor()
                    cur.execute("SELECT phone FROM gclass WHERE code=%s",(self.code,))
                    number= cur.fetchall()
                    conn.close()
                    number= number[0][0]
                    # Send message

                    from twilio.rest import Client

                    account_sid= "ACf285e3bcd6b0a836086d3bb94997b738"
                    account_token= "1c4dea75e0341a289e4f7dba65384851"

                    client= Client(account_sid,account_token)

                    message= client.messages.create( 
                        to=number,
                        from_= "+‪441293344383‬",
                        body= "Only 1 day left before homework: " + self.list_of_lists[l][1] + "is due")
                    #print(message.sid)

    def Send_Mail(self,w_code,reply,window):
        with open("Homework.txt","w") as TextFile:
            TextFile.write("Done by: " + self.name + "(" + self.code + ") \n\n\n")
            TextFile.write(reply)

        server= smtplib.SMTP("smtp.gmail.com",587)
        server.ehlo()
        server.starttls()

        msg= MIMEMultipart()
        subject= "Homework from: " + self.name + "(" + self.code + ") \n\n\n"
        msg["Subject"]= subject
        msg["From"]="germanrevisestudy@gmail.com"
        msg["To"]= "v20726@gapps.stokesfc.ac.uk"## Teacher's email addr
        body= "Below is attached the file containing the homework"
        msg.attach(MIMEText(body,"plain"))

        f= open("Homework.txt","rb")
        #print(f)
        part= MIMEBase("application","octet-stream")
        part.set_payload((f).read())
        encoders.encode_base64(part)
        #attachment= MIMEText(f)
        part.add_header("Content-Disposition","attachment",filename= "Homework.txt")
        msg.attach(part)
        text= msg.as_string()

        server.login("germanrevisestudy@gmail.com","NuncaFumar01")

        server.sendmail("germanrevisestudy@gmail.com","v20726@gapps.stokesfc.ac.uk",text)
        server.quit()
        self.Delete(w_code,window)

    def Delete(self,web_code,w):
        conn=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        cur=conn.cursor()
        cur.execute("DELETE FROM set_homework WHERE text=%s", (web_code,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Succesful","Homework has been delivered successfully")
        w.destroy()
        self.window.destroy()
        self.See_hw(self.code)

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
    def Quiz_Page(self):
        quiz= quiz_.CompleteQuiz(self.name)
        quiz.ChooseQuiz(self.window)
    def Progress_Page(self):
        student_prog= progress_page.StudentProgress(self.code,self.window)
        student_prog.MainPage()
    def on_enter(self):
        messagebox.showinfo("Instructions", "Double click any homework to complete it. Once completed click submit \n If the homework is red it signifies that it's overdue")
    def Change_Email(self):
        student_changes= Student_settings.Student_Setting(self.code)
        student_changes.Change_Email(self.window)
    def Change_Phone(self):
        student_changes= Student_settings.Student_Setting(self.code)
        student_changes.Enter_New_Number(self.window)
    
    """def LogOut(self,page):
        log=login_page.Starting()
        log.login(page)"""

