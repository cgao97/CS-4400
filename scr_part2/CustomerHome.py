import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql

class CustomerHome(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.label = tk.Label(self, text="Customer Home")
        self.label.grid(row=0, column=0)

        self.change_card = tk.Button(self, text="Change Credit Card Info", command=lambda: self.controller.show_frame(
            'CustomerChangeCreditCardInformation'))
        self.change_card.grid(row=1, column=0)
        
        self.review_order = tk.Button(self, text="Review Order", command=lambda: self.controller.show_frame(
            'CustomerReviewOrder'))
        self.review_order.grid(row=1, column=1)
        
        self.order_history = tk.Button(
            self, text="View Order History", command=lambda: self.controller.show_frame('CustomerViewOrderHistory'))
        self.order_history.grid(row=2, column=0)
        
        self.view_items = tk.Button(
            self, text="View Store Items", command=lambda: self.controller.show_frame('CustomerViewStoreItems'))
        self.view_items.grid(row=2, column=1)
