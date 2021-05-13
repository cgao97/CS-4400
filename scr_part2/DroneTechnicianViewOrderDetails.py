import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql
from tkinter import ttk
import tools

class DroneTechnicianViewOrderDetails(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.label = tk.Label(self, text="DroneTechnician View Order Details")
        self.label.grid(row=0, column=0, padx=170)
        
        self.customer = tk.Label(self, text="Customer Name: ")
        self.customer.grid(row=1, column=0)
        self.e_customer = tk.StringVar()
        e_customer = tk.Entry(self, textvariable=self.e_customer, state=tk.DISABLED)
        e_customer.grid(row=1, column=1)

        self.orderid = tk.Label(self, text="Order ID: ")
        self.orderid.grid(row=2, column=0)
        self.e_orderid = tk.StringVar()
        e_orderid = tk.Entry(self, textvariable=self.e_orderid, state=tk.DISABLED)
        e_orderid.grid(row=2, column=1)
        
        self.total_amount = tk.Label(self, text="Total Amount: ")
        self.total_amount.grid(row=3, column=0)
        self.e_total_amount = tk.StringVar()
        e_total_amount = tk.Entry(self, textvariable=self.e_total_amount, state=tk.DISABLED)
        e_total_amount.grid(row=3, column=1)

        self.num_items = tk.Label(self, text="Total Items: ")
        self.num_items.grid(row=4, column=0)
        self.e_num_items = tk.StringVar()
        e_num_items = tk.Entry(self, textvariable=self.e_num_items, state=tk.DISABLED)
        e_num_items.grid(row=4, column=1)
        
        self.date = tk.Label(self, text="Date Of Purchase: ")
        self.date.grid(row=5, column=0)
        self.e_date = tk.StringVar()
        e_date = tk.Entry(self, textvariable=self.e_date, state=tk.DISABLED)
        e_date.grid(row=5, column=1)
        
        self.droneid = tk.Label(self, text="Drone ID: ")
        self.droneid.grid(row=6, column=0)
        self.e_droneid = tk.StringVar()
        e_droneid = tk.Entry(self, textvariable=self.e_droneid, state=tk.DISABLED)
        e_droneid.grid(row=6, column=1)
        
        self.store_asso = tk.Label(self, text="Store Associate: ")
        self.store_asso.grid(row=7, column=0)
        self.e_store_asso = tk.StringVar()
        e_store_asso = tk.Entry(self, textvariable=self.e_store_asso, state=tk.DISABLED)
        e_store_asso.grid(row=7, column=1)
        
        self.status = tk.Label(self, text="Status: ")
        self.status.grid(row=8, column=0)
        self.e_status = tk.StringVar()
        e_status = tk.Entry(self, textvariable=self.e_status, state=tk.DISABLED)
        e_status.grid(row=8, column=1)
        
        self.address = tk.Label(self, text="Address: ")
        self.address.grid(row=1, column=2)
        self.e_address = tk.StringVar()
        e_address = tk.Entry(self,textvariable=self.e_address, width=40, state=tk.DISABLED)
        e_address.grid(row=1, column=3)
        
        self.items = tk.Label(self, text="Items: ")
        self.items.grid(row=2, column=2)
        
        self.tv = ttk.Treeview(self, column=(0,1), show='headings')
        #self.tv['show'] = 'headings'
        self.tv.grid(row=3, column=2)
        self.tv.heading("0", text="Item")
        self.tv.column("0", width=120, stretch=tk.NO)
        self.tv.heading("1", text="Count")
        self.tv.column("1", width=40, stretch=tk.NO)
        
        self.scoll = ttk.Scrollbar(self, orient='vertical', command=self.tv.yview)
        self.scoll.grid(row=3, column=3, sticky='nsw')
        self.tv.configure(yscrollcommand=self.scoll.set)
        
        self.back = tk.Button(self, text="Back", command=lambda: self.controller.show_frame(self.controller.DroneTechnicianViewStoreOrders))
        self.back.grid(row=9, column=0)
        
    def set(self):
        cmd = 'SELECT concat(cust.FirstName, " ", cust.LastName) AS "Customer Name", %s AS "Order ID", sum(CONTAINS.Quantity * Price) AS "Total Amount", sum(CONTAINS.Quantity) AS "Total Items", OrderDate AS "Date Of Purchase", DroneID AS "Drone ID", concat(emp.FirstName, " ", emp.LastName) AS "Store Associate", OrderStatus AS "Status", concat(cust.Street, ", ", cust.City, ", ", cust.State, " ", cust.Zipcode) AS Address FROM ORDERS LEFT JOIN DRONE ON DroneID = Drone.ID JOIN USERS AS cust ON CustomerUsername = Username AND ORDERS.ID = %s JOIN CONTAINS ON CONTAINS.OrderID = %s JOIN CHAIN_ITEM ON (ChainItemName, CHAIN_ITEM.ChainName, CHAIN_ITEM.PLUNumber) = (ItemName, CONTAINS.ChainName, CONTAINS.PLUNumber) JOIN USERS AS emp ON DroneTech = emp.Username'
        orderid = self.controller.technician_select_order
        args = (orderid, orderid, orderid)
        rc = self.controller.cursor.execute(cmd, args)
        result = self.controller.cursor.fetchall()[0]

        self.e_customer.set(result[0])
        self.e_orderid.set(result[1])
        self.e_total_amount.set(str(result[2]))
        self.e_num_items.set(str(result[3]))
        self.e_date.set(tools.dateToStr(str(result[4]), self.controller.cursor))
        self.e_droneid.set(result[5])
        self.e_store_asso.set(result[6])
        self.e_status.set(result[7])
        self.e_address.set(result[8])

        cmd = 'SELECT ItemName, CONTAINS.Quantity FROM ORDERS LEFT JOIN DRONE ON DroneID = Drone.ID JOIN CONTAINS ON CONTAINS.OrderID = %s JOIN CHAIN_ITEM ON ORDERS.ID = %s AND (ChainItemName, CHAIN_ITEM.ChainName, CHAIN_ITEM.PLUNumber) = (ItemName, CONTAINS.ChainName, CONTAINS.PLUNumber)'
        args = (orderid, orderid)
        rc = self.controller.cursor.execute(cmd, args)
        result = self.controller.cursor.fetchall()
        self.tv.delete(*self.tv.get_children())
        for idx, i in enumerate(result):
            self.tv.insert('', tk.END, values=i)
        