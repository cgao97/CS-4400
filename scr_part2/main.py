import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql
from SuperImportantCode import Screen
from Login import *
from Register import *
from DroneTechnicianHome import *
from CustomerHome import *
from ChainManagerHome import *
from AdminHome import *
from AdminCreateGroceryChain import *
from AdminCreateStore import *
from AdminViewCustomers import *
from DroneTechnicianViewStoreOrders import *
from DroneTechnicianViewOrderDetails import *
from AdminCreateDrone import *
from AdminCreateItem import *
from ChainManagerCreateChainItem import *
from ChainManagerViewDroneTechnicians import *


from glob import glob
from pathlib import Path
from importlib import import_module
import os


def auto_import():
    cdir = os.getcwd()
    dirname = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dirname)
    files = set(glob('*.py'))
    files.remove("main.py")
    files.remove("SuperImportantCode.py")
    result = set()
    for i in files:
        try:
            class_name = os.path.splitext(i)[0]
            c = getattr(import_module(class_name), class_name)
            if issubclass(c, tk.Frame):
                result.add(c)
                print('Successfully imported ' + class_name)
        except Exception as e:
            print(str(e))
            pass
    os.chdir(cdir)
    return result



connector = sql.connect(
  host="localhost",
  user="root",
  passwd="111111",
  database="grocery_drone_delivery"
)

connector.autocommit = True
cursor = connector.cursor(buffered=True)

class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.connector = connector
        self.cursor = cursor
        container = tk.Frame(self)
        container.pack(fill="both", expand = True)
        self.username = 'aallman302'
        self.Login = Login
        self.Register = Register
        self.DroneTechnicianHome = DroneTechnicianHome
        self.CustomerHome = CustomerHome
        self.ChainManagerHome = ChainManagerHome
        self.AdminHome = AdminHome
        self.AdminCreateGroceryChain = AdminCreateGroceryChain
        self.AdminCreateStore = AdminCreateStore
        self.AdminViewCustomers = AdminViewCustomers
        self.DroneTechnicianViewStoreOrders = DroneTechnicianViewStoreOrders
        self.DroneTechnicianViewOrderDetails = DroneTechnicianViewOrderDetails
        self.AdminCreateDrone = AdminCreateDrone
        self.AdminCreateItem = AdminCreateItem
        self.frames = {}
        
        #args
        self.technician_seleced_order_id = None
        
        for F in set((Register, Login, DroneTechnicianHome, CustomerHome, ChainManagerHome, AdminHome,
                  AdminCreateGroceryChain, AdminCreateStore, AdminViewCustomers, DroneTechnicianViewStoreOrders,
                  DroneTechnicianViewOrderDetails, AdminCreateDrone, AdminCreateItem, ChainManagerCreateChainItem,
                  )).union(auto_import()):

            frame = F(container, self)

            self.frames[F] = frame
            self.frames[F.__name__.lower()] = frame
            frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.show_frame('customerhome')
        
    def show_frame(self, cont):
        if isinstance(cont, str):
            cont = cont.strip().replace(' ', '').lower()
        frame = self.frames[cont]
        frame.tkraise()
        if isinstance(frame, Screen):
            frame.onload()
        
if __name__ == "__main__":
    
    app = Main()
    app.mainloop()
    
