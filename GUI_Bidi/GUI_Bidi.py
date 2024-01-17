# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 15:37:44 2023

@author: Team-Bidi
"""

import tkinter as tk
from tkinter import ttk
from pyModbusTCP.client import ModbusClient
import struct
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib import dates as mdates


"""
# Verbindung zum Modbus-Server herstellen
client = ModbusClient(host='192.168.2.149', port=502)
client.open()
"""

### AKTUALISIERUNG AUSGELESENE WERTE ###

# Funktion für den aktuellen Status der CNG
def update_status():
    """
    if client.open():
        grafcet_status_register = 16000

        status_bytes = client.read_holding_registers(grafcet_status_register, 2)
        if status_bytes:
            global grafcet_status  # Variable die für Bedingungen in anderen Funktionen genutzt werden kann
            grafcet_status = (status_bytes[0] << 8) | status_bytes[1]

            status_translation = {
                2: "StandBy",
                3: "PreCharge",
                4: "Ready",
                5: "Run",
                6: "Warning",
                7: "Alarm"
            }
            status_label.config(text=f"Status:   {status_translation.get(grafcet_status, 'Unbekannt')}")

            if grafcet_status == 2:
                enable_button.config(state="normal")
                disable_button.config(state="disable")
                start_charging_button.config(state="disable")
                reset_button.config(state="disable")
                stop_charging_button.config(state="disable")

            elif grafcet_status == 4:
                disable_button.config(state="normal")
                enable_button.config(state="disable")
                start_charging_button.config(state="normal")
                reset_button.config(state="disable")
                stop_charging_button.config(state="disable")

            elif grafcet_status == 5:
                  stop_charging_button.config(state="normal")
                  disable_button.config(state="normal")
                  reset_button.config(state="disable")
                  enable_button.config(state="disable")

            elif grafcet_status == 6 or grafcet_status == 7:
                  reset_button.config(state="normal")
                  disable_button.config(state="normal")
                  enable_button.config(state="disable")
                  start_charging_button.config(state="disable")
                  stop_charging_button.config(state="disable")

        else:
            status_label.config(text="Fehler beim Lesen der Register.")
    else:
        status_label.config(text="Verbindung zum Modbus-Server fehlgeschlagen.")

    # Hier wird der aktuelle Grafcet-Status periodisch abgefragt. Zyklus hier ist 1000 ms
    root.after(1000, update_status)
    """
    return


# Funktion zum Auslesen der aktuellen Spannung zw. U und N (EuT-Side)
def update_voltage_un():
    """
    if client.open():
        voltage_un_register = 26094

        voltage_bytes = client.read_holding_registers(voltage_un_register, 2)
        if voltage_bytes:
            if len(voltage_bytes) == 2:
                msb = voltage_bytes[0]  # Wert des MSB-Registers
                lsb = voltage_bytes[1]  # Wert des LSB-Registers

                # Kombiniere die beiden Werte in einen 32-Bit-Wert (Big-Endian)
                combined_value = (msb << 16) | lsb

                # Konvertiere den kombinierten Wert in den Datentyp float32
                global voltage_un  # Variable die für Bedingungen in anderen Funktionen genutzt werden kann
                voltage_un = struct.unpack('!f', struct.pack('!I', combined_value))[0]

                voltage_un_label.config(text="{0:.2f}".format(voltage_un))  # Anzeige auf 2 Dezimalstellen
            else:
                voltage_un_label.config(text='Fehler beim Lesen des Registers')

    else:
        voltage_un_label.config(text="Verbindung zum Modbus-Server fehlgeschlagen.")

        # Hier wird der aktuelle Spannungswert UN periodisch abgefragt. Zyklus hier ist 1000 ms
    root.after(1000, update_voltage_un)
    """
    return


# Funktion zum Auslesen des aktuellen Gesamt-Stroms (EuT-Side)
def update_current_total():
    """
    if client.open():
        current_total_register = 26106

        current_bytes = client.read_holding_registers(current_total_register, 2)
        if current_bytes:
            if len(current_bytes) == 2:
                msb = current_bytes[0]  # Wert des MSB-Registers
                lsb = current_bytes[1]  # Wert des LSB-Registers

                # Kombiniere die beiden Werte in einen 32-Bit-Wert (Big-Endian)
                combined_value = (msb << 16) | lsb

                # Konvertiere den kombinierten Wert in den Datentyp float32
                global current_total  # Variable die für Bedingungen in anderen Funktionen genutzt werden kann
                current_total = struct.unpack('!f', struct.pack('!I', combined_value))[0]

                current_total_label.config(text="{0:.2f}".format(current_total))  # Anzeige auf 2 Dezimalstellen
            else:
                current_total_label.config(text='Fehler beim Lesen des Registers')

    else:
        current_total_label.config(text="Verbindung zum Modbus-Server fehlgeschlagen.")

        # Hier wird der aktuelle Stromwert WN periodisch abgefragt. Zyklus hier ist 1000 ms
    root.after(1000, update_current_total)
    """
    return


def update_power_total():
    """
    if client.open():
        power_total_register = 26120

        power_bytes = client.read_holding_registers(power_total_register, 2)
        if power_bytes:
            if len(power_bytes) == 2:
                msb = power_bytes[0]  # Wert des MSB-Registers
                lsb = power_bytes[1]  # Wert des LSB-Registers

                # Kombiniere die beiden Werte in einen 32-Bit-Wert (Big-Endian)
                combined_value = (msb << 16) | lsb

                # Konvertiere den kombinierten Wert in den Datentyp float32
                global power_total  # Variable die für Bedingungen in anderen Funktionen genutzt werden kann
                power_total = struct.unpack('!f', struct.pack('!I', combined_value))[0]

                power_total_label.config(
                    text="{0:.2f}".format(power_total))  # Anzeige auf 2 Dezimalstellen
            else:
                power_total_label.config(text='Fehler beim Lesen des Registers')

    else:
        power_total_label.config(text="Verbindung zum Modbus-Server fehlgeschlagen.")

    # Hier wird der aktuelle Spannungswert WN periodisch abgefragt. Zyklus hier ist 1000 ms
    root.after(1000, update_power_total)
    """
    return




### SCHALTFLÄCHEN 1 ###

# Funktionen für die Schaltflächen
def enable_cng():
    """
    if client.open() and grafcet_status == 2:
        enable_disable_cng_register = 17000

        value_to_write = 1
        byte0 = (value_to_write >> 24) & 0xFF
        byte1 = (value_to_write >> 16) & 0xFF
        byte2 = (value_to_write >> 8) & 0xFF
        byte3 = value_to_write & 0xFF

        client.write_multiple_registers(enable_disable_cng_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])
        print("Schaltfläche Enable_CNG betätigt")
        """
    return


def disable_cng():
    """
    if client.open() and grafcet_status >= 4:
        enable_disable_cng_register = 17000

        value_to_write = 0
        byte0 = (value_to_write >> 24) & 0xFF
        byte1 = (value_to_write >> 16) & 0xFF
        byte2 = (value_to_write >> 8) & 0xFF
        byte3 = value_to_write & 0xFF

        client.write_multiple_registers(enable_disable_cng_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])
    print("Schaltfläche Disable_CNG betätigt")
    """
    return


def reset_alarm_warning():
    """

    ## ---> Hier noch überlegen, ob Ladevorgang bei Status Alarm automatisch abgebrochen werden soll? Das Gleiche für Status Warning überlegen! ##

    if client.open() and grafcet_status == 6 or grafcet_status ==7: # Status 6 = Warning, Status 7 = Alarm
        start_charging_button.config(state="normal")

        reset_register = 17018

        # Sequenz erstellen
        sequence = [0, 1, 0]

        values = [sequence[0] << 8 | sequence[1], sequence[1] << 8 | sequence[2]]

        # Werte in das Register schreiben
        client.write_multiple_registers(reset_register, values)

        print("Schaltfläche Reset betätigt")
        print("Sequenz [0, 1, 0] wurde erfolgreich in das Modbus-Register geschrieben.")

    else:
        print("Sequenz [0, 1, 0] wurde nicht in das Register geschrieben!")
        """
    return



### DROPDOWN-MENÜ "CONTROL OPERATION" ###

# Funktion, die INDIREKT durch Betätigung des Dropdown-Menüs "Control Operation" aufgerufen wird
def update_operation_combo_states():

    global selected_operation  # Globale Variable, die für Fkt "control_operation_selected(event)" und für Schaltfläche "Start Charging" als if-Bedingung verwendet wird
    selected_operation = control_operation_var.get()
    print("Die Operation-Variable lautet:", selected_operation, "; Datentyp:", type(selected_operation))


    # Basierend auf der Auswahl in "Control Operation" aktiviere die entsprechenden Schaltflächen
    if selected_operation == "Laden":
        current_ch_static_combo.config(state="normal")
        current_dch_static_combo.config(state="disabled")

    elif selected_operation == "Entladen":
        current_dch_static_combo.config(state="normal")
        current_ch_static_combo.config(state="disabled")


# Funktion, die DIREKT durch Betätigung des Dropdown-Menüs "Control Operation" aufgerufen wird
def control_operation_selected(event):  # event-Argument hier wichtig, damit Fkt bei jeder Betätigung des Dropdown-Menüs aufgerufen wird!
    update_operation_combo_states()  # Aufruf einer weiteren Funktion, um Aktivierung/Deaktivierung von Schaltflächen und Dropdown-Menüs je nach Dropdown-Auswahl von "Control Operation" zu steuern

    mode_translation = {
        1: "Current",
        2: "Power"
    }
    """

    if selected_operation == "Power":
        control_operation_ph_u_write_register = 17004

        value_to_write = 2
        byte0 = (value_to_write >> 24) & 0xFF
        byte1 = (value_to_write >> 16) & 0xFF
        byte2 = (value_to_write >> 8) & 0xFF
        byte3 = value_to_write & 0xFF

        client.write_multiple_registers(control_operation_ph_u_write_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])

        control_operation_ph_u_read_register = 16022
        operation_bytes = client.read_holding_registers(control_operation_ph_u_read_register, 2)  # Lesen von 2 16-Bit-Registern

        control_operation = (operation_bytes[0] << 8) | operation_bytes[1]
        print(f"Control Operation Ph U: {mode_translation.get(control_operation, 'Unbekannt')}")


    elif selected_operation == "Current":
        control_operation_ph_u_register = 17004

        value_to_write = 1
        byte0 = (value_to_write >> 24) & 0xFF
        byte1 = (value_to_write >> 16) & 0xFF
        byte2 = (value_to_write >> 8) & 0xFF
        byte3 = value_to_write & 0xFF

        client.write_multiple_registers(control_operation_ph_u_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])

        control_operation_ph_u_read_register = 16022
        operation_bytes = client.read_holding_registers(control_operation_ph_u_read_register,2)  # Lesen von 2 16-Bit-Registern

        control_operation = (operation_bytes[0] << 8) | operation_bytes[1]
        print(f"Control Operation Ph U: {mode_translation.get(control_operation, 'Unbekannt')}")
        """
    return


### SCHALTFLÄCHEN 2 ###

### DROPDOWN-MENÜS + EINGABEFELDER ###

# Anzeige, dass Dropdown-Menü betätigt wurde
def current_ch_static_combo_selected(event):
    global current_ch
    global current_ch_int
    current_ch = current_ch_static_var.get()
    print("Dropdown-Menü von Current [static] betätigt:", current_ch, "A", "; Datentyp:", type(current_ch))
    current_ch_int = int(current_ch)
    print("---current_ch_int =", current_ch_int, "; Datentyp:", type(current_ch_int))

# Anzeige, dass Dropdown-Menü betätigt wurde
def current_dch_static_combo_selected(event):
    global current_dch
    global current_dch_int
    current_dch = current_dch_static_var.get()
    print("Dropdown-Menü von Current [static] betätigt", current_dch, "A", "; Datentyp:", type(current_dch))
    current_dch_int = int(current_dch)
    print("---current_dch_int =", current_dch_int, "; Datentyp:", type(current_dch_int))


### FUNKTIONEN, DIE ÜBER IF-BEDINGUNGEN IN DER FKT VON DER SCHALTFLÄCHE "START CHARGING" AUFGERUFEN WIRD ###

def charge_control_current_static():
    """
    print("Aufruf Fkt charge_control_current_static()")

    ### Zuerst alle 3 Phasen einschalten. Stromwert aus Dropdown-Auswahl fließt über jede einzelne Phase! ###

    # Phase U einschalten
    on_off_ph_u_register = 17010

    value_to_write = 1
    byte0 = (value_to_write >> 24) & 0xFF
    byte1 = (value_to_write >> 16) & 0xFF
    byte2 = (value_to_write >> 8) & 0xFF
    byte3 = value_to_write & 0xFF

    client.write_multiple_registers(on_off_ph_u_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])
    time.sleep(1)  # Hier Wartezeit, damit CNG ausreichend Zeit hat alle Phasen einzuschalten


    if current_static_var.get() == "6 A":
        print("Dropdown-Auswahl: 6 A")


        # Stromvorgabe Phase U
        current_fundamental_ac_ph_u_register = 27072
        value_to_write = -6.0

        # Umwandeln des Gleitkommawerts in 4 Bytes im Big-Endian-Format
        value_bytes = struct.pack('>f', value_to_write)

        # Extrahieren der Bytes in der richtigen Reihenfolge
        byte0 = value_bytes[0]
        byte1 = value_bytes[1]
        byte2 = value_bytes[2]
        byte3 = value_bytes[3]

        # Schreiben der Bytes in die Register
        client.write_multiple_registers(current_fundamental_ac_ph_u_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])


    if current_static_var.get() == "8 A":
        print("Dropdown-Auswahl: 8 A")

        # Stromvorgabe Phase U
        current_fundamental_ac_ph_u_register = 27072
        value_to_write = -8.0

        # Umwandeln des Gleitkommawerts in 4 Bytes im Big-Endian-Format
        value_bytes = struct.pack('>f', value_to_write)

        # Extrahieren der Bytes in der richtigen Reihenfolge
        byte0 = value_bytes[0]
        byte1 = value_bytes[1]
        byte2 = value_bytes[2]
        byte3 = value_bytes[3]

        # Schreiben der Bytes in die Register
        client.write_multiple_registers(current_fundamental_ac_ph_u_register,[byte0 << 8 | byte1, byte2 << 8 | byte3])


    if current_static_var.get() == "10 A":
        print("Dropdown-Auswahl: 10 A")

        # Stromvorgabe Phase U
        current_fundamental_ac_ph_u_register = 27072
        value_to_write = -10.0

        # Umwandeln des Gleitkommawerts in 4 Bytes im Big-Endian-Format
        value_bytes = struct.pack('>f', value_to_write)

        # Extrahieren der Bytes in der richtigen Reihenfolge
        byte0 = value_bytes[0]
        byte1 = value_bytes[1]
        byte2 = value_bytes[2]
        byte3 = value_bytes[3]

        # Schreiben der Bytes in die Register
        client.write_multiple_registers(current_fundamental_ac_ph_u_register,[byte0 << 8 | byte1, byte2 << 8 | byte3])


    if current_static_var.get() == "13 A":
        print("Dropdown-Auswahl: 13 A")

        # Stromvorgabe Phase U
        current_fundamental_ac_ph_u_register = 27072
        value_to_write = -13.0

        # Umwandeln des Gleitkommawerts in 4 Bytes im Big-Endian-Format
        value_bytes = struct.pack('>f', value_to_write)

        # Extrahieren der Bytes in der richtigen Reihenfolge
        byte0 = value_bytes[0]
        byte1 = value_bytes[1]
        byte2 = value_bytes[2]
        byte3 = value_bytes[3]

        # Schreiben der Bytes in die Register
        client.write_multiple_registers(current_fundamental_ac_ph_u_register,[byte0 << 8 | byte1, byte2 << 8 | byte3])


    if current_static_var.get() == "16 A":
        print("Dropdown-Auswahl: 16 A")

        # Stromvorgabe Phase U
        current_fundamental_ac_ph_u_register = 27072
        value_to_write = -16.0

        # Umwandeln des Gleitkommawerts in 4 Bytes im Big-Endian-Format
        value_bytes = struct.pack('>f', value_to_write)

        # Extrahieren der Bytes in der richtigen Reihenfolge
        byte0 = value_bytes[0]
        byte1 = value_bytes[1]
        byte2 = value_bytes[2]
        byte3 = value_bytes[3]

        # Schreiben der Bytes in die Register
        client.write_multiple_registers(current_fundamental_ac_ph_u_register,[byte0 << 8 | byte1, byte2 << 8 | byte3])


    # Selektierte Stromvorgabe senden
    trigger_config_register = 17020

    value_to_write = 1

    byte0 = (value_to_write >> 24) & 0xFF
    byte1 = (value_to_write >> 16) & 0xFF
    byte2 = (value_to_write >> 8) & 0xFF
    byte3 = value_to_write & 0xFF

    client.write_multiple_registers(trigger_config_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])
    """
    return


### SCHALTFLÄCHEN 3 ###

# Funktionen für Schaltflächen
def start_charging():
    """

    if client.open() and grafcet_status >= 4: # Status 4 = Ready, Status 5 = Run

        run_ready_register = 17002

        value_to_write = 1
        byte0 = (value_to_write >> 24) & 0xFF
        byte1 = (value_to_write >> 16) & 0xFF
        byte2 = (value_to_write >> 8) & 0xFF
        byte3 = value_to_write & 0xFF

        client.write_multiple_registers(run_ready_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])
        print("Schaltfläche Start Charging betätigt")
        time.sleep(1)

        if grafcet_status ==4:
            time.sleep(1) # Hier Wartezeit, damit CNG ausreichend Zeit hat in Status "Run" zu gehen

        if selected_operation == "Power": # Auswahl Dropdown-Menü "Control Operation"
            if power_static_state == 1: # Globale Variable aus Fkt "enable_power_static()"
                charge_control_power_static() # Aufruf Funktion
                print("Funktion charge_control_power_static() erfolgreich aufgerufen")

            if power_automatic_state == 1: # Globale Variable aus Fkt "enable_power_automatic()"
                charge_control_power_automatic()
                print("Funktion charge_control_power_automatic() erfolgreich aufgerufen")

            if power_manual_state == 1: # Globale Variable aus Fkt "enable_power_manual()"
                charge_control_power_manual() # Aufruf Funktion
                print("Funktion charge_control_power_manual() erfolgreich aufgerufen")


        if selected_operation == "Current": # Auswahl Dropdown-Menü "Control Operation"
            if current_static_state == 1: # Globale Variable aus Fkt "enable_current_static()"
                charge_control_current_static() # Aufruf Funktion
                print("Funktion charge_control_current_static() erfolgreich aufgerufen")

            if current_automatic_state == 1: # Globale Variable aus Fkt "enable_current_automatic()"
                charge_control_current_automatic() # Aufruf Funktion
                print("Funktion charge_control_current_automatic() erfolgreich aufgerufen")

            if current_manual_state == 1: # Globale Variable aus Fkt "enable_current_manual()"
                charge_control_current_manual() # Aufruf Funktion
                print("Funktion charge_control_current_manual() erfolgreich aufgerufen")
                """
    return

def stop_charging():
    """
    run_ready_register = 17002

    value_to_write = 0
    byte0 = (value_to_write >> 24) & 0xFF
    byte1 = (value_to_write >> 16) & 0xFF
    byte2 = (value_to_write >> 8) & 0xFF
    byte3 = value_to_write & 0xFF

    client.write_multiple_registers(run_ready_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])
    print("Schaltfläche Stop Charging betätigt")
    """
    return



# Erstellen des GUI-Hauptfensters
root = tk.Tk()
root.title("EV-Emulator")

"""
get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = screen_width
window_height = screen_height
# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)
root.attributes('-topmost', 1)
"""


# Erstellen eines Frames für den 1. Bereich von links, "Charge Parameter"
frame_0_0 = ttk.LabelFrame(text="Charge Parameter")
frame_0_0.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
#frame_0_0.columnconfigure(0, weight=1)

#

# Erstellen eines weiteren Frames ohne Überschrift innerhalb des Frames "Charge Parameter"
no_header_frame_0_0 = ttk.LabelFrame(frame_0_0, text="")
no_header_frame_0_0.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
#no_header_frame_0_0.columnconfigure(0, weight=1)

# Erstellen des Dropdown-Menüs für "Control Operation" im MITTLEREN Frame
control_operation_var = tk.StringVar()
control_operation_label = ttk.Label(no_header_frame_0_0, text="Control Operation:")
control_operation_combo = ttk.Combobox(no_header_frame_0_0, textvariable=control_operation_var, values=["Laden", "Entladen"], state="readonly")

# Positionieren des Labels und des Dropdown-Menüs "Control Operation" im MITTLEREN Frame
control_operation_label.grid(row=1, column=0, padx=5, pady=5)
control_operation_combo.grid(row=1, column=1, padx=5, pady=5)

# Verknüpfung der Dropdown-Auswahl der Control Operation an die entsprechende Funktion im MITTLEREN Frame
control_operation_combo.bind("<<ComboboxSelected>>", control_operation_selected)  # Durch bind-Methode wird Fkt "control_operation_selected(event)" jedes Mal bei Benutzung des Dropdown-Menüs aufgerufen (-->EVENT!!!)

#

# Erstellen eines weiteren Frames "Voltage Control EuT-Side" innerhalb des Frames "Charge Parameter"
voltage_control_frame = ttk.LabelFrame(frame_0_0, text="Voltage Control --> Cinergia")
voltage_control_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
#voltage_control_frame.columnconfigure(0, weight=1)


# Erstellen des Dropdown-Menüs für "Voltage [static]" im MITTLEREN Frame
voltage_static_label = ttk.Label(voltage_control_frame, text="Voltage [static] fixed on 400V.")
voltage_static_label.config(state="normal")

# Positionieren des Labels und des Dropdown-Menüs "Voltage [static]" im MITTLEREN Frame
voltage_static_label.grid(row=3, column=0, padx=5, pady=5)

#

# Erstellen eines weiteren Frames "Charge Current Control EuT-Side" innerhalb des Frames "Charge Parameter"
current_ch_control_frame = ttk.LabelFrame(frame_0_0, text="Charge Current --> CMS")
current_ch_control_frame.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")
#current_dch_control_frame.columnconfigure(0, weight=1)


# Erstellen des Dropdown-Menüs für "Current [static]" im MITTLEREN Frame
current_ch_static_var = tk.StringVar()
current_ch_static_label = ttk.Label(current_ch_control_frame, text="Charge Current in A:" )
current_ch_static_combo = ttk.Combobox(current_ch_control_frame, textvariable=current_ch_static_var, values=["6", "8", "10", "13", "16"], state="readonly")
current_ch_static_combo.config(state="disabled")

# Positionieren des Labels und des Dropdown-Menüs "Voltage [static]" im MITTLEREN Frame
current_ch_static_label.grid(row=6, column=0, padx=5, pady=5)
current_ch_static_combo.grid(row=6, column=1, padx=5, pady=5)

# Verknüpfung der Dropdown-Auswahl der Current [static] an die entsprechende Funktion im MITTLEREN Frame
current_ch_static_combo.bind("<<ComboboxSelected>>", current_ch_static_combo_selected) # --> Funktion wird nur zur Anzeige der Betätigung des Dropdown-Menüs im Terminal verwendet

#

# Erstellen eines weiteren Frames "Discharge Current Control EuT-Side" innerhalb des Frames "Charge Parameter"
current_dch_control_frame = ttk.LabelFrame(frame_0_0, text="")
current_dch_control_frame.grid(row=8, column=0, padx=10, pady=10, sticky="nsew")
#current_dch_control_frame.columnconfigure(0, weight=1)

# Erstellen des Dropdown-Menüs für "Current [static]" im MITTLEREN Frame
current_dch_static_var = tk.StringVar()
current_dch_static_label = ttk.Label(current_dch_control_frame, text="Discharge Current --> CMS" )
current_dch_static_combo = ttk.Combobox(current_dch_control_frame, textvariable=current_dch_static_var, values=["6", "8", "10", "13", "16"], state="readonly")
current_dch_static_combo.config(state="disabled")

# Positionieren des Labels und des Dropdown-Menüs "Voltage [static]" im MITTLEREN Frame
current_dch_static_label.grid(row=9, column=0, padx=5, pady=5)
current_dch_static_combo.grid(row=9, column=1, padx=5, pady=5)

# Verknüpfung der Dropdown-Auswahl der Current [static] an die entsprechende Funktion im MITTLEREN Frame
current_dch_static_combo.bind("<<ComboboxSelected>>", current_dch_static_combo_selected) # --> Funktion wird nur zur Anzeige der Betätigung des Dropdown-Menüs im Terminal verwendet

#
#
#

# Erstellen des Frames für den LINKEN Bereich "Controllable Load" (Tab3)
left_frame = ttk.LabelFrame(text="Controllable Load")
left_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Erstellen des Frames für den LINKEN Bereich "Controllable Load"
control_left_frame = ttk.LabelFrame(left_frame, text="Control Cinergia")
control_left_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Konfigurieren der Spalten im LINKEN Frame, um die Schaltflächen im no_header_left_frame zu zentrieren
control_left_frame.columnconfigure(0, weight=1)
control_left_frame.columnconfigure(1, weight=1)
control_left_frame.columnconfigure(2, weight=1)

# Erstellen eines weiteren Frames "Voltage EuT-Side" innerhalb des Frames "Controllable Load"
voltage_display_frame = ttk.LabelFrame(left_frame, text="Voltage EuT-Side")
voltage_display_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

# Erstellen eines weiteren Frames "Current EuT-Side" innerhalb des Frames "Controllable Load"
current_display_frame = ttk.LabelFrame(left_frame, text="Current EuT-Side")
current_display_frame.grid(row=8, column=0, padx=10, pady=10, sticky="nsew")

# Erstellen eines weiteren Frames "Power EuT-Side" innerhalb des Frames "Controllable Load"
power_display_frame = ttk.LabelFrame(left_frame, text="Power EuT-Side")
power_display_frame.grid(row=12, column=0, padx=10, pady=10, sticky="nsew")





# Erstellen eines Frames für den RECHTEN Bereich "Charge Process" (Tab3)
right_frame = ttk.LabelFrame(text="Charge Process")
right_frame.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

# Erstellen des Frames für den RECHTEN Bereich "Charge Process"
no_header_right_frame = ttk.LabelFrame(right_frame, text="")
no_header_right_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")


# Erstellen der Schaltflächen "Enable CNG", "Disable CNG" und "Reset" im LINKEN Frame
enable_button = ttk.Button(control_left_frame, text="Enable CNG", command=enable_cng)
disable_button = ttk.Button(control_left_frame, text="Disable CNG", state="disabled", command=disable_cng)
reset_button = ttk.Button(control_left_frame, text="Reset", state="disabled", command=reset_alarm_warning)

# Erstellen der Schaltflächen "Start Charging", "Stop Charging"  im RECHTEN Frame
start_charging_button = ttk.Button(no_header_right_frame, text="Start Charging", state="disabled", command=start_charging)
stop_charging_button = ttk.Button(no_header_right_frame, text="Stop Charging", state="disabled", command=stop_charging)

# Positionieren der Schaltflächen im RECHTEN Frame
start_charging_button.grid(row=1, column=0, padx=5, pady=5)
stop_charging_button.grid(row=1, column=1, padx=5, pady=5)

# Konfigurieren der Spalten im RECHTEN Frame, um die Schaltflächen zu zentrieren
no_header_right_frame.columnconfigure(0, weight=1)
no_header_right_frame.columnconfigure(1, weight=1)


# Erstellen der Statusanzeige im LINKEN Frame
#status_label_fix = ttk.Label(left_frame, text="Status:")
status_label = ttk.Label(control_left_frame, text="")
update_status() # Aufruf der Funktion. Ausgelesener Wert aus Funktion wird an vorherige Label-Variable übergeben


# Erstellen eines Labels zur Anzeige von Spannungswerten im LINKEN Frame "voltage_display_frame"
voltage_un_label_fix = ttk.Label(voltage_display_frame, text="Voltage U-N:")
voltage_un_label = ttk.Label(voltage_display_frame, text="")
update_voltage_un()  # Aufruf der Funktion. Ausgelesener Wert wird hier in vorherige Label-Variable geschrieben
unit_label_un = ttk.Label(voltage_display_frame, text="[V_rms]")


# Erstellen eines Labels zur Anzeige von Stromwerten im LINKEN Frame "current_display_frame"
current_total_label_fix = ttk.Label(current_display_frame, text="Current total:")
current_total_label = ttk.Label(current_display_frame, text="")
update_current_total()  # Aufruf der Funktion. Ausgelesener Wert wird hier in vorherige Label-Variable geschrieben
unit_label_current_total = ttk.Label(current_display_frame, text="[A_rms]")


# Erstellen eines Labels zur Anzeige der einzelnen Leistungen im LINKEN Frame "power_display_frame"
power_total_label_fix = ttk.Label(power_display_frame, text="Power total:")
power_total_label = ttk.Label(power_display_frame, text="")
update_power_total()  # Aufruf der Funktion. Ausgelesener Wert wird hier in vorherige Label-Variable geschrieben
unit_label_power_total = ttk.Label(power_display_frame, text="[W]")


# Positionieren der Schaltflächen, der Statusanzeige und dem Rest im LINKEN Frame
status_label.grid(row=0, column=1, padx=0, pady=0)
enable_button.grid(row=1, column=0, padx=0, pady=5)
disable_button.grid(row=1, column=1, padx=0, pady=5)
reset_button.grid(row=1, column=2, padx=0, pady=5)
voltage_un_label_fix.grid(row=5, column=3, padx=5, pady=5)
voltage_un_label.grid(row=5, column=4, padx=5, pady=5)
unit_label_un.grid(row=5, column=5, padx=5, pady=5)
current_total_label_fix.grid(row=10, column=3, padx=5, pady=5)
current_total_label.grid(row=10, column=4, padx=5, pady=5)
unit_label_current_total.grid(row=10, column=5, padx=5, pady=5)
power_total_label_fix.grid(row=14, column=3, padx=5, pady=5)
power_total_label.grid(row=14, column=4, padx=5, pady=5)
unit_label_power_total.grid(row=14, column=5, padx=5, pady=5)



# Starten der GUI
root.mainloop()