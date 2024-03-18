import tkinter as tk
from tkinter import ttk


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
        self.grid(row=0, column=0, sticky='nsew')

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
        self.grid(row=0, column=1, sticky='nsew')

        self.create_widgets()

    def create_widgets(self):
        # Erstellen Sie Labels für die Werte
        value_labels = []
        for i in range(4):
            label = ttk.Label(self, text=f"Wert {i+1}: 0")
            label.pack(side=tk.BOTTOM)
            value_labels.append(label)


class Cms(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='CMS')
        self.grid(row=0, column=2, sticky='nsew')

class Evtec(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text='EVTEC')
        self.grid(row=0, column=3, sticky='nsew')


class Entry(ttk.Frame):
    def __init__(self, parent, label_text, button_text, label_background):
        super().__init__(parent)

        label = ttk.Label(self, text=label_text, background=label_background)
        button = ttk.Button(self, text=button_text)

        label.pack(expand=True, fill='both')
        button.pack(expand=True, fill='both', pady=10)

        self.pack(side='left', expand=True, fill='both', padx=20, pady=20)


App()