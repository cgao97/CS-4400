import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql

STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

class AdminCreateStore(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Admin Create Store")
        self.label.grid(row=0, column=2)
        
        self.chain_name = tk.Label(self, text="Affliated Grocery Chain: ")
        self.chain_name.grid(row=1, column=1)
        
        cmd = "SELECT * FROM CHAIN"
        self.controller.cursor.execute(cmd)
        chains = self.controller.cursor.fetchall()
        chains = list(map(lambda x: x[0], chains))
        #print(chains)
        self.e_chain_name = tk.StringVar()
        chain_menu = tk.OptionMenu(self , self.e_chain_name, *chains)
        chain_menu.grid(row=1, column=2)
        
        self.store_name = tk.Label(self, text="Grocery Store Location Name: ")
        self.store_name.grid(row=2, column=1)
        self.e_store_name = tk.Entry(self)
        self.e_store_name.grid(row=2, column=2)
        
        self.street = tk.Label(self, text="Street: ", width=50)
        self.street.grid(row=3, column=1)
        self.e_street = tk.Entry(self)
        self.e_street.grid(row=3, column=2)

        self.city = tk.Label(self, text="City: ")
        self.city.grid(row=4, column=1)
        self.e_city = tk.Entry(self)
        self.e_city.grid(row=4, column=2)

        self.state = tk.Label(self, text='State:')
        self.state.grid(row=4, column=3)
        self.e_state = tk.StringVar()
        chain_menu = tk.OptionMenu(self , self.e_state, *STATES)
        chain_menu.grid(row=4, column=4)
        
        self.zipcode = tk.Label(self, text='Zip:')
        self.zipcode.grid(row=4, column=5)
        self.e_zipcode = tk.Entry(self)
        self.e_zipcode.grid(row=4, column=6)
        
        self.back = tk.Button(self, text="Back", command=lambda: self.controller.show_frame(self.controller.AdminHome))
        self.back.grid(row=5, column=0)
        
        self.create = tk.Button(self, text="Create", command=self.create_store)
        self.create.grid(row=5, column=6)
        
    def create_store(self):
        if not all([self.e_chain_name.get(), self.e_store_name.get(), self.e_street, self.e_city,
                   self.e_state, self.e_zipcode]):
            Msgbox.showerror("Error", "All fields are required")
            return 1
        cmd = "SELECT * FROM Store WHERE (ChainName, StoreName) = (%s, %s)"
        args = (self.e_chain_name.get(), self.e_store_name.get())
        #print(cmd %args)
        self.controller.cursor.execute(cmd, args)
        if self.controller.cursor.fetchone():
            Msgbox.showerror("Error", "Chain Store combination already exists")
            return 1
        
        cmd = "SELECT * FROM Store WHERE ChainName = %s AND Zipcode = %s"
        args = (self.e_chain_name.get(), self.e_zipcode.get())
        self.controller.cursor.execute(cmd, args)
        if self.controller.cursor.fetchone():
            Msgbox.showerror("Error", "A chain cannot have two stores in the same zip code.")
            return 1
        try:
            cmd = "admin_create_new_store"
            args = (self.e_store_name.get(), self.e_chain_name.get(), self.e_street.get(),
                    self.e_city.get(),
                    self.e_state.get(), self.e_zipcode.get())
            print(args)
            self.controller.cursor.callproc(cmd, args)
            Msgbox.showinfo("Message", "Success")
        except:
            Msgbox.showerror("Error", "Invalid Input")