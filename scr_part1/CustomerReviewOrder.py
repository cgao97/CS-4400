import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql
from tkinter import ttk
import tools

class CustomerReviewOrder(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        self.label = tk.Label(self, text='Customer Review Order')
        self.label.grid(row=0, column=0)
        
        self.chain = tk.Label(self, text="Chain")
        self.chain.grid(row=1, column=0)
        
        self.e_chain = tk.StringVar()
        e_chain = tk.Entry(self, textvariable=self.e_chain, state=tk.DISABLED)
        e_chain.grid(row=1, column=1)
        
        self.store = tk.Label(self, text="Store")
        self.store.grid(row=1, column=2)
        
        self.e_store = tk.StringVar()
        e_store = tk.Entry(self, textvariable=self.e_chain, state=tk.DISABLED)
        e_store.grid(row=1, column=3)
        
        self.e_select_num = tk.StringVar()
        self.select_num_menu = ttk.Combobox(self, textvariable=self.e_select_num, state="readonly")
        self.select_num_menu.grid(row=2, column=0)
        self.e_select_num.trace("w", self.set_num)
        
        self.tv = ttk.Treeview(self, column=(0,1), show='headings')
        #self.tv['show'] = 'headings'
        self.tv.grid(row=3, column=0, columnspan=3)
        self.tv.heading("0", text="Items")
        self.tv.column("0", width=160, stretch=tk.NO)
        self.tv.heading("1", text="Quantity")
        self.tv.column("1", width=80, stretch=tk.NO)

        self.tv.bind("<Button-1>", self.row_selection)

        self.scoll = ttk.Scrollbar(self, orient='vertical', command=self.tv.yview)
        self.scoll.grid(row=3, column=4, sticky='nsw')
        self.reverse = False
        self.tv.configure(yscrollcommand=self.scoll.set)

        self.back = tk.Button(self, text="Cancel Order", command=self.back)
        self.back.grid(row=4, column=0)

        self.place_order = tk.Button(self, text="Place Order", command=self.place_order)
        self.place_order.grid(row=4, column=2)
    
    def set(self):
        #self.chain_menu.bind("<<ComboBoxSelected>>", self.set_store)
        chain, store, tv = self.controller.customer_selected_items_args
        self.e_chain.set(chain)
        self.e_store.set(store)
        for child in tv.get_children():
            row = tv.item(child)["values"]
            if row[1] == 0:
                continue
            self.tv.insert('', tk.END, values=row)

    def row_selection(self, event):
        item = self.tv.selection()
        row = self.tv.set(item)
        print(row)
        try:
            if row:
                chain, store, _ = self.controller.customer_selected_items_args
                cmd = 'SELECT CHAIN_ITEM.OrderLimit, CHAIN_ITEM.Quantity FROM CHAIN_ITEM JOIN ITEM ON (CHAIN_ITEM.ChainItemName = ITEM.ItemName) JOIN CHAIN ON (CHAIN_ITEM.ChainName = CHAIN.ChainName) JOIN STORE ON (CHAIN.ChainName = STORE.ChainName) JOIN USERS ON (USERS.Zipcode = STORE.Zipcode) WHERE (CHAIN.ChainName = %s) AND (StoreName = %s) AND (USERS.Username = %s) AND (CHAIN_ITEM.ChainItemName = %s)'
                args = (chain, store, self.controller.username, row['0'])
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
        for child in self.tv.get_children():
            row = self.tv.item(child)["values"]
            if not row:
                return
            if not row[1] or row[1] == 0:
                pass
            proc = 'customer_update_order'
            args = (self.controller.username, row[0], row[1])
            self.controller.cursor.callproc(proc, args)
        
        cmd = 'UPDATE ORDERS SET OrderStatus = "Pending" Where CustomerUsername = %s AND OrderStatus = "Creating"'
        args = (self.controller.username,)
        rc = self.controller.cursor.execute(cmd, args)
        self.controller.show_frame(self.controller.CustomerHome)
    
    def back(self):
        self.tv.delete(*self.tv.get_children())
        cmd = 'DELETE CONTAINS FROM ORDERS JOIN CONTAINS ON (ORDERS.ID = CONTAINS.OrderID) WHERE ORDERS.CustomerUsername = %s AND OrderStatus = "Creating"'
        args = (self.controller.username,)
        #print(cmd%args)
        rc = self.controller.cursor.execute(cmd, args)
        self.controller.show_frame(self.controller.CustomerViewStoreItems)
        