import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql
from tkinter import ttk
import tools

DRONE_STATUS = ['Pending', 'Drone Assigned', 'In Transit', 'Delivered']
class DroneTechnicianViewStoreOrders(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)
        
        self.label = tk.Label(self, text='View Store Orders')
        self.label.grid(row=0, column=0)
        
        self.date_label = tk.Label(self, text='Date')
        self.date_label.grid(row=1, column=0)
        
        self.e_start_date = tk.Entry(self)
        self.e_start_date.grid(row=1, column=1)

        self.hyphen = tk.Label(self, text=" - ")
        self.hyphen.grid(row=1, column=2)

        self.e_end_date = tk.Entry(self)
        self.e_end_date.grid(row=1, column=3)
        
        self.e_operator = tk.StringVar()
        self.operator_menu = ttk.Combobox(self, textvariable=self.e_operator, state="readonly", width=15)
        self.operator_menu.grid(row=2, column=0)
        self.operator_menu.set('NULL')
        self.e_operator.set(self.operator_menu.get())

        self.e_drone_id = tk.StringVar()
        self.drone_menu = ttk.Combobox(self, textvariable=self.e_drone_id, values=['NULL'], state="readonly", width=10)
        self.drone_menu.grid(row=2, column=1)
        self.drone_menu.set('NULL')
        self.e_drone_id.set(self.drone_menu.get())

        self.e_status = tk.StringVar()
        self.status_menu = ttk.Combobox(self, textvariable=self.e_status, values=DRONE_STATUS, state="readonly", width=15)
        self.status_menu.grid(row=2, column=2)
        self.status_menu.set(DRONE_STATUS[0])
        self.e_status.set(self.status_menu.get())
        
        self.tv = ttk.Treeview(self, column=(0,1,2,3,4,5), show='headings')
        #self.tv['show'] = 'headings'
        self.tv.grid(row=3, column=0, columnspan=5)
        self.tv.heading("0", text="ID", command=lambda:self.sort_column(self.tv, '0'))
        self.tv.column("0", width=80, stretch=tk.NO)
        self.tv.heading("1", text="Operator")
        self.tv.column("1", width=160, stretch=tk.NO)
        self.tv.heading("2", text="Date", command=lambda:self.sort_column(self.tv, '2'))
        self.tv.column("2", width=80, stretch=tk.NO)
        self.tv.heading("3", text="Drone ID", command=lambda:self.sort_column(self.tv, '3'))
        self.tv.column("3", width=80, stretch=tk.NO)
        self.tv.heading("4", text="Status", command=lambda:self.sort_column(self.tv, '4'))
        self.tv.column("4", width=80, stretch=tk.NO)
        self.tv.heading("5", text="Total", command=lambda:self.sort_column(self.tv, '5'))
        self.tv.column("5", width=80, stretch=tk.NO)
        
        self.tv.bind("<Button-1>", self.row_selection)
        
        self.scoll = ttk.Scrollbar(self, orient='vertical', command=self.tv.yview)
        self.scoll.grid(row=3, column=6, sticky='nsw')
        self.reverse = False
        self.tv.configure(yscrollcommand=self.scoll.set)

        self.back = tk.Button(self, text="Back", command=lambda: self.controller.show_frame(self.controller.DroneTechnicianHome))
        self.back.grid(row=4, column=0)
        
        self.reset = tk.Button(self, text="Reset", command=self.reset)
        self.reset.grid(row=4, column=1)
        
        self.filter = tk.Button(self, text="Filter", command=self.filter_rows)
        self.filter.grid(row=4, column=2)

        self.filter = tk.Button(self, text="View Order Details", command=lambda: self.view_order_details())
        self.filter.grid(row=4, column=3)
        
        self.filter = tk.Button(self, text="Save", command=lambda: self.save())
        self.filter.grid(row=4, column=4)
        
    def firstname_on_click(self, event):
        if self.e_firstname['fg'] == 'grey':
            self.e_firstname.delete(0, tk.END)
            self.e_firstname.config(fg = 'black')
    def lastname_on_click(self, event):
        if self.e_lastname['fg'] == 'grey':
            self.e_lastname.delete(0, tk.END)
            self.e_lastname.config(fg = 'black')
                                
    def reset(self):
        self.e_start_date.delete(0, tk.END)
        self.e_end_date.delete(0, tk.END)
        self.operator_menu.set('NULL')
        self.drone_menu.config(values=['NULL'])
        self.drone_menu.set('NULL')
        self.tv.delete(*self.tv.get_children())

    def filter_rows(self):
        self.tv.delete(*self.tv.get_children())
        start = self.e_start_date.get()
        end = self.e_end_date.get()
        if start:
            start = tools.strToDate(start, self.controller.cursor)
            if not start:
                return 1
        else:
            start = '0000-00-00'
        if end:
            end = tools.strToDate(end, self.controller.cursor)
            if not end:
                return 1
        else:
            end = '9999-12-31'
        
        cmd = 'SELECT CONTAINS.OrderID, CONCAT(FirstName, " ", LastName) AS Operator, OrderDate, DroneID, OrderStatus, sum(CONTAINS.Quantity * Price) AS Total FROM CHAIN_ITEM JOIN CONTAINS ON (ChainItemName, CHAIN_ITEM.ChainName, CHAIN_ITEM.PLUNumber) = (ItemName, CONTAINS.ChainName, CONTAINS.PLUNumber) JOIN (SELECT ORDERS.ID, OrderStatus, OrderDate, CustomerUsername, DroneID, DroneTech, Zipcode as CustomerZip FROM ORDERS JOIN USERS ON CustomerUsername = Username AND OrderDate BETWEEN %s and %s LEFT JOIN DRONE ON DroneID = Drone.ID) AS temp ON CONTAINS.OrderID = ID AND (CONTAINS.ChainName, temp.CustomerZip) = (SELECT DRONE_TECH.ChainName, Store.Zipcode as StoreZip FROM DRONE_TECH JOIN STORE ON (DRONE_TECH.StoreName, DRONE_TECH.ChainName) = (STORE.StoreName, STORE.ChainName) AND Drone_Tech.Username = %s) LEFT JOIN USERS ON Username = DroneTech group by OrderID'
        args = (start, end, self.controller.username)
        rc = self.controller.cursor.execute(cmd, args)
        result = self.controller.cursor.fetchall()
        print(result)
        for idx, i in enumerate(result):
            self.tv.insert('', tk.END, values=i)
        #self.tv.grid(row=3, column=0, columnspan=5)
        #self.tv.bind("<Button-1>", self.event_sort_column)

    def sort_column(self, tv, col):
        l = [(tv.set(i, col), i) for i in tv.get_children()]
        l.sort(reverse=self.reverse)
        self.reverse = not self.reverse
        for index, (val, i) in enumerate(l):
            tv.move(i, '', index)
    
    def row_selection(self, event):
        item = self.tv.selection()
        row = self.tv.set(item)
        self.operator_menu.config(values=['NULL', self.controller.username])
        print(row)
        try:
            if row['1'] == 'None':
                cmd = 'SELECT ID FROM DRONE WHERE DroneTech = %s AND DroneStatus <> "Busy"'
                args = (self.controller.username,)
                rc = self.controller.cursor.execute(cmd, args)
                result = self.controller.cursor.fetchall()
                drone = list(map(lambda x: x[0], result))
                print(drone)
                print(self.controller.username)
                self.drone_menu.config(values=['NULL'] + drone)
        except:
            pass
            
    def view_order_details(self):
        item = self.tv.selection()
        row = self.tv.set(item)
        if not row:
            Msgbox.showerror("Error", "Please make a selection first")
            return 1
        self.controller.technician_select_order = row['0']
        self.controller.DroneTechnicianViewOrderDetails.set(self.controller.frames[self.controller.DroneTechnicianViewOrderDetails])
        self.controller.show_frame(self.controller.DroneTechnicianViewOrderDetails)
        
    
    def save(self):
        item = self.tv.selection()
        row = self.tv.set(item)
        if not row:
            Msgbox.showerror("Error", "Please make a selection first")
            return 1
        if self.e_operator.get() != 'NULL' and self.e_drone_id.get() != 'NULL':
            cmd = 'UPDATE ORDERS SET OrderStatus = %s, DroneID = %s WHERE %s = ID'
            args = (self.e_status.get(), self.e_drone_id.get(), row['0'])
            rc = self.controller.cursor.execute(cmd, args)
            cmd = 'UPDATE DRONE SET DroneStatus = "Busy" WHERE %s = ID'
            args = (self.e_drone_id.get(),)
            rc = self.controller.cursor.execute(cmd, args)
            if self.e_status.get() == 'Delivered':
                cmd = 'UPDATE DRONE SET DroneStatus = "Available" WHERE %s = ID'
                args = (self.e_drone_id.get(),)
                print(cmd%args)
                rc = self.controller.cursor.execute(cmd, args)
            Msgbox.showinfo("Message", "Success")
            self.reset()
        else:
            Msgbox.showerror("Error", "Drone ID and drone technician should be assigned together")
            return 1