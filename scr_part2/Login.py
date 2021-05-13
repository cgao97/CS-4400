import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql

class Login(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Login", font=10)
        self.label.grid(row=0, column=0)
        
        self.username = tk.Label(self, text='Username')
        self.username.grid(row=1, column=0)
        
        self.e_username = tk.Entry(self)
        self.e_username.grid(row=1, column=1)

        self.passward = tk.Label(self, text='Password')
        self.passward.grid(row=2, column=0)
        
        self.e_password = tk.Entry(self, show='*')
        self.e_password.grid(row=2, column=1)

        self.login = tk.Button(self, text='Login', command=self.check_login)
        self.login.grid(row=3, column=0)
        
        self.register = tk.Button(self, text='Register', command=lambda: self.controller.show_frame(controller.Register))
        self.register.grid(row=3, column=1)
        
    def check_login(self):
        cur_user = self.e_username.get()
        if not cur_user:
            Msgbox.showerror("Error", "Username cannot be empty")
            return 1
        cur_password = self.e_password.get()
        if not cur_password:
            Msgbox.showerror("Error", "Password cannot be empty")
            return 1
        #print("SELECT Username FROM USERS WHERE Username = '%s' AND PASS = '%s'"%(cur_user, cur_password))
        cmd = "SELECT Username FROM USERS WHERE Username = %s AND PASS = %s"
        args = (cur_user, cur_password)
        self.controller.cursor.execute(cmd, args)
        this_user = self.controller.cursor.fetchone()
        if not this_user:
            Msgbox.showerror("Error", "Login Error")
            return 1
        
        self.controller.username = cur_user
        cmd = "SELECT * FROM CUSTOMER WHERE Username = %s"
        args = (cur_user,)
        print(args)
        self.controller.cursor.execute(cmd, args)
        if self.controller.cursor.fetchone():
            self.controller.show_frame(self.controller.CustomerHome)
        cmd = "SELECT * FROM DRONE_TECH WHERE Username = %s"
        args = (cur_user,)
        self.controller.cursor.execute(cmd, args)
        if self.controller.cursor.fetchone():
            self.controller.show_frame(self.controller.DroneTechnicianHome)
        
        cmd = "SELECT * FROM MANAGER WHERE Username = %s"
        args = (cur_user,)
        self.controller.cursor.execute(cmd, args)
        if self.controller.cursor.fetchone():
            self.controller.show_frame(self.controller.ChainManagerHome)
        
        cmd = "SELECT * FROM ADMIN WHERE Username = %s"
        args = (cur_user,)
        self.controller.cursor.execute(cmd, args)
        if self.controller.cursor.fetchone():
            self.controller.show_frame(self.controller.AdminHome)