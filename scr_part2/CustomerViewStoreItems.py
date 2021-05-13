import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql
from tkinter import ttk
import tools

CATAGORY = ['All', 'Dairy', 'Bakery', 'Meat', 'Produce', 'Personal Care', 'Paper Goods', 'Beverages', 'Other']
class CustomerViewStoreItems(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        self.label = tk.Label(self, text='Customer View Store Items')
        self.label.grid(row=0, column=0)

        self.date_label = tk.Label(self, text='Username')
        self.date_label.grid(row=1, column=0)

        self.e_username = tk.StringVar()
        self.username = tk.Entry(self, textvariable=self.e_username, state="readonly")
        self.username.grid(row=1, column=1)
        
        self.chain_store = tk.Label(self, text="Chain")
        self.chain_store.grid(row=1, column=2)

        self.e_chain = tk.StringVar()
        self.chain_menu = ttk.Combobox(self, textvariable=self.e_chain, state="readonly")
        self.chain_menu.grid(row=1, column=3)
        self.e_chain.trace("w", self.set_store)
        
        self.catagory = tk.Label(self, text="Catagory: ")
        self.catagory.grid(row=2, column=0)

        self.e_catagory = tk.StringVar()
        self.catagory_menu = ttk.Combobox(self, textvariable=self.e_catagory, values=CATAGORY, state="readonly")
        self.catagory_menu.grid(row=2, column=1)
        self.catagory_menu.set(CATAGORY[0])
        self.e_catagory.set(self.catagory_menu.get())
        self.e_catagory.trace("w", self.set_table)

        self.e_store = tk.Label(self, text="Store")
        self.e_store.grid(row=2, column=2)
        
        self.e_store = tk.StringVar()
        self.store_menu = ttk.Combobox(self, textvariable=self.e_store, state="readonly")
        self.store_menu.grid(row=2, column=3)
        self.e_store.trace("w", self.set_table)

        self.e_select_num = tk.StringVar()
        self.select_num_menu = ttk.Combobox(self, textvariable=self.e_select_num, state="readonly")
        self.select_num_menu.grid(row=3, column=0)
        self.e_select_num.trace("w", self.set_num)
        
        
        self.tv = ttk.Treeview(self, column=(0,1), show='headings')
        #self.tv['show'] = 'headings'
        self.tv.grid(row=4, column=0, columnspan=3)
        self.tv.heading("0", text="Items")
        self.tv.column("0", width=160, stretch=tk.NO)
        self.tv.heading("1", text="Quantity")
        self.tv.column("1", width=80, stretch=tk.NO)

        self.tv.bind("<Button-1>", self.row_selection)

        self.scoll = ttk.Scrollbar(self, orient='vertical', command=self.tv.yview)
        self.scoll.grid(row=3, column=4, sticky='nsw')
        self.reverse = False
        self.tv.configure(yscrollcommand=self.scoll.set)

        self.back = tk.Button(self, text="Cancel Order", command=self.cancel_order)
        self.back.grid(row=5, column=0)

        self.place_order = tk.Button(self, text="Place Order", command=self.place_order)
        self.place_order.grid(row=5, column=2)
    
    def set(self):
        #self.chain_menu.bind("<<ComboBoxSelected>>", self.set_store)
        self.e_store.set("")
        self.e_chain.set("")
        self.tv.delete(*self.tv.get_children())
        self.e_username.set(self.controller.username)
        cmd = 'SELECT ChainName FROM Store WHERE Zipcode = (SELECT Zipcode FROM USERS WHERE Username = %s)'
        args = (self.controller.username,)
        rc = self.controller.cursor.execute(cmd, args)
        result = self.controller.cursor.fetchall()
        print(result)
        if not result:
            Msgbox.showinfo("Warning", "There are no stores available to order from.")
            self.chain_menu.config(values='NULL')
            self.store_menu.config(values='NULL')
        chains = list(map(lambda x: x[0], result))
        self.chain_menu.config(values=chains)

        
    def set_store(self, name,index,mode):
        self.e_store.set('')
        self.store_menu.config(values=['NULL'])
        cmd = 'SELECT StoreName FROM Store WHERE Zipcode = (SELECT Zipcode FROM USERS WHERE Username = %s) AND ChainName = %s'
        args = (self.controller.username, self.e_chain.get())
        rc = self.controller.cursor.execute(cmd, args)
        result = self.controller.cursor.fetchall()
        print(result)
        stores = list(map(lambda x: x[0], result))
        self.store_menu.config(values=stores)
        
    def set_table(self, name, index, mode):
        self.tv.delete(*self.tv.get_children())
        print(2)
        cmd = 'SELECT CHAIN_ITEM.ChainItemName, 0 FROM CHAIN_ITEM JOIN ITEM ON (CHAIN_ITEM.ChainItemName = ITEM.ItemName) JOIN CHAIN ON (CHAIN_ITEM.ChainName = CHAIN.ChainName) JOIN STORE ON (CHAIN.ChainName = STORE.ChainName) JOIN USERS ON (USERS.Zipcode = STORE.Zipcode) WHERE (CHAIN.ChainName = %s) AND (StoreName = %s) AND (ItemType = %s OR %s = "ALL") AND (USERS.Username = %s)'
        args = (self.e_chain.get(), self.e_store.get(), self.e_catagory.get(), self.e_catagory.get(), self.controller.username)
        rc = self.controller.cursor.execute(cmd, args)
        result = self.controller.cursor.fetchall()
        for idx, i in enumerate(result):
            self.tv.insert('', tk.END, values=i)


    def row_selection(self, event):
        item = self.tv.selection()
        row = self.tv.set(item)
        print(row)
        try:
            if row:
                cmd = 'SELECT CHAIN_ITEM.OrderLimit, CHAIN_ITEM.Quantity FROM CHAIN_ITEM JOIN ITEM ON (CHAIN_ITEM.ChainItemName = ITEM.ItemName) JOIN CHAIN ON (CHAIN_ITEM.ChainName = CHAIN.ChainName) JOIN STORE ON (CHAIN.ChainName = STORE.ChainName) JOIN USERS ON (USERS.Zipcode = STORE.Zipcode) WHERE (CHAIN.ChainName = %s) AND (StoreName = %s) AND (ItemType = %s OR %s = "ALL") AND (USERS.Username = %s) AND (CHAIN_ITEM.ChainItemName = %s)'
                args = (self.e_chain.get(), self.e_store.get(), self.e_catagory.get(), self.e_catagory.get(), self.controller.username, row['0'])
                print(cmd%args)
                rc = self.controller.cursor.execute(cmd, args)
                result = self.controller.cursor.fetchall()
                item_limit = int(result[0][0])
                chain_limit = int(result[0][1])
                if item_limit > chain_limit:
                    item_limit = chain_limit
                print(item_limit)
                self.select_num_menu.config(values=list(range(item_limit+1)))
        except:
            pass


    def set_num(self, name, index, mode):
        selected = self.tv.selection()
        row = self.tv.set(selected)
        if not row:
            Msgbox.showerror("Error", "Please make a selection first")
            return 1
        print((row['0'], self.e_select_num.get()))
        self.tv.item(selected, text='', values=(row['0'], self.e_select_num.get()))
    
    def place_order(self):
        cmd = 'SELECT * FROM ORDERS WHERE CustomerUsername = %s AND OrderStatus = "Creating"'
        args = (self.controller.username,)
        rc = self.controller.cursor.execute(cmd, args)
        result = self.controller.cursor.fetchall()
        if not result:
            cmd = 'INSERT INTO ORDERS (OrderStatus, OrderDate, CustomerUsername, DroneID) VALUES ("Creating", CURDATE(), %s, NULL)'
            args = (self.controller.username,)
            rc = self.controller.cursor.execute(cmd, args)
            
        if not self.tv.get_children():
            Msgbox.showerror("Error", "Please add items")
            return 1
        for child in self.tv.get_children():
            row = self.tv.item(child)["values"]
            if not row[1] or row[1] == 0:
                continue
            proc = 'customer_select_items'
            args = (self.controller.username, self.e_chain.get(), self.e_store.get(), row[0], row[1])
            self.controller.cursor.callproc(proc, args)
        self.controller.customer_selected_items_args = (self.e_chain.get(), self.e_store.get(),self.tv)
        self.controller.CustomerReviewOrder.set(self.controller.frames[self.controller.CustomerReviewOrder])
        self.controller.show_frame(self.controller.CustomerReviewOrder)
    def cancel_order(self):
        cmd = 'DELETE FROM ORDERS WHERE CustomerUsername = %s AND OrderStatus = "Creating"'
        args = (self.controller.username,)
        #print(cmd%args)
        rc = self.controller.cursor.execute(cmd, args)
        self.controller.show_frame(self.controller.CustomerHome)
            