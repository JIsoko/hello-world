import mysql.connector # To connect to the database
import hashlib, uuid   # To hash a password
import smtplib         #TO send emails
from tkinter import *  #To create user interface
from tkinter import ttk
from tkinter import messagebox
import Student #Student section imported
import Teacher #Teacher section imported
from validate_email import validate_email #To validate an email address
from ttkthemes import themed_tk as tk # To select and use a theme

class Starting():

    def Intro_Page(self):
        self.start_page=Tk()
        self.start_page.wm_title("Intro") #Name of the window is "Intro"
        self.start_page.geometry("680x300") #Sizing of the window

        #Logo which is showing by placing it on a label
        intro_la= Label(self.start_page)
        intro_logo=PhotoImage(file="Actual_logo.png")
        intro_la.config(image= intro_logo)
        intro_la.grid(row=1,column=1)

        Label(self.start_page,text="Double click to continue...").grid(row=0,column=1)

        #Allows an event to occur, namely that after doubleclicking another function runs
        self.start_page.bind("<Double-1>",self.OnDoubleClick)
        
        self.start_page.mainloop()

    def OnDoubleClick(self,event):
        #Function for the login page is run
        logging= Login(self.start_page)
        logging.login()

class Login():
    def __init__(self,page):
        self.check= False #Used to check if user has inserted wrong/invalid login details. If True, they're wrong
        self.check2= False #Used to check if user has inserted wrong/invalid registration code. If True, they're wrong
        self.list_of_lists=[] #Used to store the details from the database
        page.destroy()

    def login(self):

        self.window=tk.ThemedTk() # Window is created
        self.window.wm_title("Login/Register") #Name of the window
        self.window.geometry("530x190") #Sizing of the window

        self.window.get_themes() #Allows access to themes
        self.window.set_theme("radiance") #Theme:radiance is being used

        #Setting up of the notebook containing the login and register tabs
        tab_control = ttk.Notebook(self.window,style='Custom.TNotebook')
 
        tab1 = ttk.Frame(tab_control)
        
        tab2 = ttk.Frame(tab_control)
        
        tab_control.add(tab1, text='LOGIN')
        
        tab_control.add(tab2, text='REGISTER')

        tab_control.grid(row=0,column=1,padx=50)

        #Tab1 is the login Tab with an entrybox for the username and the other for the password
        self.log= ttk.Entry(tab1,width= 45)
        self.log.grid(row=1,column=1,pady=10,padx=10)
        self.log.config(justify=CENTER,font=("Courier",10))  #Adjusting size and font in entry box

        self.password_e= ttk.Entry(tab1, width=45,show="*")
        self.password_e.grid(row=3,column=1,pady=5)
        self.password_e.config(justify=CENTER,font=("Courier",10)) #Adjusting size and font in entry box

        #Label that links to another section that deals with password recovery via phone messages/calls
        link1 = Label(tab1, text="Forgot your login?", fg="blue",font="Calibri 9",cursor="hand2")
        link1.grid(row=4,column=1)
        link1.bind("<Button-1>", lambda e: self.Restore_UserID(self.window))

        #Tab2 is the registration Tab with an entrybox for the registration code given by the teacher
        code_e= ttk.Entry(tab2, width=45)
        code_e.grid(row=3,column=1,pady=30)
        code_e.config(justify=CENTER,font=("Courier",10))  #Adjusting size and font in entry box

        #Menu with button that offers the instructions as to how login and register. Function is further down
        self.add_menu(self.window,"Instructions", commands = [("Instructions",self.on_enter,True)])

        #Login Button in Tab1
        login= ttk.Button(tab1, text= "LOGIN",width=45,command= lambda:self.LogginIn(self.log.get(),self.password_e.get()))
        login.grid(row=5,column=1,padx=10,pady= 11)

        #Register button in Tab2
        register_f= ttk.Button(tab2, text= "Register Form",width=45,command= lambda:self.Register(code_e.get()))
        register_f.grid(row=5,column=1,padx=10,pady= 11) 

        #Reports back if user inserted wrong/invalid details and deals with it by clearing the respective entry boxes
        if self.check== True :
            self.password_e.delete(0,END) #Clears entry box
        if self.check2== True:
            code_e.delete(0,END) #Clears entry box

        self.window.mainloop()  

    
        
    def LogginIn(self,userID,password):
        print(userID,password)
        self.view() # Gets all the content from the gclass table containing login details
        teac= Teacher.teacher(self.window)  #Instantation of the Teacher class from the teacher section
        checker=1 # This is used to know when to stop comparing preventing the list getting out of index
        for item in range(0,len(self.list_of_lists)):
            if userID.upper()== self.list_of_lists[item][2]: #Compares username provided with all usernames in db. Username is the third element in each db record
                print("Correct UserID")
                pass_check = hashlib.sha512(password.encode("utf-8") + str(self.list_of_lists[item][6]).encode("utf-8")).hexdigest() # password provided is hashed salted with salt from db record since passwords are stored in such a way
                print(self.list_of_lists[item][7].upper())
                if pass_check[:9]== str(self.list_of_lists[item][5]) and str(self.list_of_lists[item][7]).upper()=="STUDENT":#Compares hashed password provided with actual password and checks role of used: Student or Teacher
                    stud= Student.student(self.list_of_lists[item][0]) #Instantation of Student class from Student section. It requires the name to be passed on as parameter
                    stud.StudentPage()
                    break
                elif pass_check[:9]== str(self.list_of_lists[item][5]) and str(self.list_of_lists[item][7]).upper()== "TEACHER":#Compares hashed password provided with actual password and checks role of used: Student or Teacher
                    print("Got here")
                    teac.Teacher_Page(self.list_of_lists[item][0]) #It requires the name to be passed on as parameter
                    break
                else:
                    self.check=True # Check becomes true indicating invalid details
                    self.login()
            else:
                checker+=1
        if checker>len(self.list_of_lists):
            print("Incorrect UserID")
            self.check=True
            self.login()

    def Register(self,password):
        teac= Teacher.teacher(self.window)
        print(teac.permission_password)
        if password==teac.permission_password:
            role = "Student"
            reg= Registration()
            reg.register_form(role)
            #Open Registration form
        else:
            self.check2=True
            self.login()

    #Selects everything from gclass table
    def view(self):
        connection=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        c=connection.cursor()
        c.execute("SELECT * FROM gclass")
        rows=c.fetchall()
        connection.close()
        self.get_list_of_lists(rows)# Calls function that will store the content in lists of a list that can be indexed

    #Turns the tuples from the database into lists which are more flexible
    def get_list_of_lists(self,list_of_tuples):
        for tuple in list_of_tuples: 
            self.list_of_lists.append(list(tuple)) 
        print(self.list_of_lists)
    
    #Deals with the menubar used in the login page
    def add_menu(self,window_name,menuname, commands):
        menubar = Menu(window_name)
        window_name.config(menu=menubar)
        menu = Menu(menubar, tearoff = 0)

        for command in commands:
            menu.add_command(label = command[0], command = command[1])
            if command[2]:
                menu.add_separator()

        menubar.add_cascade(label=menuname, menu=menu)

    def on_enter(self):
        messagebox.showinfo("Instructions", " Login: Enter UserID and password in the boxes in this order \n \n Register: Ask teacher for admission code and enter code in  box in the register section")


    def Restore_UserID(self,frame):
        frame.destroy()
        # Restore password and userid by asking for Name and Surname.
        window= tk.ThemedTk()

        window.get_themes()
        window.set_theme("radiance")

        reg= Registration()
        
        window.wm_title("RESTORE-USERID & PASSWORD")
        window.geometry("360x100")
        
        #Entry boxes for the name and surname
        name_e= ttk.Entry(window,width=30)
        name_e.grid(row=1,column=1,padx= 10,pady=5)
        #Example is insetrted so user knows what it expects
        name_e.insert(END,"e.g John")   
        #Styling of name entry box     
        name_e.config(foreground="grey",font= ("Calibri", 10))
        surname_e= ttk.Entry(window,width=30)
        surname_e.grid(row=2,column=1,padx=10,pady=2)
        #Example is insetrted so user knows what it expects
        surname_e.insert(END,"e.g Smith")
        surname_e.config(foreground="grey",font= ("Calibri", 10))    

        #When user enters entry box, the example are cleared so user can type entries
        def on_enter1(event):
            name_e.delete(0,END)

        #When user enters entry box, the example are cleared so user can type entries
        def on_enter2(event):
            surname_e.delete(0,END)

        def find_user():
            try:# Try is used in case entries are invalid, so using this errors can be handles
                conn= mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
                c=conn.cursor()
                #Seeaches and seleects username using the name and surname provided previously
                c.execute("SELECT code FROM gclass WHERE name=%s and surname=%s",(name_e.get(),surname_e.get()))
                user_c= c.fetchall()
                conn.close()
                user_c= user_c[0][0]
                #Runs fuction which is the next step for password recuperation
                reg.Phone_Verification(window,user_c)
            except:
                name_e.delete(0,END) #Clears entry box
                surname_e.delete(0,END) #Clears entry box
                messagebox.showerror("User not found","User not found in the database. Ensure name and surname are correct!")

        next_step_b= ttk.Button(window,text="Next Step",width=10,command= find_user ).grid(row=3,column=2,pady=3)


        name_e.bind("<Button-1>",on_enter1)#Binds entry box so that when clicked a function is run

        surname_e.bind("<Button-1>",on_enter2)#Binds entry box so that when clicked a function is run

        window.mainloop()

    
    def Restore_Password(self,code):
        window= tk.ThemedTk()
        window.wm_title("RESTORE-USERID & PASSWORD")
        window.geometry("510x150")
       

        window.get_themes()
        window.set_theme("radiance")

        #Username is clearly shown after identity has been proven

        userd_id= ttk.Label(window,text=" UserId: "+code.upper())
        userd_id.grid(row=1,column=2,padx= 10,pady=5)
        userd_id.config(font=("Calibri",20))

        #Labels and entry boxes so that user can make another password
        l1= ttk.Label(window,text=" Type New Password").grid(row=2,column=1,padx= 10,pady=5)
        l2= ttk.Label(window,text=" Retype New Password").grid(row=3,column=1,padx= 10,pady=5)
            
        new_pass= ttk.Entry(window,width=30,show="*")
        new_pass.grid(row=2,column=2,padx=10,pady=2)

        retype_pass=  ttk.Entry(window,width=30,show="*")
        retype_pass.grid(row=3,column=2,padx=10,pady=2)

        next_step_b= ttk.Button(window,text="Finish",width=10,command=lambda: self.Update_Password(code,new_pass,retype_pass,window)).grid(row=4,column=3,pady=3)

        #Allows that when clicked entry box is cleared from its example
        def on_enter1(event):
            new_pass.delete(0,END)

        #Allows that when clicked entry box is cleared from its example
        def on_enter2(event):
            retype_pass.delete(0,END)

        new_pass.bind("<Button-1>",on_enter1)#Allows that when clicked entry box is cleared from its example

        retype_pass.bind("<Button-1>",on_enter2)#Allows that when clicked entry box is cleared from its example

        window.mainloop()

    def Update_Password(self,user,new_password,re_new_password,frame):
        if new_password.get()== re_new_password.get(): #Compares two passwords provided
            conn= mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
            c=conn.cursor()
            new_salt = uuid.uuid4().hex
            new_hashed_password = hashlib.sha512(new_password.get().encode("utf-8") + new_salt.encode("utf-8")).hexdigest() # Encodes new password by adding salt and then hashing it
            c.execute("UPDATE gclass SET password=%s, salt=%s WHERE code=%s",(new_hashed_password[:9],new_salt,user)) #Password is updated
            conn.commit()
            conn.close()
            print("Success")
            messagebox.showinfo("Password update","Password has been updated successfully")#User is alerted of success
            frame.destroy() #Window is destroyed and user returns to login page
            self.login()
        else:
            new_password.delete(0,END)
            re_new_password.delete(0,END)
            messagebox.showerror("Passwords do not match","New passwords don't match. Try again!")
            
