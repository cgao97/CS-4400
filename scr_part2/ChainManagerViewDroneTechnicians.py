import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql
from SuperImportantCode import Screen

class ChainManagerViewDroneTechnicians(Screen):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.add_label('Chain Manager View Drone Technicians')
        self.add_entry('Chain', disabled=True)
        self.add_entry('Username')
        self.add_options('Location', ['Null'])        
        self.add_button('Filter', lambda: self.onload())
        self.add_table('Drone Technicians', ('Username', 'Name', 'Location'), enable_editor=True)

        self.add_navigation_button('ch ai N m an Age r homE')
        self.add_button('Reset', lambda: self.reset())
        self.add_button('Save', lambda:self.save())
    
    def reset(self):
        self.onload()

    def save(self):
        x = self.get_all_items_in_table('drone technicians')
        print(x)
        for i in x:
            self.execute('update drone_tech set storename = %s where username= %s', (i[2], i[0]))
        Msgbox.showinfo("Info", "Success!")

    def onload(self):
        user = self.controller.username
        dt_username = self.get_entry('Username').strip()
        location_cond = self.get_option('Location')
        conditions = 'and drone_tech.username = "{0}"'.format(dt_username) if dt_username != '' else ''
        conditions += 'and drone_tech.storename = "{0}"'.format(
            location_cond) if location_cond != 'Null' else ''
        chain = self.fetchone(
            'select manager.chainname from chain_item join manager on manager.username = %s and chain_item.chainname = manager.chainname', (user,))[0]
        locations = [i[0] for i in self.fetchall(
            'select storename from store where chainname = %s', (chain,)
        )]
        temp = self.fetchall("select concat(firstname, ' ', lastname), drone_tech.username, drone_tech.storename from users, drone_tech \
            where users.username=drone_tech.username and drone_tech.chainName = %s " + conditions, (chain,))
                      
        self.update_entry('chain', chain)
        self.update_options('Location', ['Null'] + locations)
        table_data = [(i[1], i[0], locations) for i in temp]
        table_data_default_index = [(None, None, locations.index(i[2])) for i in temp]
        self.update_table('Drone Technicians', table_data, table_data_default_index)
