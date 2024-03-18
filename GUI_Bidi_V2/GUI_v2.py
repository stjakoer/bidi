import threading
import tkinter as tk
from tkinter import ttk
from connect.connect_cinergia import cinergia_read_modbus, cinergia_write_modbus
from connect.connect_evtec import evtec_read_modbus
from connect.connect_cms import cms_canbus_listener


class App(tk.Tk):
    def __init__(self):
        # main setup
        super().__init__()
        self.title('Bidi Masterprojekt')
        self.geometry('1920x1080')

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

        cng_control_frame.grid(row=2, column=0, pady=10, columnspan=2, sticky='nsew')
        button_enable_cng.grid(row=0, column=0, sticky='nsew', ipady=10)
        button_disable_cng.grid(row=0, column=1, sticky='nsew', ipady=10)
        button_reset_cng.grid(row=1, column=0, columnspan=2, sticky='nsew', ipady=10)
        button_start_cng.grid(row=2, column=0, sticky='nsew', ipady=10)
        button_stop_cng.grid(row=2, column=1, sticky='nsew', ipady=10)

        button_start_charging.grid(row=3, column=0, columnspan=2, sticky='nsew', ipady=20)
        button_stop_charging.grid(row=4, column=0, columnspan=2, sticky='nsew', ipady=20)

    def no_connection(self, status):
        pass

    def reset_button(self):
        pass


class Cinergia(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='Cinergia')
        self.grid(row=0, column=1, sticky='N', ipadx=50)

        self.cng_dict = {}
        self.labels = {}

        self.update_dict()

        self.status_label = StatusLabel(self)
        self.no_connect = Control(self)

    def create_cng_labels(self):
        for labels in self.labels.values():
            for label in labels:
                label.destroy()

        self.labels = {}
        for i, key in enumerate(self.cng_dict):
            # Label für den Namen
            name_label = ttk.Label(self, text=self.cng_dict[key]['name']+':')
            name_label.grid(row=i, column=0, sticky='W')

            # Label für den Wert
            value_label = ttk.Label(self, text=self.cng_dict[key]['value'])
            value_label.grid(row=i, column=1)

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
            self.create_cng_labels()

        if self.cng_dict[16000]['value'] is not None:
            self.status_label.update_status(True)
            self.no_connect.no_connection((False))
        else:
            self.status_label.update_status(False)
            self.no_connect.no_connection(True)


class Cms(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='CMS')
        self.grid(row=0, column=2, sticky='N', ipadx=50)

        self.cms_dict = {}
        self.labels = {}

        self.update_dict()

        self.status_label = StatusLabel(self)   # andere Klasse einbinden

    def create_labels(self):
        for labels in self.labels.values():
            for label in labels:
                label.destroy()

        self.labels = {}
        for i, key in enumerate(self.cms_dict):
            # Label für den Namen
            name_label = ttk.Label(self, text=key+':')
            name_label.grid(row=i, column=0, sticky='W')

            # Label für den Wert
            value_label = ttk.Label(self, text=self.cms_dict[key])
            value_label.grid(row=i, column=1)

            # Speichern Sie die Labels in self.labels
            self.labels[key] = (name_label, value_label)

    def update_dict(self):
        thread = threading.Thread(target=self.update_dict_thread, daemon=True)
        thread.start()

        self.after(1000, self.update_dict)

    def update_dict_thread(self):
        self.cms_dict = cms_canbus_listener()
        # Aktualisieren der StringVars
        for key in self.cms_dict:
            if key in self.labels:
                name_label, value_label = self.labels[key]
                value_label.config(text=self.cms_dict[key])

        if not self.labels:
            self.create_labels()

        connected = self.cms_dict['StateMachineState'] is not None
        self.status_label.update_status(connected)


class Evtec(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='EVTEC')
        self.grid(row=0, column=3, sticky='N', ipadx=50)

        self.evt_dict = {}
        self.labels = {}

        self.update_dict()

        self.status_label = StatusLabel(self)

    def create_labels(self):
        for labels in self.labels.values():
            for label in labels:
                label.destroy()

        for i, key in enumerate(self.evt_dict):
            # Label für den Namen
            name_label = ttk.Label(self, text=self.evt_dict[key]['name']+':')
            name_label.grid(row=i, column=0, sticky='W')

            # Label für den Wert
            value_label = ttk.Label(self, text=self.evt_dict[key]['value'])
            value_label.grid(row=i, column=1)

            # Speichern Sie die Labels in self.labels
            self.labels[key] = (name_label, value_label)

    def update_dict(self):
        thread = threading.Thread(target=self.update_dict_thread, daemon=True)
        thread.start()

        self.after(1000, self.update_dict)

    def update_dict_thread(self):
        self.evt_dict = evtec_read_modbus()
        # Aktualisieren der StringVars
        for key in self.evt_dict:
            if key in self.labels:
                name_label, value_label = self.labels[key]
                value_label.config(text=self.evt_dict[key]['value'])

        if not self.labels:
            self.create_labels()

        connected = self.evt_dict[0]['value'] is not None
        self.status_label.update_status(connected)


#   Hilfreiche Klassen:
class StatusLabel(ttk.Label):
    def __init__(self, parent):
        super().__init__(parent, text='Boot...', font=('Calibri', 16))
        self.grid(row=25, column=0, columnspan=2, pady=10)

    def update_status(self, connected):
        if connected:
            self.config(text='Connected')
        else:
            self.config(text='No Connection')


App()
