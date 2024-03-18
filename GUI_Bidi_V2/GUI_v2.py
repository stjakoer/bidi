import threading
import tkinter as tk
from tkinter import ttk
from connect.connect_cinergia import cinergia_read_modbus, cinergia_write_modbus

class App(tk.Tk):
    def __init__(self):
        # main setup
        super().__init__()
        self.title('Bidi Masterprojekt')
        self.geometry('600x600')
        self.minsize(600,600)

        # frames
        self.menu = Control(self)
        self.main = Cinergia(self)
        self.main = Cms(self)
        self.main = Evtec(self)

        # run
        self.mainloop()


class Control(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='Control')
        self.grid(row=0, column=0, sticky='N')

        self.voltage = 400

        self.create_widgets()

    def create_widgets(self):
        # create the widgets
        voltage_label = ttk.Label(self, text=f'Voltage: {self.voltage} V')
        choose_current_label = ttk.Label(self, text='Choose Current')
        current_combo = ttk.Combobox(self, values=['4', '8', '20'])

        cng_control_frame = ttk.LabelFrame(self, text='CNG')
        button_enable_cng = ttk.Button(cng_control_frame, text='Enable')
        button_disable_cng = ttk.Button(cng_control_frame, text='Disable')
        button_reset_cng = ttk.Button(cng_control_frame, text='Reset')
        button_start_cng = ttk.Button(cng_control_frame, text='Start CNG')
        button_stop_cng = ttk.Button(cng_control_frame, text='Stop CNG')

        button_start_charging = ttk.Button(self, text='Laden Starten')
        button_stop_charging = ttk.Button(self, text='Laden Stoppen')

        # create the grid
        self.columnconfigure((0, 1), weight=1, uniform='a')
        cng_control_frame.columnconfigure((0, 1), weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3), weight=1)

        # place the widgets
        voltage_label.grid(row=0, column=0, sticky='nsew')
        choose_current_label.grid(row=1, column=0, sticky='nsew')
        current_combo.grid(row=1, column=1, sticky='nsew')

        cng_control_frame.grid(row=2, column=0, columnspan=2, sticky='nsew')
        button_enable_cng.grid(row=0, column=0, sticky='nsew')
        button_disable_cng.grid(row=0, column=1, sticky='nsew')
        button_reset_cng.grid(row=1, column=0, columnspan=2, sticky='nsew')
        button_start_cng.grid(row=2, column=0, sticky='nsew')
        button_stop_cng.grid(row=2, column=1, sticky='nsew')

        button_start_charging.grid(row=3, column=0, columnspan=2, sticky='nsew')
        button_stop_charging.grid(row=4, column=0, columnspan=2, sticky='nsew')


class Cinergia(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='Cinergia')
        self.grid(row=0, column=1)

        self.cng_dict = {}
        self.labels = {}

        self.update_dict()



    def create_labels(self):
        for labels in self.labels.values():
            for label in labels:
                label.destroy()

        # Erstellen Sie zwei Labels für jeden Eintrag in cng_dict
        self.labels = {}
        for i, key in enumerate(self.cng_dict):
            # Erstellen Sie ein Label für den Namen
            name_label = ttk.Label(self, text=self.cng_dict[key]['name']+':')
            name_label.grid(row=i, column=0, sticky='W')  # Platzieren Sie das Label in der i-ten Zeile und der 0-ten Spalte

            # Erstellen Sie ein Label für den Wert
            value_label = ttk.Label(self, text=self.cng_dict[key]['value'])
            value_label.grid(row=i, column=1)  # Platzieren Sie das Label in der i-ten Zeile und der 1-ten Spalte

            # Speichern Sie die Labels in self.labels
            self.labels[key] = (name_label, value_label)

    def update_dict(self):
        thread = threading.Thread(target=self.update_dict_thread, daemon=True)
        thread.start()

        self.after(1000, self.update_dict)

    def update_dict_thread(self):
        self.cng_dict = cinergia_read_modbus()
        # Aktualisieren der StringVars
        for key in self.cng_dict:
            if key in self.labels:
                name_label, value_label = self.labels[key]
                value_label.config(text=self.cng_dict[key]['value'])

        if not self.labels:
            self.create_labels()


class Cms(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='CMS')
        self.grid(row=0, column=2, sticky='nsew')


class Evtec(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='EVTEC')
        self.grid(row=0, column=3, sticky='nsew')


App()
