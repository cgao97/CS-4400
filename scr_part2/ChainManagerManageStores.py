import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql
from SuperImportantCode import Screen


class ChainManagerManageStores(Screen):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.add_label('Chain Manager Manage Stores')
        self.add_entry('Chain', disabled=True)
        self.add_options('Name', ('NULL',))
        self.add_range_selector('Total Range')
        self.add_table('Stores', ('Name', 'Address', '# Orders', 'Employees', 'Total'))
        self.add_navigation_button('ChainManagerHome')
        self.add_button('Reset', lambda: self.reset())
        self.add_button('Filter', lambda: self.onload())

    def reset(self):
        self.onload(default=True)
    def onload(self, default=False):
        user = self.controller.username
        chain = self.fetchone(
            'select manager.chainname from chain_item join manager on manager.username = %s and chain_item.chainname = manager.chainname', (user,))[0]
        self.update_entry('chain', chain)

        self.execute('call manager_manage_stores(%s, null, null, null);', (user,))
        t = self.fetchall('select * from manager_manage_stores_result')
        self.update_options('Name', ['Null'] + [i[0] for i in t])
        if default:
            self.update_table('stores', t)
        else:
            name = self.get_option('name').strip()
            if name == 'Null':
                name = None
            self.execute(
                'call manager_manage_stores(%s, %s, %s, %s);', [user, name ]+  list(self.get_range('total range')))
            t = self.fetchall('select * from manager_manage_stores_result')
            self.update_table('stores', t)