class Registration():
    
    def __init__(self):
        self.times=True # Variable that prevents someone registering twice. Once details are submitted it becomes False
        self.next_step=False # Used to distinguish when the function is called from password recovery or registration step2
    
    def register_form(self,roles):
        register= tk.ThemedTk() # Themed window created
        register.wm_title("REGISTER- SHOW MY HOMEWORK") #Title assigned to window
        register.geometry("270x380")# Sizing of window
        register.get_themes() 
        register.set_theme("radiance")

        #Title 
        title_= ttk.Label(register, text=" REGISTER")
        title_.grid(row=0,column=0,pady=15)

        #Entry boxes for registration inputs
        code_e= ttk.Entry(register,width=40)
        code_e.grid(row=1,column=0,pady=5,padx=5)
        code_e.config(justify=CENTER) #Entries are centered
        name_e= ttk.Entry(register,width=40)
        name_e.grid(row=3,column=0,pady=5,padx=5)
        name_e.config(justify=CENTER)
        surname_e= ttk.Entry(register,width=40)
        surname_e.grid(row=5,column=0,pady=5,padx=5)
        surname_e.config(justify=CENTER)
        phone_e= ttk.Entry(register,width=40)
        phone_e.grid(row=7,column=0,pady=5,padx=5)
        phone_e.config(justify=CENTER)
        meg_e= ttk.Combobox(register,width=38) # Entry box with predefined options
        meg_e["values"]= ("A*", "A","B","C","D","E","F","U") #Possible grades
        meg_e.grid(row=9,column=0,pady=5,padx=5)
        meg_e.config(justify=CENTER)
        password_e= ttk.Entry(register,width=40,show="*")
        password_e.grid(row=11,column=0,pady=5,padx=5)
        password_e.config(justify=CENTER)
        re_password_e= ttk.Entry(register,width=40,show="*")
        re_password_e.grid(row=13,column=0,pady=5,padx=5)
        re_password_e.config(justify=CENTER)
        email_e= ttk.Entry(register,width=40)
        email_e.grid(row=15,column=0,pady=5,padx=5)
        email_e.config(justify=CENTER)
        year_e= ttk.Combobox(register,width=38) # Entry box with predefined options
        year_e["values"]= (1,2) #Possible years: EIther First year student or second year
        year_e.grid(row=17,column=0,pady=5,padx=5)
        year_e.config(justify=CENTER)

        #Labels are placed within each respective entry box to indicate what sort of entry is expected e.g "UserID" on first entry box
        entries= [code_e,name_e,surname_e,phone_e,meg_e,password_e,re_password_e,email_e,year_e]
        labels= ["UserID","Name","Surname","Phone Number","MEG","Type Password","Retype Password","Email Address","Year"]
        for i in range(0,len(entries)):
            entries[i].insert(END,labels[i] )

        #As user clicks entry box, entry boxes are cleared allowing the user to write
        def on_enter(event):
            time=0 #So that clearing of entry box is only once
            for i in range(0,len(entries)):
                if time==0:
                    entries[i].delete(0,END)
                    time= 1

        #Binds each entry box to the event that runs on_enter when user clicks an entry box 
        for i in range(0,len(entries)):
            entries[i].bind("<Button-1>", on_enter)

        register_b= ttk.Button(register,text= "Register",width=25,command= lambda: self.check(code_e,name_e,surname_e,phone_e,meg_e,password_e,re_password_e,email_e,year_e,register,roles))
        register_b.grid(row=18,column=0,pady= 10)

        register.mainloop()

    #Verification for entry of data from the register form. If data is wrong, warning messagebox is displayed.
    def check(self,e1,e2,e3,e4,e5,e6,e7,e8,e9,w,r):
        if e1.get()[0].upper()== "V" or e1.get()[0].upper()=="T" and len(e1.get())==6: # All college userids start with V or T
            for letters in range(0,len(e2.get())):
                if 65<= ord(e2.get()[letters].upper()) <= 90: # Checking that no numbers are used by checking the ASCII value
                    for letters in range(0,len(e3.get())):
                        if 65<= ord(e3.get()[letters].upper()) <= 90:# Checking that no numbers are used by checking the ASCII value
                            if len(e4.get())>10 and len(e4.get())<14:
                                for num in range(1,len(e4.get())):# Starts from second position as some numbers start with character +
                                    if int(e4.get()[num])/2>-1 and len(e4.get())== 11:# Checking that no characters are used and that length is correct
                                        if str(e5.get())== "A*" or 65<=ord(str(e5.get())) <=70 or str(e5.get()).upper()== "U": # Checking that grade is within the possible grades
                                            if e6.get()== e7.get(): #Password and retyped password must match
                                                val= 0 
                                                for i in range(0,1):
                                                    if self.Email_Checker(e8.get()): # If email is valid True is returned
                                                        val=1
                                                        if val==1:
                                                            if int(e9.get())== 1 or int(e9.get())==2: #Checking that year is within possible college years
                                                                salt_e = uuid.uuid4().hex
                                                                hashed_password = hashlib.sha512(e6.get().encode("utf-8") + salt_e.encode("utf-8")).hexdigest() #Password is salted and hashed
                                                                try:
                                                                    if self.times==True:
                                                                        print("Inserting")
                                                                        print((e2.get(),e3.get(),e1.get(),e4.get(),e8.get(),hashed_password[:9],str(salt_e),r,e5.get(),e9.get()))
                                                                        self.reg_data=[e2.get(),e3.get(),e1.get(),e4.get(),e8.get(),hashed_password[:9],str(salt_e),r,e5.get(),e9.get()]
                                                                        self.next_step= True
                                                                        self.Phone_Verification(w," ") #Takes in a window. 2nd parameter blank as it's for the user id used in the password recovery
                                                                        self.times=False
                                                                except Exception as e:
                                                                    print(str(e))
                                                                    if self.times==True:
                                                                        print("Show error")
                                                                        messagebox.showinfo("Registration failed","Try again later")
                                                                        self.times=False
                                                            else:
                                                                self.Alert(e9)
                                                if val==0:
                                                    self.Alert(e8)
                                            else:
                                                self.Alert(e6)
                                                self.Alert(e7)

                                        else:
                                            self.Alert(e5)
                                    else:
                                        self.Alert(e4)
                            else:
                                self.Alert(e3)
                        else:
                            self.Alert(e3)
                else:
                    self.Alert(e2)
        else:
            self.Alert(e1)

    #Here phones are verified for registration or as part of password recovery process
    def Phone_Verification(self,GUI,user_code):
        GUI.destroy() #Previous window is removed
            
        print("Verification part")
        from random import randint #Library that deals with generation of random numbers

        #Code that is messaged is random    
        verification_code=""
        for i in range(0,6): #The verification is of 5 numbers
            verification_code+= str(randint(0,9))

        if self.next_step== True: # Means that the function has been called from the registration and not the password recovery
            phone_n= "+44"+self.reg_data[3][1:] #Phone number 
            print(phone_n)
        else: #Means function called from password recovery
            conn= mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
            c=conn.cursor()
            c.execute("SELECT phone FROM gclass WHERE code=%s",(user_code,)) #Phone number is selected using the user id
            row= c.fetchall() #Fetches query
            conn.close()
            phone_n= row[0][0] # Indexing to get the number

        window= tk.ThemedTk()
        window.wm_title("VERIFY- Phone Number")
        window.geometry("395x64")
        window.get_themes()
        window.set_theme("radiance")

        #Entry box where user will insert verification code received
        code_entry= ttk.Entry(window, width=20)
        code_entry.grid(row=1,column=0,padx= 10,pady=5)
        code_entry.insert(END,"e.g 123456") #Example of a verification code is shown

        #Alternative link that offers a phone call rather than a message
        call_link = Label(window, text="Prefer a call?", fg="blue", cursor="hand2")
        call_link.config(font=("Calibri",8))
        call_link.grid(row=2,column=0,padx=10)
        call_link.bind("<Button-1>", lambda e: self.Call(phone_n,code_entry))

        verify_b= ttk.Button(window, text= "Verify",width=10,command= lambda: self.Verify(code_entry,verification_code,window,user_code))
        verify_b.grid(row=1,column=1,padx=3,pady=5)

        #When user clicks entrybox, it's cleared
        def on_enter(event):
            code_entry.delete(0,END)

        #Binds entry box to click event
        code_entry.bind("<Button-1>",on_enter)
            
        try_again_b=ttk.Button(window,text="Send again",width=10,command= lambda: self.Send_Text(phone_n,verification_code))
        try_again_b.grid(row=1,column=2,padx=2,pady=5)

        self.Send_Text(phone_n,verification_code)

        window.mainloop()

    #Checks that code inserted matches verification code
    def Verify(self,input_box,code,frame,user):
        if self.next_step== True: #Distinguishes whether as part of registration or password recovery
            if input_box.get()== code: #Compares codes
                print("Phone Number valid")
                self.INSERTER(self.reg_data[0],self.reg_data[1],self.reg_data[2],self.reg_data[3],self.reg_data[4],self.reg_data[5],self.reg_data[6],self.reg_data[7],self.reg_data[8],self.reg_data[9])
                messagebox.showinfo("SIGNED UP","Registration complete. Don't forger your password!")
                Logging= Login(frame) # Login page is shown as registration is complete
                Logging.login()
            else:
                input_box.config({"background":"#DC231F"})
        else:
            if input_box.get()==code:
                print("Phone N valid")
                #Openz page containing last step of password recovery
                restore= Login(frame)
                restore.Restore_Password(user)
            else:
                input_box.config({"background":"#DC231F"})


    def Send_Text(self,phone_number,code):
        from twilio.rest import Client #Library that deals with communication

        #Twilio account details
        account_sid= "" 
        account_token= ""

        #Access to twilio account
        client= Client(account_sid,account_token)

        #Message sent to user via text message
        message= client.messages.create( 
            to=phone_number,
            from_= "+‪441293344383‬", #Twilio phone number
            body= "Verification code: "+code)
    
    def Call(self,phone_num,input_box):
        from twilio.rest import Client #Library that deals with communication

        #Twilio account details
        account_sid= ""
        account_token= ""
        
        #Accessing twilio account
        client= Client(account_sid,account_token)

        try: #Call is attempted 
            call= client.calls.create(
                url='http://demo.twilio.com/docs/voice.xml', #Contains xml script that deals with response once user picks up
                to='++447710601096',
                from_='+‪441293344383')

            if self.next_step== True: # Checks if function is ran as part of registration
                self.INSERTER(self.reg_data[0],self.reg_data[1],self.reg_data[2],self.reg_data[3],self.reg_data[4],self.reg_data[5],self.reg_data[6],self.reg_data[7],self.reg_data[8],self.reg_data[9])
                messagebox.showinfo("SIGNED UP","Registration complete. Don't forger your password!")
                Logging= Login(frame)
                Logging.login()
                ###### TEMPORARY###### ENABLE to speak code that needs to be inserted

        except:
            input_box.config(({"background":"#DC231F"}))

    #Checks email verification by attempting to send an email to the email provided
    def Email_Checker(self,email):
        if validate_email(email)== True: #Checks validation of email 
            try:
                server= smtplib.SMTP("smtp.gmail.com",587) #Accessing gmail server via port 587
                server.starttls()
                server.login("germanrevisestudy@gmail.com","NuncaFumar01") #Logging in gmail email account
                #Message and subject of email 
                msg= "This is an email send to verify this email address."
                subject= "Email Verification"
                body= "Subject: {} \n\n {}".format(subject,msg)

                #Email is sent
                server.sendmail("germanrevisestudy@gmail.com",email,body)
                server.quit()
                x=True 
                return x 
            except:
                x=False
                return x
        else:
            x=False
            return x


    def INSERTER(self,name,surname,userid,phone,email,password,salt,role,meg,year):
        if self.times==1:
            conn= mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
            c=conn.cursor()
            c.execute("INSERT INTO gclass VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,surname,userid,phone,email,password,salt,role,meg,year)) #Inserts new user's data in db
            conn.commit()
            conn.close()

            #Welcoming email is sent
            server= smtplib.SMTP("smtp.gmail.com",587) #Access to gmail server
            server.starttls()
            server.login("germanrevisestudy@gmail.com","NuncaFumar01") #logging into email account
            #Message is formulated
            msg= "Welcome "+name.title() +" to Revise & Study.\n\n As a student you will be able to complete homework and revise through various quizzes."
            subject= "Welcome "+name.title() +" to Revise & Study"
            body= "Subject: {} \n\n {}".format(subject,msg)
            
            #Email is sent
            server.sendmail("germanrevisestudy@gmail.com",email,body)
            server.quit()

    #Deals with showing error when an invalid entry is inserted in the registration form
    def Alert(self,box):
        box.delete(0,END)
        messagebox.showinfo("Wrong Entry","Check your entries")

Log= Starting()
Log.Intro_Page()

#Challenge
#Write xml file to speak verification code

#Issues


#To do
#Ask twice before hoemwork is submitted( try messagebox)
#Credit icons @ <div>Icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/"             title="Flaticon">www.flaticon.com</a></div>

#Potential improvements
