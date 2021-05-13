import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql
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
from DroneTechnicianTrackAssignedDrones import *
from CustomerViewStoreItems import *
from CustomerReviewOrder import *

connector = sql.connect(
  host="localhost",
  user="root",
  passwd="gcx19970916",
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
        self.username = None
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
        self.DroneTechnicianTrackAssignedDrones = DroneTechnicianTrackAssignedDrones
        self.CustomerViewStoreItems = CustomerViewStoreItems
        self.CustomerReviewOrder = CustomerReviewOrder
        self.frames = {}
        
        #args
        self.technician_seleced_order_id = None
        self.customer_selected_items_args = None
        
        for F in (Register, Login, DroneTechnicianHome, CustomerHome, ChainManagerHome, AdminHome,
                  AdminCreateGroceryChain, AdminCreateStore, AdminViewCustomers, DroneTechnicianViewStoreOrders,
                  DroneTechnicianViewOrderDetails, DroneTechnicianTrackAssignedDrones, CustomerViewStoreItems,
                  CustomerReviewOrder):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.show_frame(Login)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        
if __name__ == "__main__":
    
    app = Main()
    app.mainloop()
    