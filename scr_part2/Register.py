import tkinter as tk
import tkinter.messagebox as Msgbox
import tkinter.ttk as ttk
import tools

STATES = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

class Register(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Register", font=10)
        self.label.grid(row=0, column=0)
        
        self.firstname = tk.Label(self, text='First Name')
        self.firstname.grid(row=1, column=0)
        
        self.e_firstname = tk.Entry(self)
        self.e_firstname.grid(row=1, column=1)

        self.lastname = tk.Label(self, text='Last Name')
        self.lastname.grid(row=2, column=0)
        
        self.e_lastname = tk.Entry(self)
        self.e_lastname.grid(row=2, column=1)
        
        self.username = tk.Label(self, text='Username')
        self.username.grid(row=3, column=0)
        
        self.e_username = tk.Entry(self)
        self.e_username.grid(row=3, column=1)

        self.passward = tk.Label(self, text='Password')
        self.passward.grid(row=4, column=0)
        
        self.e_password = tk.Entry(self, show='*')
        self.e_password.grid(row=4, column=1)
        
        self.confirm = tk.Label(self, text='Confirm')
        self.confirm.grid(row=5, column=0)
        
        self.e_confirm = tk.Entry(self, show='*')
        self.e_confirm.grid(row=5, column=1)
        
        self.street = tk.Label(self, text='Street')
        self.street.grid(row=1, column=3)
        
        self.e_street = tk.Entry(self)
        self.e_street.grid(row=1, column=4)
        
        city = tk.Label(self, text='City')
        city.grid(row=2, column=3)
        
        self.e_city = tk.Entry(self)
        self.e_city.grid(row=2, column=4)

        self.state = tk.Label(self, text='State')
        self.state.grid(row=3, column=3)
        self.e_state = tk.StringVar()
        menu = ttk.Combobox(self, textvariable=self.e_state, values=STATES, state="readonly", width=5)
        menu.grid(row=3, column=4)
        self.e_state.set(menu.get())
        
        self.zipcode = tk.Label(self, text='Zip')
        self.zipcode.grid(row=4, column=3)
        self.e_zipcode = tk.Entry(self)
        self.e_zipcode.grid(row=4, column=4)
        
        self.customer = tk.Button(self, text="Customer", command=self.show_reg_cust)
        self.customer.grid(row=6, column=0)
        
        self.employee = tk.Button(self, text="Employee", command=self.show_reg_employee)
        self.employee.grid(row=6, column=1)
        
        #customer
        self.card_num = tk.Label(self, text='Card Number')
        self.card_num.grid(row=7, column=0)
        
        self.e_card_num = tk.Entry(self)
        self.e_card_num.grid(row=7, column=1)
        
        self.cvv = tk.Label(self, text='CVV')
        self.cvv.grid(row=8, column=0)
        
        self.e_cvv = tk.Entry(self)
        self.e_cvv.grid(row=8, column=1)
        
        self.exp_date = tk.Label(self, text='Exp')
        self.exp_date.grid(row=8, column=2)
        
        self.e_exp_date = tk.Entry(self)
        self.e_exp_date.grid(row=8, column=3)
        
        #employee
        self.chain = tk.Label(self, text='Associated Grocery Chain')
        self.chain.grid(row=7, column=0)
        
        self.e_chain = tk.Entry(self)
        self.e_chain.grid(row=7, column=1)
        
        self.store = tk.Label(self, text='Associated Store Name')
        self.store.grid(row=8, column=0)
        
        self.e_store = tk.Entry(self)
        self.e_store.grid(row=8, column=1)
        
        self.chain.grid_forget()
        self.e_chain.grid_forget()
        self.store.grid_forget()
        self.e_store.grid_forget()
        
        register = tk.Button(self, text="Register", command=self.register_user)
        register.grid(row=9, column=1)
        
        to_login = tk.Button(self, text="Back to Login", command=lambda: self.controller.show_frame(controller.Login))
        to_login.grid(row=9, column=2)
        
    def show_reg_cust(self):
        self.chain.grid_forget()
        self.e_chain.grid_forget()
        self.e_chain.delete(0, tk.END)
        self.store.grid_forget()
        self.e_store.grid_forget()
        self.e_store.delete(0, tk.END)
        self.card_num.grid(row=7, column=0)
        self.e_card_num.grid(row=7, column=1)
        self.cvv.grid(row=8, column=0)
        self.e_cvv.grid(row=8, column=1)
        self.exp_date.grid(row=8, column=2)
        self.e_exp_date.grid(row=8, column=3)
    def show_reg_employee(self):
        self.card_num.grid_forget()
        self.e_card_num.grid_forget()
        self.e_card_num.delete(0, tk.END)
        self.cvv.grid_forget()
        self.e_cvv.grid_forget()
        self.e_cvv.delete(0, tk.END)
        self.exp_date.grid_forget()
        self.e_exp_date.grid_forget()
        self.e_exp_date.delete(0, tk.END)
        self.chain.grid(row=7, column=0)
        self.e_chain.grid(row=7, column=1)
        self.store.grid(row=8, column=0)
        self.e_store.grid(row=8, column=1)
    def register_user(self):
        if all([self.e_firstname.get(), self.e_lastname.get(), self.e_username.get(), self.e_password.get(),
               self.e_confirm.get(), self.e_street.get(), self.e_city.get(), self.e_state.get(),
               self.e_zipcode.get()]):
            if len(self.e_zipcode.get()) != 5:
                Msgbox.showerror("Error", "Zipcode Error")
                return 1
            if self.e_password.get() != self.e_confirm.get():
                Msgbox.showerror("Error", "Password does not match")
                return 1
            user_date = tools.strToDate(self.e_exp_date.get(), self.controller.cursor)
            if not user_date:
                return 1
            cmd = "SELECT * FROM USERS WHERE Username = %s"
            args = (self.e_username.get(),)
            self.controller.cursor.execute(cmd, args)
            #print(self.controller.cursor.fetchone())
            if self.controller.cursor.fetchone():
                Msgbox.showerror("Error", "Username already exists")
                return 1
            #Register Customer
            if all([self.e_card_num.get(), self.e_cvv.get(), self.e_exp_date.get()]):
                try:
                    args = (self.e_username.get(), self.e_password.get(), self.e_firstname.get(), 
                            self.e_lastname.get(), self.e_street.get(), self.e_city.get(),
                            self.e_state.get(), self.e_zipcode.get(), self.e_card_num.get(),
                            self.e_cvv.get(), user_date)
                    print(args)
                    rc = self.controller.cursor.callproc("register_customer", args)
                    Msgbox.showinfo("Message", "Success")
                    self.controller.show_frame(self.controller.Login)
                except:
                    Msgbox.showerror("Error", "Invalid Input")
            
            #Register Drone Tech    
            elif all([self.e_chain.get(), self.e_store.get()]):
                cmd = "SELECT * FROM STORE WHERE (StoreName, ChainName) = (%s, %s)"
                args = (self.e_store.get(), self.e_chain.get())
                self.controller.cursor.execute(cmd, args)
                if self.controller.cursor.fetchone():
                    try:
                        args = (self.e_username.get(), self.e_password.get(), self.e_firstname.get(), 
                                self.e_lastname.get(), self.e_street.get(), self.e_city.get(),
                                self.e_state.get(), self.e_zipcode.get())
                        rc = self.controller.cursor.callproc("register_employee", args)
                        cmd = "INSERT INTO DRONE_TECH VALUES (%s, %s, %s)"
                        args = (self.e_username.get(), self.e_store.get(), self.e_chain.get())
                        rc = self.controller.cursor.execute(cmd, args)
                        Msgbox.showinfo("Message", "Success")
                        self.controller.show_frame(self.controller.Login)
                    except:
                        Msgbox.showerror("Error", "Invalid Input")
                        
                else:
                    Msgbox.showerror("Error", "Invalid Store")
                    return 1

            # Register Chain Manager
            elif self.e_chain.get() != "" and self.e_store.get() == "":
                cmd = "SELECT * FROM MANAGER WHERE ChainName = %s"
                args = (self.e_chain.get(),)
                self.controller.cursor.execute(cmd, args)
                if self.controller.cursor.fetchone():
                    Msgbox.showerror("Error", "Chain Manager already exists")
                    return 1
                try:
                    args = (self.e_username.get(), self.e_password.get(), self.e_firstname.get(), 
                            self.e_lastname.get(), self.e_street.get(), self.e_city.get(),
                            self.e_state.get(), self.e_zipcode.get())
                    rc = self.controller.cursor.callproc("register_employee", args)
                    cmd = "INSERT INTO MANAGER VALUES (%s, %s)"
                    args = (self.e_username.get(), self.e_chain.get())
                    rc = self.controller.cursor.execute(cmd, args)
                    Msgbox.showinfo("Message", "Success")
                    self.controller.show_frame(self.controller.Login)
                except:
                    Msgbox.showerror("Error", "Invalid Input")
            else:
                Msgbox.showerror("Error", "All fields are required")
                return 1
        else:
            Msgbox.showerror("Error", "All fields are required")
            return 1
