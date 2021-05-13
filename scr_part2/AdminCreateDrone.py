import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql
from SuperImportantCode import Screen


class AdminCreateDrone(Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.add_label('Admin Create Drone')
        self.add_entry('Drone Id', disabled=True)
        self.update_entry('Drone ID', self.fetchone('select max(id) from drone')[0] + 1)
        self.add_options('Associated Zip Code', [i[0] for i in self.fetchall('select distinct zipcode from store')], 
                         command=lambda x: self.update_options('Store Associate', self.get_associates(self.get_option('associated zip code'))))
        self.add_entry('Travel Radius', number=True)
        self.add_entry('Status', disabled=True)
        self.update_entry('Status', 'Available')
        self.add_options('Store Associate', self.get_associates(self.get_option('associated zip code')))
        self.add_navigation_button('adminhome')
        self.add_button('Create', lambda: self.create_drone())

    def get_associates(self, zip):
        x = self.fetchall(
            "select drone_tech.username from drone_tech, users, store where drone_tech.username = users.username and store.storename=drone_tech.storename and store.chainname=drone_tech.chainname and store.zipcode={0};".format(zip))
        x = [i[0] for i in x]
        return x
    
    def create_drone(self):
        try:
            self.execute('INSERT INTO DRONE VALUES(%s, %s, %s, %s, %s)', self.get(
                'drone id', 'status', 'associated zip code', 'travel radius', 'store associate'))
            self.update_entry('drone id', self.fetchone('select max(id) from drone')[0] + 1)
            Msgbox.showinfo("Info", "Success!")
        except Exception as e:
            Msgbox.showerror("Error", str(e))
