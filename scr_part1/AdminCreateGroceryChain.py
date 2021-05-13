import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql

class AdminCreateGroceryChain(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Admin Create Grocery Chain")
        self.label.grid(row=0, column=1)
        
        self.chain_name = tk.Label(self, text="Grocery Chain Name")
        self.chain_name.grid(row=1, column=1)
        
        self.e_chain_name = tk.Entry(self)
        self.e_chain_name.grid(row=1, column=2)
        
        self.back = tk.Button(self, text="Back", command=lambda: self.controller.show_frame(self.controller.AdminHome))
        self.back.grid(row=3, column=0)
        
        self.create = tk.Button(self, text="Create", command=self.create_chain)
        self.create.grid(row=3, column=3)
        
    def create_chain(self):
        if not self.e_chain_name.get():
            Msgbox.showerror("Error", "All fields are required")
            return 1
        cmd = "SELECT * FROM CHAIN WHERE ChainName = %s"
        args = (self.e_chain_name.get(),)
        self.controller.cursor.execute(cmd, args)
        
        if self.controller.cursor.fetchone():
            Msgbox.showerror("Error", "Chain already exists")
            return 1
        try:
            cmd = "INSERT INTO CHAIN VALUES (%s)"
            args = (self.e_chain_name.get(),)
            print(cmd%args)
            self.controller.cursor.execute(cmd, args)
            Msgbox.showinfo("Message", "Success")
        except:
            Msgbox.showerror("Error", "Invalid Input")
            