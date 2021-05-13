import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql
from SuperImportantCode import Screen


class ChainManagerViewDrones(Screen):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.add_label('Chain Manager View Drones')
        self.add_entry('Drone ID', number=True)
        self.add_entry('Radius', number=True)
        self.add_button('Filter', lambda: self.onload())
        self.add_table('Drones', ('Drone ID', 'Operator', 'Radius', 'Zip Code', 'Status'))
        self.add_navigation_button('ChainManagerHome')
        self.add_button('Reset', None)

    def onload(self):
        user = self.controller.username
        query = 'SELECT ID, DroneTech AS Operator, Radius, Zip, DroneStatus FROM \
        DRONE JOIN DRONE_TECH \
        ON DRONE_TECH.Username = DRONE.DroneTech JOIN MANAGER ON MANAGER.ChainName = DRONE_TECH.ChainName\
        WHERE MANAGER.Username = %s \
        AND(%s IS NULL OR %s = "" or DRONE.ID=%s) \
        AND(%s IS NULL OR %s = "" or DRONE.Radius >= %s)'

        x = self.fetchall(query, [user] + self.get('drone id', 'drone id', 'drone id', 'radius', 'radius', 'radius'))
        print(x)
        self.update_table('Drones', x)
