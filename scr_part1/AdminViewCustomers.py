import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql
from tkinter import ttk

class AdminViewCustomers(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.label = tk.Label(self, text="Admin View Customers")
        self.label.grid(row=0, column=0, padx=170)
        
        self.customer = tk.Label(self, text="Customer: ")
        self.customer.grid(row=1, column=0)
        
        self.e_firstname = tk.Entry(self, fg='grey')
        self.e_firstname.insert(0, 'First')
        self.e_firstname.bind('<FocusIn>', self.firstname_on_click)
        #self.e_firstname.config(fg = 'grey')
        self.e_firstname.grid(row=1, column=1)

        self.e_lastname = tk.Entry(self, fg='grey')
        self.e_lastname.insert(0, 'Last')
        self.e_lastname.bind('<FocusIn>', self.lastname_on_click)
        self.e_lastname.config(fg = 'grey')
        self.e_lastname.grid(row=1, column=2)

        self.back = tk.Button(self, text="Back", command=lambda: self.controller.show_frame(self.controller.AdminHome))
        self.back.grid(row=4, column=0)
        
        self.reset = tk.Button(self, text="Reset", command=self.reset)
        self.reset.grid(row=4, column=1)
        
        self.filter = tk.Button(self, text="Filter", command=self.filter_rows)
        self.filter.grid(row=4, column=2)
        
        self.tv = ttk.Treeview(self, column=(0,1,2), show='headings')
        #self.tv['show'] = 'headings'
        self.tv.grid(row=3, column=0, columnspan=3)
        self.tv.heading("0", text="Username", command=lambda:self.sort_column(self.tv, '0'))
        self.tv.column("0", width=80, stretch=tk.NO)
        self.tv.heading("1", text="Name", command=lambda:self.sort_column(self.tv, '1'))
        self.tv.column("1", width=160, stretch=tk.NO)
        self.tv.heading("2", text="Address")
        self.tv.column("2", width=260, stretch=tk.NO)
        
        self.scoll = ttk.Scrollbar(self, orient='vertical', command=self.tv.yview)
        self.scoll.grid(row=3, column=2, sticky='nsw')
        self.reverse = False
        self.tv.configure(yscrollcommand=self.scoll.set)
        
    def firstname_on_click(self, event):
        if self.e_firstname['fg'] == 'grey':
            self.e_firstname.delete(0, tk.END)
            self.e_firstname.config(fg = 'black')
    def lastname_on_click(self, event):
        if self.e_lastname['fg'] == 'grey':
            self.e_lastname.delete(0, tk.END)
            self.e_lastname.config(fg = 'black')
                                
    def reset(self):
        self.e_firstname.delete(0, tk.END)
        self.e_firstname.insert(0, 'First')
        self.e_firstname.config(fg = 'grey')
        self.e_lastname.delete(0, tk.END)
        self.e_lastname.insert(0, 'Last')
        self.e_lastname.config(fg = 'grey')
        self.tv.delete(*self.tv.get_children())

    def filter_rows(self):
        self.tv.delete(*self.tv.get_children())
        firstname = self.e_firstname.get()
        lastname = self.e_lastname.get()
        if self.e_firstname['fg'] == 'grey' or not firstname:
            firstname = None
        if self.e_lastname['fg'] == 'grey'or not lastname:
            lastname = None
        cmd = 'SELECT CUSTOMER.Username, CONCAT(Firstname, " ", LastName) AS FullName, CONCAT(Street, ", ", City, ", ", State, " ", Zipcode) AS Address FROM CUSTOMER JOIN USERS ON CUSTOMER.Username = USERS.Username WHERE (%s IS NULL OR %s = FirstName) AND (%s IS NULL OR %s = LastName);'
        args = (firstname, firstname, lastname, lastname)
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
            