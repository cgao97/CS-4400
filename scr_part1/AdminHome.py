import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql

class AdminHome(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Admin Home")
        self.label.grid(row=0, column=0)

        self.create_item = tk.Button(self, text="Create Item", command=None)
        self.create_item.grid(row=1, column=0)
        
        self.create_drone = tk.Button(self, text="Create Drone", command=None)
        self.create_drone.grid(row=1, column=1)
        
        self.view_cust = tk.Button(self, text="View Customer Info", command=lambda: self.controller.show_frame(self.controller.AdminViewCustomers))
        self.view_cust.grid(row=2, column=0)
        
        self.create_grocery_chain = tk.Button(self, text="Create Grocery Chain", command=lambda: self.controller.show_frame(self.controller.AdminCreateGroceryChain))
        self.create_grocery_chain.grid(row=2, column=1)
        
        create_store = tk.Button(self, text="Create Store", command=lambda: self.controller.show_frame(self.controller.AdminCreateStore))
        create_store.grid(row=2, column=2)