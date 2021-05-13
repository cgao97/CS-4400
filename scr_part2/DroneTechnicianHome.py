import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql

class DroneTechnicianHome(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Drone Technician Home")
        self.label.grid(row=0, column=0)
        
        self.view_order = tk.Button(self, text="View Store Orders", command=lambda: self.controller.show_frame(self.controller.DroneTechnicianViewStoreOrders))
        self.view_order.grid(row=1, column=0)
        
        self.track = tk.Button(self, text="Track Drone Delivery", command=lambda: self.controller.show_frame(self.controller.DroneTechnicianTrackAssignedDrones))
        self.track.grid(row=1, column=1)
