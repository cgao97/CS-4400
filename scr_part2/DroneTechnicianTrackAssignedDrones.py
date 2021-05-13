import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql
from tkinter import ttk

STATUS = ["All", "Available", "Busy"]

class DroneTechnicianTrackAssignedDrones(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.label = tk.Label(self, text="My Assigned Drones")
        self.label.grid(row=0, column=1)
        
        self.droneid = tk.Label(self, text="Drone ID: ")
        self.droneid.grid(row=1, column=0)
        
        self.e_droneid = tk.Entry(self)
        #self.e_firstname.config(fg = 'grey')
        self.e_droneid.grid(row=1, column=1)
        
        self.status = tk.Label(self, text="Status")
        self.status.grid(row=1, column=2)
        
        self.e_status = tk.StringVar()
        self.status_menu = ttk.Combobox(self, textvariable=self.e_status, values=STATUS, state="readonly")
        self.status_menu.grid(row=1, column=3)
        self.status_menu.set('All')
        self.e_status.set(self.status_menu.get())
        
        self.tv = ttk.Treeview(self, column=(0,1,2), show='headings')
        #self.tv['show'] = 'headings'
        self.tv.grid(row=2, column=0, columnspan=4)
        self.tv.heading("0", text="Drone ID", command=lambda:self.sort_column(self.tv, '0'))
        self.tv.column("0", width=120, stretch=tk.NO)
        self.tv.heading("1", text="Status", command=lambda:self.sort_column(self.tv, '1'))
        self.tv.column("1", width=120, stretch=tk.NO)
        self.tv.heading("2", text="Radius", command=lambda:self.sort_column(self.tv, '2'))
        self.tv.column("2", width=120, stretch=tk.NO)
        
        self.scoll = ttk.Scrollbar(self, orient='vertical', command=self.tv.yview)
        self.scoll.grid(row=2, column=4, sticky='nsw')
        self.reverse = False
        self.tv.configure(yscrollcommand=self.scoll.set)
        

        self.back = tk.Button(self, text="Back", command=lambda: self.controller.show_frame(self.controller.DroneTechnicianHome))
        self.back.grid(row=4, column=0)
        
        self.reset = tk.Button(self, text="Reset", command=self.reset)
        self.reset.grid(row=4, column=1)
        
        self.filter = tk.Button(self, text="Filter", command=self.filter_rows)
        self.filter.grid(row=4, column=2)
        
    def reset(self):
        self.e_droneid.delete(0, tk.END)
        self.e_status.set("All")
        self.tv.delete(*self.tv.get_children())

    def filter_rows(self):
        self.tv.delete(*self.tv.get_children())
        status = self.e_status.get()
        droneid = self.e_droneid.get()
        if not droneid:
            droneid = None
        print(droneid)
        cmd = 'SELECT ID, DroneStatus, Radius FROM DRONE WHERE DroneTech = %s AND (%s = ID OR %s IS NULL) AND (%s = DroneStatus OR %s = "All")'
        args = (self.controller.username, droneid, droneid, status, status)
        rc = self.controller.cursor.execute(cmd, args)
        result = self.controller.cursor.fetchall()
        print(result)
        for idx, i in enumerate(result):
            self.tv.insert('', tk.END, values=i)
        #self.tv.bind("<Button-1>", self.event_sort_column)

    def sort_column(self, tv, col):
        l = [(tv.set(i, col), i) for i in tv.get_children()]
        l.sort(reverse=self.reverse)
        self.reverse = not self.reverse
        for index, (val, i) in enumerate(l):
            tv.move(i, '', index)
            