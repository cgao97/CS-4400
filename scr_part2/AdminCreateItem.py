import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql
from SuperImportantCode import Screen


class AdminCreateItem(Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.add_label('Admin Create Item')
        self.add_entry('Name')
        self.add_options('Type', [
            'Dairy', 'Bakery', 'Meat', 'Produce', 'Personal Care', 'Paper Goods', 'Beverages'
        ])
        self.add_options('Organic', ('Yes', 'No'))
        self.add_entry('Origin')
        self.add_navigation_button('adminhome')
        self.add_button('Create',lambda:self.create_item())

    def create_item(self):
        try:
            #INSERT INTO ITEM VALUES (i_item_name, i_item_type, i_origin, i_organic);
            self.execute('insert into item values (%s, %s, %s, %s)', self.get('name', 'type', 'origin', 'organic'))
            Msgbox.showinfo("Info", "Success!")
        except Exception as e:
            Msgbox.showerror("Error", str(e))
