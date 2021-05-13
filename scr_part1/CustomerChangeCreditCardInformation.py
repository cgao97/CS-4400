
# import tkinter as tk
# import tkinter.messagebox as Msgbox
# import mysql.connector as sql


# class CustomerChangeCreditCardInformation(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         self.label = tk.Label(self, text="CustomerViewOrderHistory")
#         self.label.grid(row=0, column=1)

#         self.Username_label = tk.Label(self, text="User Name ")
#         self.Username_label.grid(row=1, column=0)
#         self.Username_input = tk.Entry(self, state=tk.DISABLED)
#         self.Username_input.grid(row=1, column=1)

#         self.OrderID = tk.StringVar()
#         self.OrderID = self.get_items()
#         self.OrderID_label = tk.Label(self, text=OrderID)
#         self.OrderID_label.grid(row=2, column=0)
#         self.OrderID_input = tk.OptionMenu(self, self.OrderID, *self.OrderID)
#         self.OrderID_input.grid(row=2, column=1)

#         self.FirstName_label = tk.Label(self, text="FirstName Label")
#         self.FirstName_label.grid(row=3, column=0)
#         self.FirstName_input = tk.Entry(self)
#         self.FirstName_input.grid(row=3, column=1)

#         self.LastName_label = tk.Label(self, text="LastName Label")
#         self.LastName_label.grid(row=3, column=0)
#         self.LastName_input = tk.Entry(self)
#         self.LastName_input.grid(row=3, column=1)


#         self.CreditCardNumber_label = tk.Label(self, text="CreditCardNumber")
#         self.CreditCardNumber_label.grid(row=3, column=0)
#         self.CreditCardNumber_input = tk.Entry(self)
#         self.CreditCardNumber_input.grid(row=3, column=1)

#         self.SecurityCode_label = tk.Label(self, text='SecurityCode')
#         self.SecurityCode_label.grid(row=1, column=0)
#         self.SecurityCode_input = tk.Entry(self)
#         self.SecurityCode_input.grid(row=3, column=1)


#         self.back = tk.Button(self, text="Back", command=lambda: self.controller.show_frame('CustomerChangeCreditCardInformation'))
#         self.back.grid(row=7, column=0)

#         self.Approve = tk.Button(self, text="Approve", command=lambda: self.change_credit_card_information())
#         self.Approve.grid(row=7, column=1)



#     def add_entry(self, text, row, disabled=False):
#         ui_elements_name = text.strip().replace(' ', '_').lower()
#         self.ui_elements[ui_elements_name + '_label'] = tk.Label(self, text=text)
#         self.ui_elements[ui_elements_name + '_label'].grid(row=row, column=0)
#         self.ui_elements[ui_elements_name + '_input'] = tk.Entry(self, state=tk.DISABLED if disabled else tk.NORMAL)
#         self.ui_elements[ui_elements_name + '_input'].grid(row=row, column=1)



import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql
from SuperImportantCode import Screen


class CustomerChangeCreditCardInformation (Screen):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.add_entry('Username', number=True)
        self.add_entry('FirstName', number=True)
        self.add_entry('LastName', number=True)
        self.add_entry('Credit Card Number', number=True)
        self.add_entry('Security Code', number=True)
        self.add_entry('Expiration Date ', number=True)
        self.add_navigation_button('CustomerHome')

        self.add_button('Reset', None)

        self.back = tk.Button(self, text="Back", command=lambda: self.controller.show_frame('CustomerChangeCreditCardInformation'))
        self.back.grid(row=7, column=0)

        self.Approve = tk.Button(self, text="Approve", command=lambda: self.change_credit_card_information())
        self.Approve.grid(row=7, column=0)

    
    def change_credit_card_information(self):

        #insert into chain_item (ChainItemName , ChainName, PLUNumber , Orderlimit,Quantity , Price)
        # values(i_item_name, i_chain_name, i_PLU_number,
        #        i_order_limit, i_quantity, i_price);
        user = self.controller.username
        try:
            customer = self.fetchone(
                'select customer.username from users join customer on users.username = %s and users.username = customer.username', (user,))[0]
            username, firstname, lastname, creditcardnumber, securitycode, expirationdate = self.get('Username', 'FirstName','LastName', 'CcNumber', 'CVV', 'EXP_DATE')
                
            self.execute(
                'insert into customer (Username, FirstName, LastName, CcNumber, CVV, EXP_DATE ) values (%s, %s, %s, %s, %s, %s)', 
                (username, firstname, lastname, creditcardnumber, securitycode, expirationdate))
            Msgbox.showinfo("Info", "Success!")
        except Exception as e:
            Msgbox.showerror("Error", str(e))




