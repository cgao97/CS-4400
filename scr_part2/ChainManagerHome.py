import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql

class ChainManagerHome(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Chain Manager Home")
        self.label.grid(row=0, column=0)

        self.view_tech = tk.Button(self, text="View Drone Technician",
                                   command=lambda: self.controller.show_frame('ChainManagerViewDroneTechnicians'))
        self.view_tech.grid(row=1, column=0)
        
        self.view_drones = tk.Button(
            self, text="View Drones", command=lambda: self.controller.show_frame('ChainManagerViewDrones'))
        self.view_drones.grid(row=1, column=1)
        
        self.create_chain_items = tk.Button(
            self, text="Create Chain Items", command=lambda: self.controller.show_frame('ChainManagerCreateChainItem'))
        self.create_chain_items.grid(row=2, column=0)
        
        self.manage_stores = tk.Button(
            self, text="Manage Stores", command=lambda: self.controller.show_frame('ChainManagerManageStores'))
        self.manage_stores.grid(row=2, column=1)
        
        
