from tkinter import *
import mysql.connector
from tkinter import ttk
import Set_hw
import teacher_progress
import set_revision 
from tkinter import font
from tkinter import messagebox
from ttkthemes import themed_tk as tk
from random import randint
import History


class Database():

    def __init(self):
        connection=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        c=connection.cursor()

    def create(self):
        connection=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        c=connection.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS gclass(name TEXT, surname TEXT,code VARCHAR(6) PRIMARY KEY,phone TEXT,email TEXT, password TEXT, salt TEXT, role TEXT,meg TEXT, year INT(1)) ")
        connection.close()

    def INSERTER(self,name,surname, code,phone, email, password, salt,role,meg,year):# Allows records to be inserted in the database
        connection=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        c=connection.cursor()
        c.execute("INSERT INTO gclass VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",((name,surname, code,phone, email, password, salt,role,meg,year)))
        connection.commit()
        connection.close()


    def Viewer(self):
        connection=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        c=connection.cursor()
        c.execute("SELECT code,name,surname,email,phone, meg FROM gclass")
        rows=c.fetchall()
        
        connection.close()
        return rows# Calls function that will store the content in lists of a list that can be indexed
        print(rows)

    def SEARCHER(self,code="",name= "", surname= "",meg=""):# Allows a record to be searched when at least one field has been inputted
        connection=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        c=connection.cursor()
        c.execute("SELECT code,name,surname,email,phone,meg FROM gclass WHERE name=%s OR code= %s OR surname= %s OR meg=%s ",(name,code, surname,meg))
        rows= c.fetchall()
        connection.close()
        return rows

    def DELETER(self,person):# Allows a record to be deleted making the person unavailable to access
        connection=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        c=connection.cursor()
        c.execute("DELETE FROM gclass WHERE code= %s", (person,))
        connection.commit()
        connection.close()

    def UPDATER(self,code, name, surname,meg):# Allows a field(s) to be updated
        connection=mysql.connector.connect(host="db4free.net",user="josephisoko01",password="Peter2001",db="germanclass")
        c=connection.cursor()
        c.execute("UPDATE gclass SET name= %s, surname=%s, meg=%s WHERE code= %s",(name, surname,meg,code))
        connection.commit()
        connection.close()

