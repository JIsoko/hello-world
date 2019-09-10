"""
Studnet will be able to change details such as email and phone. These latetr two will
have to be verified prior the actual update

"""
from tkinter import *
from ttkthemes import themed_tk as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from random import randint
import smtplib
import progress_page
import quiz_
import stud_hw
import webbrowser


class Student_Setting():

    def __init__(self,userid):
        self.times=0
        self.userid= userid
        # Get name of student
        conn= mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        c=conn.cursor()
        c.execute("SELECT name FROM gclass WHERE code=%s",(self.userid,))
        name= c.fetchall()
        conn.close()
        self.name= name[0][0]


    def Enter_New_Number(self,GUI):
        GUI.destroy()
        window= tk.ThemedTk()
        window.wm_title("Change Number- New Phone Number")
        window.geometry("405x64")
        window.get_themes()
        window.set_theme("radiance")

        new_number= ttk.Entry(window, width=20)
        new_number.insert(END,"New Phone Number")
        new_number.config(foreground="grey",font= ("Calibri", 16))
        new_number.grid(row=1,column=0,padx= 10,pady=13)

        self.add_menu(window,"Navigate", commands = [("Quiz", lambda: self.Quiz_Page(window), True), ("Progress", lambda: self.Progress_Page(window), True),("MySFC", self.MYSFC, True),("Update Email Address",lambda: self.Change_mail(window),True),("Do Homework",lambda: self.Homework(window),True)])

        def on_enter(event):
            self.times+=1
            if self.times==1:
                new_number.delete(0,END)

        new_number.bind("<<Button-1>>",on_enter)

        next_step= ttk.Button(window, text="Next Step",command=lambda: self.Verify_NewPhone(new_number.get(),window)).grid(row=1,column=1,padx=10,pady=8)

        window.mainloop()
    
    def Verify_NewPhone(self,phone_n,widget):
        print(phone_n)
        if len(phone_n)==11:
            widget.destroy()

            # Verification code
            verification_code=""
            for i in range(0,6):
                verification_code+= str(randint(0,9))

            verification_window= tk.ThemedTk()
            verification_window.wm_title("VERIFY- Phone Number")
            verification_window.geometry("410x64")
            verification_window.get_themes()
            verification_window.set_theme("radiance")

            code_entry= ttk.Entry(verification_window, width=20)
            code_entry.grid(row=1,column=0,padx= 10,pady=5)
            code_entry.insert(END,"e.g 123456")
            code_entry.config(foreground="grey",font= ("Calibri", 10))#Format of pin

            call_link = Label(verification_window, text="Prefer a call?", fg="blue", cursor="hand2")
            call_link.config(font=("Calibri",8))
            call_link.grid(row=2,column=0,padx=10)
            call_link.bind("<Button-1>", lambda e: self.Call(phone_n,code_entry))

            verify_b= ttk.Button(verification_window, text= "Verify",width=10,command= lambda: self.Verify(phone_n,code_entry.get(),verification_code))
            verify_b.grid(row=1,column=1,padx=3,pady=5)

            def on_enter(event):
                code_entry.delete(0,END)

            code_entry.bind("<Button-1>",on_enter)
                
            try_again_b=ttk.Button(verification_window,text="Send again",width=10,command= lambda: self.Send_Message(phone_n))
            try_again_b.grid(row=1,column=2,padx=2,pady=5)

            self.Send_Message(phone_n,verification_code)

            verification_window.mainloop()
        else:
            messagebox.showinfo("Invalid Number","Re-enter phone number as 07....")

    def Send_Message(self,number,ver_code):
        from twilio.rest import Client

        account_sid= "ACf285e3bcd6b0a836086d3bb94997b738"
        account_token= "1c4dea75e0341a289e4f7dba65384851"

        client= Client(account_sid,account_token)

        message= client.messages.create( 
            to=number,
            from_= "+‪441293344383‬",
            body= "Verification code: "+ver_code)
        #print(message.sid)

    def Verify(self,phone_number,input_code,ver_code):
        if ver_code== input_code:
            #Update
            self.Update_Phone(phone_number)
            messagebox.showinfo("UPDATE SUCCESSFUL","Update completed!!")
        else:
            messagebox.showerror("Wrong Pin", "Invalid Pin. Try again!")

    def Call_Option(number):
        from twilio.rest import Client

        try:

            account_sid= "ACf285e3bcd6b0a836086d3bb94997b738"
            account_token= "1c4dea75e0341a289e4f7dba65384851"

            client= Client(account_sid,account_token)

            call= client.calls.create(
                url='http://demo.twilio.com/docs/voice.xml',
                to=number,
                from_='+‪441293344383')

            #print(call.sid)
            self.Update_Phone(number)
            messagebox.showinfo("UPDATE SUCCESSFUL","Update completed!!")
                ###### TEMPORARY###### ENABLE to speak code that needs to be inserted
        except:
            messagebox.showerror("Try again","Call failed. Try again later")

    def Update_Phone(self,phone):
        try:
            conn= mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
            c=conn.cursor()
            c.execute("UPDATE gclass SET phone=%s WHERE code=%s",(phone,self.userId))
            conn.commit()
            conn.close()
            
        except:
            messagebox.showerror("Try again","Update failed. Try again later")
        

    def Change_Email(self,window):
        window.destroy()
        email_window= tk.ThemedTk()
        email_window.wm_title("Change Email address")

        email_window.get_themes()
        email_window.set_theme("radiance")
        
        email_window.wm_title("UPDATE EMAIL")
        email_window.geometry("450x110")

        self.add_menu(email_window,"Navigate", commands = [("Quiz", lambda: self.Quiz_Page(email_window), True), ("Progress", lambda: self.Progress_Page(email_window), True),("MySFC", self.MYSFC, True),("Update Phone Number",lambda: self.Change_Phone(email_window),True),("Do Homework",lambda: self.Homework(email_window),True)])#,("Log Out",self.LogOut(self.window),True)])

        email_e= ttk.Entry(email_window,width=30)
        email_e.grid(row=1,column=1,padx= 10,pady=5)
        email_e.insert(END,"Type Email address")        
        email_e.config(foreground="grey",font= ("Calibri", 14))
        re_email_e= ttk.Entry(email_window,width=30)
        re_email_e.grid(row=2,column=1,padx=10,pady=2)
        re_email_e.insert(END,"Retype Email address")
        re_email_e.config(foreground="grey",font= ("Calibri", 14))    

        def on_enter1(event):
            email_e.delete(0,END)

        def on_enter2(event):
            re_email_e.delete(0,END)

        email_e.bind("<Button-1>",on_enter1)
        re_email_e.bind("<Button-1>",on_enter2)

        next_step_b= ttk.Button(email_window,text="Next Step",width=10,command= lambda:self.Update_Email(email_e.get(),re_email_e.get()) ).grid(row=3,column=2,pady=3)

        email_window.mainloop()
        # Import function from registration to verify and validate email address
    def Update_Email(self,new_email,retyped_email):
        if new_email== retyped_email:
            try:
                conn= mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
                c=conn.cursor()
                c.execute("UPDATE gclass SET email=%s WHERE code=%s",(new_email,self.userId))
                conn.commit()
                conn.close()

                server= smtplib.SMTP("smtp.gmail.com",587)
                server.starttls()
                server.login("germanrevisestudy@gmail.com","NuncaFumar01")
                msg= "Revise & Study\n\n Email has been successfully updated!."
                subject= "Revise & Study: Email has been updated."
                body= "Subject: {} \n\n {}".format(subject,msg)

                server.sendmail("germanrevisestudy@gmail.com",new_email,body)
                server.quit()

                messagebox.showinfo("UPDATE SUCCESSFUL","Your email address has been successfully updated")
            except:
                messagebox.showerror("Try again","Update failed. Try again later")
        else:
            messagebox.showerror("Emails not matching","Make sure emails are equal!")
    
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
    def Quiz_Page(self,page):
        quiz= quiz_.CompleteQuiz(self.name)
        quiz.ChooseQuiz(page)
    def Progress_Page(self,page):
        student_prog= progress_page.StudentProgress(self.userid,page)
        student_prog.MainPage()
    def Homework(self,page):
        see_hw= stud_hw.See_Homework(page)
        see_hw.See_hw(self.userid)
    def Change_mail(self,page):
        self.Change_Email(page)
    def Change_Phone(self,page):
        self.Enter_New_Number(page)


