import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql
from SuperImportantCode import Screen


class test(Screen):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.add_table('Drones', ('Drone ID', 'Operator',
                                  'Radius', 'Zip Code', 'Status'), enable_editor=True)
        self.update_table('Drones', [('fdsfds', [1, 5], 'gfdgdf','eqweq','qqewq'),
                                     ('dsadsax2', 'xzcxzczx','gfdgdf', 'eqweq', 'qqewq'),
                                     ('dsadsax2', 'xzcxzczx', 'gfdgdf', 'eqweq', 'qqewq'),
                                     ('dsadsax2', 'xzcxzczx', 'gfdgdf', 'eqweq', 'qqewq'), 
                                     ('dsa','gfdgfvd','xzcxzcxz','ewewqewqewq','hythyth')

         ])
        self.add_button('update', lambda: self.update_table_row('drones'))

        self.add_button('print value', lambda: print(self.get_selected_item_in_table('drones')))

        self.add_button('fetch one', lambda: print(self.fetchall('select distinct Zipcode from store')))

        self.add_options('czxc', ['fdsfds', 'vfdvfd'])
        self.update_options('czxc', ['vcfd', 'freth','cxnckjz'])
