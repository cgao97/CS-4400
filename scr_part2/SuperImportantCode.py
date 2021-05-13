import tkinter as tk
import tkinter.messagebox as Msgbox
import mysql.connector as sql
from tkinter import ttk



type_map = {
    str: tk.StringVar,
    int:tk.IntVar,
    float:tk.DoubleVar
}

numbers = set(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'])

class Screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.elements = {}
        self.variables = {}
        self.commands = {}
        self.row = 0
        self.reverse = False
        self.is_number = {}
        self.has_alternatives = {}
        self.alternatives = {}
        self.increment_row = True
        def validate_num(S):
            if S in numbers:
                return True
            self.bell()  # .bell() plays that ding sound telling you there was invalid input
            return False
        self.validate_num = (self.register(validate_num), '%S')

    @staticmethod
    def get_element_name(text):
        return text.strip().replace(' ', '').lower()

    def add_label(self, text, column = 0):
        ui_element_name = Screen.get_element_name(text)
        elements = self.elements
        elements[ui_element_name +
                '_label'] = tk.Label(self, text=text)
        elements[ui_element_name + '_label'].grid(row=self.row, column=column)
        self.row += 1 if self.increment_row else 0

    def add_entry(self, text, column = 0, disabled=False, number=False, show_label=True):
        ui_element_name = Screen.get_element_name(text)
        elements = self.elements
        elements[ui_element_name +
                        '_label'] = tk.Label(self, text=text)
        elements[ui_element_name + '_label'].grid(row=self.row, column=column)
        elements[ui_element_name + '_input'] = tk.Entry(
            self, state=tk.DISABLED if disabled else tk.NORMAL, validate='key', vcmd=self.validate_num if number else None)
        elements[ui_element_name + '_input'].grid(row=self.row, column=column + 1)
        self.is_number[ui_element_name] = number
        self.row += 1 if self.increment_row else 0

    def get_entry(self, text):
        ui_element_name = Screen.get_element_name(text)
        if ui_element_name in self.is_number and self.is_number[ui_element_name]:
            try:
                return int(self.elements[ui_element_name + '_input'].get())
            except ValueError:
                Msgbox.showerror("Error", "Please input a valid number!")
                raise ValueError()
        else:
            return self.elements[ui_element_name + '_input'].get()


    def update_entry(self, text, new_value):
        ui_element_name = Screen.get_element_name(text) + '_input'
        original_state = self.elements[ui_element_name]["state"]
        self.elements[ui_element_name].configure(state=tk.NORMAL)
        self.elements[ui_element_name].delete(0, "end")
        self.elements[ui_element_name].insert(0, str(new_value))
        self.elements[ui_element_name].configure(state=original_state)

    def add_range_selector(self, text, column=0, disabled=False):
        ui_element_name = Screen.get_element_name(text)
        elements = self.elements
        elements[ui_element_name +
                 '_label'] = tk.Label(self, text=text)
        elements[ui_element_name + '_label'].grid(row=self.row, column=column)

        elements[ui_element_name + '_input1'] = tk.Entry(
            self, state=tk.DISABLED if disabled else tk.NORMAL, validate='key', vcmd=self.validate_num)
        elements[ui_element_name +
                 '_input1'].grid(row=self.row, column=column + 1)

        elements[ui_element_name +
                 '_label2'] = tk.Label(self, text='-')
        elements[ui_element_name + '_label2'].grid(row=self.row, column=column + 2)

        elements[ui_element_name + '_input2'] = tk.Entry(
            self, state=tk.DISABLED if disabled else tk.NORMAL, validate='key', vcmd=self.validate_num)
        elements[ui_element_name +
                 '_input2'].grid(row=self.row, column=column + 3)
        self.row += 1 if self.increment_row else 0

    def get_range(self, text):
        ui_element_name = Screen.get_element_name(text) + '_input'
        try:
            l = self.elements[ui_element_name + '1'].get()
            r = self.elements[ui_element_name + '2'].get()
            l = -2147483648 if l.strip() == '' else l
            r = 2147483647 if r.strip() == '' else r
            return int(l), int(r)
        except ValueError:
            Msgbox.showerror("Error", "Please input a valid number!")
            raise ValueError()

    def update_range(self, text, min, max):
        ui_element_name = Screen.get_element_name(text) + '_input'
        self.elements[ui_element_name + '1'].delete(0, "end")
        self.elements[ui_element_name + '1'].insert(0, min)
        self.elements[ui_element_name+ '2'].delete(0, "end")
        self.elements[ui_element_name + '2'].insert(0, max)

    def add_options(self, text, values, column = 0, disabled=False, default_index=0, command=None):
        elements = self.elements
        controller = self.controller
        ui_element_name = Screen.get_element_name(text)
        self.variables[ui_element_name] =  type_map[type(values[0])]()  
        self.variables[ui_element_name].set(values[default_index] if len(values) > 0 else None)
        elements[ui_element_name +
                '_label'] = tk.Label(self, text=text)
        elements[ui_element_name + '_label'].grid(row=self.row, column=column)

        self.commands[ui_element_name] = command
        elements[ui_element_name + '_input'] = tk.OptionMenu(
            self, self.variables[ui_element_name], *values, command=command)
        elements[ui_element_name + '_input'].configure(state=tk.DISABLED if disabled else tk.NORMAL)
        elements[ui_element_name + '_input'].grid(row=self.row, column=column + 1)
        self.row += 1 if self.increment_row else 0

    def update_options(self, text, values, default_index = 0):
        ui_element_name = Screen.get_element_name(text)
        menu = self.elements[ui_element_name + '_input']["menu"]
        menu.delete(0, "end")
        def new_command(value):
            self.variables[ui_element_name].set(value)
            if self.commands[ui_element_name] is not None:
                self.commands[ui_element_name](value)
        for i in values:
            menu.add_command(
                label=i, command=lambda value=i: new_command(value))
        self.variables[ui_element_name].set(
            values[default_index] if len(values) > 0 else None)


    def get_option(self, text):
        ui_element_name = Screen.get_element_name(text)
        return self.variables[ui_element_name].get()

    def get(self, *texts):
        result = []
        for text in texts:
            ui_element_name = Screen.get_element_name(text) 
            if isinstance(self.elements[ui_element_name + '_input'], tk.OptionMenu):
                result.append(self.variables[ui_element_name].get())
            else:
                result.append(self.elements[ui_element_name + '_input'].get())
        return result

    
    def add_table(self, text, headings, column = 0, enable_editor=False):
        ui_element_name = Screen.get_element_name(text)
        self.elements[ui_element_name] = ttk.Treeview(self, column=list(
            range(len(headings))), show='headings', selectmode="browse")
        self.elements[ui_element_name].grid(row=self.row, column=column, columnspan=len(headings))
        for index, i in enumerate(headings):
            self.elements[ui_element_name].heading(str(
                index), text=i, command=lambda: self.sort_column(self.elements[ui_element_name], str(index)))
            self.elements[ui_element_name].column(
                str(index), width=200, stretch=tk.NO)
        self.elements[ui_element_name + '_scroll'] = ttk.Scrollbar(
            self, orient='vertical', command=self.elements[ui_element_name].yview)
        self.elements[ui_element_name +
                      '_scroll'].grid(row=self.row, column=len(headings)+ column, sticky='nsw')
        self.reverse = False
        self.elements[ui_element_name].configure(
            yscrollcommand=self.elements[ui_element_name + '_scroll'].set)
        if enable_editor:
            self.elements[ui_element_name + '_row_editor_label'] = tk.Label(self, text='Currently Selected Row:')
            self.elements[ui_element_name + '_row_editor_label'].grid(row=self.row + 1, column=column)
            
            self.elements[ui_element_name + '_row_editor_selection'] = tk.Label(self, text='Null')
            self.elements[ui_element_name + '_row_editor_selection'].grid(row=self.row + 2, column=column)

            saved_row = self.row
            self.elements[ui_element_name].bind(
                '<<TreeviewSelect>>', lambda x: self.__show_table_row_editor(text, saved_row, column))
            self.row += 3 if self.increment_row else 0
        else:
            self.row += 1 if self.increment_row else 0

    def __show_table_row_editor(self, text, row, column):
        ui_element_name = Screen.get_element_name(text)
        self.elements[ui_element_name + '_row_editor_selection'].grid_remove()
        values = self.get_selected_item_in_table(ui_element_name)
        identifier = self.get_selected_item_identifier_in_table(ui_element_name)
        for col, value in enumerate(values):
            print(col, value)
            sub_element_name = ui_element_name + '_row_editor_selection_' + str(col)
            if sub_element_name in self.elements:
                self.elements[sub_element_name].grid_forget()
            if self.has_alternatives[identifier] and col in self.alternatives[identifier]:
                self.variables[sub_element_name] =  type_map[type(value)]()  
                self.variables[sub_element_name].set(value)
                self.elements[sub_element_name] = tk.OptionMenu(
                    self, self.variables[sub_element_name], *self.alternatives[identifier][col],
                    command=lambda value: self.update_table_row(text))
            else:
                self.elements[sub_element_name] = tk.Entry(self)
                self.elements[sub_element_name].delete(0, "end")
                self.elements[sub_element_name].insert(0, value)
                self.elements[sub_element_name].config(state='disabled')
            self.elements[sub_element_name].grid(row=row + 2, column=column + col)


    def update_table(self, text, data, default_locations=None):
        ui_element_name = Screen.get_element_name(text)
        self.elements[ui_element_name].delete(*self.elements[ui_element_name].get_children())
        if default_locations is None:
            len_columns = len(data[0]) if len(data) > 0 else 0
            default_locations = [[0] * len_columns] * len(data)
        for index, i in enumerate(data):
            identifier = ui_element_name + '_' + str(index)
            default = []
            has_alternatives = False
            for col, value in enumerate(i):
                if type(value) in [tuple, list, set]:
                    has_alternatives = True
                    default.append(value[default_locations[index][col]] if len(value) > 0 else None)
                    self.alternatives.setdefault(identifier,{})
                    self.alternatives[identifier][col] = list(value)
                else:
                    default.append(value)
            self.elements[ui_element_name].insert('', tk.END, values=default, text=identifier)
            self.has_alternatives[identifier] = has_alternatives

    def get_entry_or_option_in_table_editor(self, text):
        ui_element_name = Screen.get_element_name(text)
        if isinstance(self.elements[ui_element_name], tk.OptionMenu):
            return self.variables[ui_element_name].get()
        else:
            return self.elements[ui_element_name].get()

    def update_table_row(self, text):
        ui_element_name = Screen.get_element_name(text)
        identifier = self.get_selected_item_identifier_in_table(ui_element_name)
        values = self.get_selected_item_in_table(ui_element_name)
        new_value = [self.get_entry_or_option_in_table_editor(
            ui_element_name + '_row_editor_selection_' + str(i)) for i in range(len(values))]
        print(new_value)
        self.elements[ui_element_name].item(self.elements[ui_element_name].focus(), text=identifier, value=new_value)


    def get_selected_item_in_table(self, text, type_model=None):
        ui_element_name = Screen.get_element_name(text)
        cur_item = self.elements[ui_element_name].focus()
        values = self.elements[ui_element_name].item(cur_item)['values']
        if type_model is not None:
            for index, i in enumerate(values):
                values[index] = type_model[index](values[index]) 
        return values

    def get_all_items_in_table(self, text,  type_model=None):
        ui_element_name = Screen.get_element_name(text)
        children = self.elements[ui_element_name].get_children()
        result = []
        for cur_item in children:
            values = self.elements[ui_element_name].item(cur_item)['values']
            if type_model is not None:
                for index, i in enumerate(values):
                    values[index] = type_model[index](values[index])
            result.append(values)
        return result

    def get_selected_item_identifier_in_table(self, text):
        ui_element_name = Screen.get_element_name(text)
        cur_item = self.elements[ui_element_name].focus()
        identifier = self.elements[ui_element_name].item(cur_item)['text']
        return identifier

    def sort_column(self, tv, col):
        l = [(tv.set(i, col), i) for i in tv.get_children()]
        l.sort(reverse=self.reverse)
        self.reverse = not self.reverse
        for index, (val, i) in enumerate(l):
            tv.move(i, '', index)

    def add_button(self, text, c, column = 0):
        ui_element_name = Screen.get_element_name(text) + '_button'
        self.elements[ui_element_name] = tk.Button(self, text=text, command=c)
        self.elements[ui_element_name].grid(row = self.row, column = column)
        self.row += 1 if self.increment_row else 0

    def add_navigation_button(self, c, c_text = 'Back'):
        elements = self.elements
        controller = self.controller
        if isinstance(c, str):
            c_command = lambda: controller.show_frame(c)
        else:
            c_command = c

        elements['back'] = tk.Button(self, text=c_text, command=c_command)
        elements['back'].grid(row=self.row, column=0)

        self.row += 1 if self.increment_row else 0

    def set_row(self, row):
        self.row = row

    def fetchone(self, query, params=None):
        self.controller.cursor.execute(query, params)
        return self.controller.cursor.fetchone()

    def fetchall(self, query, params=None):
        self.controller.cursor.execute(query, params)
        return self.controller.cursor.fetchall()

    def execute(self, query, params=None):
        self.controller.cursor.execute(query, params)

    def onload(self):
        pass

    @staticmethod
    def join(a, b, c1, c2, *argv):
        print(c1)
        c = [c1, c2]
        print(c)
        for i in argv:
            c.append(i)
        print(c)
        c = [(c[2 * i], c[2 * i + 1]) for i in range(len(c) // 2)]
        print(c)
        c = ','.join([a + '.' + i[0] + '=' + b + '.' + i[1] for i in c])
        return '{0} join {1} on {2};'.format(a,b,c)