class teacher():

    def __init__(self,w):
        w.destroy()
        self.permission_password= "12345"
        self.selected_tuple=[]
        self.database=Database()
        self.database.create()
        self.check=False

    def registering_password(self):
        for i in range(0,10):
            self.permission_password+= str(randint(0,9))  
  

    def Teacher_Page(self,name):

        self.window= tk.ThemedTk()
        self.name= name
        self.window.wm_title(self.name.title())
        self.width=0
        for letter in range(len(self.name)):
            self.width+=20
        self.width+=600
        dimensions= str(self.width)+"x100"
        self.window.geometry(dimensions)
        print(self.name,self.width)
        
        self.window.get_themes()
        self.window.set_theme("radiance")
        """
        menubar = Menu(self.window)
        self.window.config(menu=menubar)
        menu = Menu(menubar, tearoff = 0)

        def add_menu(menuname, commands):
            for command in commands:
                menu.add_command(label = command[0], command = command[1])
                if command[2]:
                    menu.add_separator()

            menubar.add_cascade(label=menuname, menu=menu)

        def LoggingOut(page):
            log= login_page.Starting()
            log.login(page)
        """
        title_frame=ttk.Frame(self.window)
        title_frame.grid(row=0,column=0,columnspan=4)

        main_frame=ttk.Frame(self.window)
        main_frame.grid(row=2,column=0,rowspan=6,columnspan=4)

        title= ttk.Label(title_frame,text="Welcome back "+ self.name)# Add personalized welcome by passing as paramter list_of_lists[1](in login_page.py)
        title.grid(row=0,column=2,padx=65)
        title.config(font=("Courier",35))

        services= ttk.Combobox(main_frame,width=60)
        services["values"]= ("__________","Set Homework","Set Quiz","Progress","Manage Class","Assigned Material")
        services.grid(row=0,column=3,pady=5,padx=15)
        services.config(justify=CENTER)
        
        go=ttk.Button(main_frame,text="Go",width=5,command=lambda:self.go(services)).grid(row=0,column=4)

        self.window.mainloop()

    def go(self,cbox):
        print(cbox.get())
        if cbox.get()=="Set Homework":
            set_homew= Set_hw.Set_Homework(self.window)
            set_homew.Set_Homeworks()
        elif cbox.get()== "Set Quiz":
            set_quiz=set_revision.Revision(self.window) 
            set_quiz.Title()
        elif cbox.get()== "Progress":
            t= teacher_progress.TeacherProgress(self.window)
            t.MainPage()
        elif cbox.get()== "Manage Class":
            self.check=True
            self.Manage_class()
        elif cbox.get()== "Assigned Material":
            h=History.History(self.window)
            h.Main()
             

    def Manage_class(self):
        class_window= tk.ThemedTk()
        class_window.wm_title("MANAGE CLASS- SHOW MY HOMEWORK")
        class_window.geometry("708x380")
        
        class_window.get_themes()
        class_window.set_theme("radiance")

        if self.check== True:
            self.window.destroy()

        menubar = Menu(class_window)
        class_window.config(menu=menubar)

        def add_menu(menuname, commands):
            menu = Menu(menubar, tearoff = 0)

            for command in commands:
                menu.add_command(label = command[0], command = command[1])
                if command[2]:
                    menu.add_separator()

            menubar.add_cascade(label=menuname, menu=menu)

        def Progress_Student():
            t= teacher_progress.TeacherProgress(class_window)
            t.MainPage()
        
        def SetHW():
            set_hw= Set_hw.Set_Homework(class_window)
            set_hw.Set_Homeworks()
        
        def SetQuiz():
            set_quiz= set_revision.Revision(class_window)
            set_quiz.Title()

        def History_Link():
            #print("Trying the history link")
            h= History.History(class_window)
            h.Main()
        
        """def LogOut(page):
            log=login_page.Starting()
            log.login(page)"""

        add_menu("Navigate", commands = [("Progress", Progress_Student, True), ("Set Homework", SetHW, True),("Set Quiz", SetQuiz, True),("Assigned Work",History_Link,True)])#, ("Log Out",LogOut(class_window),True)])

        m_class=ttk.Label(class_window, text="Manage Class")
        m_class.grid(row=0,column=1,padx=8)
        m_class.config(font=("Courier",45))

        l1= ttk.Label(class_window, text= "Code")
        l1.grid(row= 1, column=0)
        l2= ttk.Label(class_window, text= "Name")
        l2.grid(row= 1, column=2)
        l3= ttk.Label(class_window, text= "Surname")
        l3.grid(row= 2, column=0)
        l4=ttk.Label(class_window,text="MEG")
        l4.grid(row=2,column=2)

        e1=ttk.Entry(class_window)
        e1.grid(row=1, column=1)
        e2=ttk.Entry(class_window)
        e2.grid(row=1, column=3)
        e3=ttk.Entry(class_window)
        e3.grid(row=2, column=1)
        e4=ttk.Combobox(class_window,width=16)
        e4["values"]= ("A*", "A","B","C","D","E","F","U")
        e4.grid(row=2,column=3,pady=2)

        #small_font = font.Font(family="Times",size=6)

        list1= Listbox(class_window, height=10, width= 50)#font= small_font)
        #list1.configure(justify=CENTER)
        list1.grid(row= 3, column=0, rowspan=7, columnspan=2,padx=10,pady=10)

        sb1=ttk.Scrollbar(class_window)
        sb1.grid(row=3,column=2, rowspan= 7)


        b1=ttk.Button(class_window, text= " Password" ,width= 12,  command= lambda:self.register_password())
        b1.grid(row=3, column=3)
        b2=ttk.Button(class_window, text= "Search", width= 12, command= lambda:self.search_command(list1,e1,e2,e3,e4))
        b2.grid(row=4, column=3)
        b3=ttk.Button(class_window, text= "Update",width= 12,  command= lambda:self.update_command(list1,e1,e2,e3,e4))
        b3.grid(row=5, column=3)
        b4=ttk.Button(class_window, text= "Delete",width= 12,  command= lambda:self.delete_command(list1))
        b4.grid(row=6, column=3)
        b5=ttk.Button(class_window, text= "View", width= 12, command= lambda:self.view_command(list1))
        b5.grid(row=7, column=3)
        b6=ttk.Button(class_window,text= "Close",width= 12,  command= class_window.destroy)
        b6.grid(row=8, column=3)


        def get_selected_row(event):# When a record in the listbox is clicked, the data will go in the appropriate entry boxes
            index= list1.curselection()
            self.selected_tuple= list1.get(index)
            print(self.selected_tuple)
            e1.delete(0,END)
            e1.insert(END,self.selected_tuple[0])
            e2.delete(0,END)
            e2.insert(END,self.selected_tuple[1])
            e3.delete(0,END)
            e3.insert(END,self.selected_tuple[2])
            e4.delete(0,END)
            e4.insert(END,self.selected_tuple[-1])

        list1.configure(yscrollcommand= sb1.set)# Binding the listbox to the scrollbar amd viceversa in the following line
        sb1.configure(command= list1.yview)
        list1.bind('<<ListboxSelect>>',get_selected_row)# Defining the event(clicking the listbox)

        class_window.mainloop()


    def view_command(self,lb):# Displays content in listbox
        lb.delete(0,END)
        for row in self.database.Viewer():
            print(row)
            if row[0][0].upper()== "V":
                lb.insert(END,row)

    def register_password(self):
        #self.registering_password()
        messagebox.showinfo("Registering Password","                                    "+ self.permission_password+ "\n" + "Show to students who want to register and put as password when logging in ")

    def search_command(self,lb,entry1,entry2,entry3,entry4):
        lb.delete(0,END)
        for row in self.database.SEARCHER(entry1.get(),entry2.get(),entry3.get(),entry4.get()) :
            lb.insert(END,row)

    def delete_command(self,lb):
        self.database.DELETER(self.selected_tuple[0])#self.selected_tuple[0] is the code field of whatever record is clicked from the listbox
        messagebox.showinfo(" Deletion Successful ", "Student record has been succesfully deleted")
        self.view_command(lb)


    def update_command(self,lb,entry1,entry2,entry3,entry4):
        try:
            print(self.selected_tuple[0])
            if self.selected_tuple[0][0].upper()== "V" or self.selected_tuple[0][0].upper()=="T":#Verification and validaton for data entry
                for letters in range(0,len(entry2.get())):# Add warning messageboxes for wrong entry
                    if 65<= ord(entry2.get()[letters].upper()) <= 90:
                        for letters in range(0,len(entry3.get())):
                            if 65<= ord(entry3.get()[letters].upper()) <= 90:
                                if  ord(str(entry4.get()))== "A*" or 65<=ord(str(entry4.get())) <=70 or ord(str(entry4.get())).upper()== "U":
                                    self.database.UPDATER(self.selected_tuple[0],entry2.get(),entry3.get(),entry4.get())    # issue with updating to A*   
                            else:
                                entry3.delete(0,END)
                                messagebox.showinfo("Wrong Entry","Check your entries")
                                entry3.configure({"background":"#DC231F"})
                    else:
                        entry2.delete(0,END)
                        messagebox.showinfo("Wrong Entry","Check your entries")
                        entry2.configure({"background":"#DC231F"})

            else:
                entry1.delete(0,END)
                messagebox.showinfo("Wrong Entry","Check your entries")
                eentry1.configure({"background":"#DC231F"})
        except Exception as e:
            print(e)
            messagebox.showinfo("Procedure failed. Try again later")

        messagebox.showinfo("Updating Successful", "Student record has been succesfully updated")
        self.view_command(lb)


#te=teacher()
#te.Teacher_Page("Giuseppe")