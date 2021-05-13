import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql
from SuperImportantCode import Screen

class ChainManagerCreateChainItem(Screen):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.add_label('Chain Manager Create Chain Item')
        self.add_options('Item', [i[0] for i in self.fetchall('select itemname from item')])
        self.add_entry('Quantity Available', number=True)
        self.add_entry('Limit Per Order', number = True)
        self.add_entry('PLU Number',disabled=True)
        self.update_entry('plu number', self.get_largest_plu() + 1)
        self.add_entry('Price per Unit')
        self.add_navigation_button('chainmanagerhome')
        self.add_button('Create', lambda: self.create_chain_item())

    def onload(self):
        self.update_entry('plu number', self.get_largest_plu() + 1)

    def get_largest_plu(self):
        user  = self.controller.username
        x = self.fetchone(
            'select max(plunumber) from chain_item join manager on manager.username = %s and chain_item.chainname = manager.chainname', (user,))[0]
        if x is None:
            x = 9999
        return x

    def create_chain_item(self):

        #insert into chain_item (ChainItemName , ChainName, PLUNumber , Orderlimit,Quantity , Price)
        # values(i_item_name, i_chain_name, i_PLU_number,
        #        i_order_limit, i_quantity, i_price);
        user = self.controller.username
        try:
            chain = self.fetchone(
                'select manager.chainname from chain_item join manager on manager.username = %s and chain_item.chainname = manager.chainname', (user,))[0]
            item, plu, limit, quantity, price = self.get('item', 'plu number','limit per order', 'quantity available', 'price per unit')
                
            self.execute(
                'insert into chain_item (ChainItemName , ChainName, PLUNumber , Orderlimit,Quantity , Price) values (%s, %s, %s, %s, %s, %s)', 
                (item, chain, plu, limit, quantity, price))
            Msgbox.showinfo("Info", "Success!")
        except Exception as e:
            Msgbox.showerror("Error", str(e))
            
    #     self.label = tk.Label(self, text="Chain Manager Create Chain Item")
    #     self.label.grid(row=0, column=1)

    #     self.chain_name_label = tk.Label(self, text="Chain Name")
    #     self.chain_name_label.grid(row=1, column=0)
    #     self.chain_name_input = tk.Entry(self, state=tk.DISABLED)
    #     self.chain_name_input.grid(row=1, column=1)

    #     self.item = tk.StringVar()
    #     self.items = self.get_items()
    #     self.item_label = tk.Label(self, text="Item")
    #     self.item_label.grid(row=2, column=0)
    #     self.item_input = tk.OptionMenu(self, self.item, *self.items)
    #     self.item_input.grid(row=2, column=1)

    #     self.quantity_available_label = tk.Label(self, text="Quantity Label")
    #     self.quantity_available_label.grid(row=3, column=0)
    #     self.quantity_available_input = tk.Entry(self)
    #     self.quantity_available_input.grid(row=3, column=1)

    #     self.limit_per_order_label = tk.Label(self, text="Limit Per Order")
    #     self.limit_per_order_label.grid(row=4, column=0)
    #     self.limit_per_order_input = tk.Entry(self)
    #     self.limit_per_order_input.grid(row=4, column=1)

    #     self.ui_elements = {}

    #     self.add_entry('PLU Number', 5)

    #     self.add_entry('Price Per Unit', 6)

    #     self.back = tk.Button(self, text="Back", command=lambda: self.controller.show_frame('ChainManagerHome'))
    #     self.back.grid(row=7, column=0)

    #     self.create = tk.Button(self, text="Create", command=self.create_drone)
    #     self.create.grid(row=8, column=2)

    # def get_items(self):
    #     return [
    #         'fdfds','fsdfdsfs0','gfdgfdgfdgfd'
    #     ]

    # def get_asss(self, item):
    #     return ["fdsfsdfds", "fdsfsd"]

    # def create_drone(self):
    #     pass

    # def add_entry(self, text, row, disabled=False):
    #     ui_elements_name = text.strip().replace(' ', '_').lower()
    #     self.ui_elements[ui_elements_name + '_label'] = tk.Label(self, text=text)
    #     self.ui_elements[ui_elements_name + '_label'].grid(row=row, column=0)
    #     self.ui_elements[ui_elements_name + '_input'] = tk.Entry(self, state=tk.DISABLED if disabled else tk.NORMAL)
    #     self.ui_elements[ui_elements_name + '_input'].grid(row=row, column=1)
