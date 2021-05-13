import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql


# class CustomerViewOrderHistory(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         self.label = tk.Label(self, text="CustomerViewOrderHistory")
#         self.label.grid(row=0, column=1)

#         self.Username_label = tk.Label(self, text="Username")
#         self.Username_label.grid(row=1, column=0)
#         self.Username_input = tk.Entry(self, state=tk.DISABLED)
#         self.Username_input.grid(row=1, column=1)

#         self.OrderID = tk.StringVar()
#         self.OrderID = self.get_items()
#         self.OrderID_label = tk.Label(self, text=OrderID)
#         self.OrderID_label.grid(row=2, column=0)
#         self.OrderID_input = tk.OptionMenu(self, self.OrderID, *self.OrderID)
#         self.OrderID_input.grid(row=2, column=1)

#         self.TotalAmount_label = tk.Label(self, text="TotalAmount Label")
#         self.TotalAmount_label.grid(row=3, column=0)
#         self.TotalAmount_input = tk.Entry(self)
#         self.TotalAmount_input.grid(row=3, column=1)

#         self.TotalItems_label = tk.Label(self, text="TotalItems Label")
#         self.TotalItems_label.grid(row=3, column=0)
#         self.TotalItems_input = tk.Entry(self)
#         self.TotalItems_input.grid(row=3, column=1)

#         self.DroneID_label = tk.Label(self, text="DroneID")
#         self.DroneID_label.grid(row=3, column=0)
#         self.DroneID_input = tk.Entry(self)
#         self.DroneID_input.grid(row=3, column=1)

#         self.StoreAssociate_label = tk.Label(self, text="StoreAssociate")
#         self.StoreAssociate_label.grid(row=3, column=0)
#         self.StoreAssociate_input = tk.Entry(self)
#         self.StoreAssociate_input.grid(row=3, column=1)

#         self.Status_label = tk.Label(self, text="StoreAssociate")
#         self.Status_label.grid(row=3, column=0)
#         self.Status_input = tk.Entry(self)
#         self.Status_input.grid(row=3, column=1)

#         self.date_label = tk.Label(self, text='Date')
#         self.date_label.grid(row=1, column=0)
#         self.date_input = tk.Entry(self)
#         self.date_input.grid(row=3, column=1)



#         self.back = tk.Button(self, text="Back", command=lambda: self.controller.show_frame('CustomerViewOrderHistory'))
#         self.back.grid(row=7, column=0)


#     def get_OrderID(self):
#         return [
#             'fdfds','fsdfdsfs0','gfdgfdgfdgfd'
#         ]


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



class CustomerViewOrderHistory(Screen):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.add_entry('Username')
        self.add_options('OrderID', ('42'))
        self.add_entry('TotalAmount')
        self.add_entry('TotalItems')
        self.add_entry('DateOfPurshase')
        self.add_entry('DroneID')
        self.add_entry('StoreAssociation')
        self.add_entry('Status')

        self.back = tk.Button(self, text="Back", command=lambda: self.controller.show_frame('CustomerHome'))
        self.back.grid(row=7, column=0)

