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



# Verbindung zum Modbus-Server herstellen
client = ModbusClient(host='192.168.2.149', port=502)
client.open()


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
def update_button_and_combo_states():

    global selected_operation  # Globale Variable, die für Fkt "control_operation_selected(event)" und für Schaltfläche "Start Charging" als if-Bedingung verwendet wird
    selected_operation = control_operation_var.get()


    # Basierend auf der Auswahl in "Control Operation" aktiviere die entsprechenden Schaltflächen
    if selected_operation == "Laden":
        power_static_button.config(state="normal")
        power_automatic_button.config(state="normal")
        current_static_button.config(state="disabled")
        current_automatic_button.config(state="disabled")
        current_static_combo.config(state="disabled")
        current_automatic_combo.config(state="disabled")

    elif selected_operation == "Entladen":
        current_static_button.config(state="normal")
        current_automatic_button.config(state="normal")
        power_static_button.config(state="disabled")
        power_automatic_button.config(state="disabled")
        power_static_combo.config(state="disabled")
        power_automatic_combo.config(state="disabled")


# Funktion, die DIREKT durch Betätigung des Dropdown-Menüs "Control Operation" aufgerufen wird
def control_operation_selected(event):  # event-Argument hier wichtig, damit Fkt bei jeder Betätigung des Dropdown-Menüs aufgerufen wird!
    update_button_and_combo_states() # Aufruf einer weiteren Funktion, um Aktivierung/Deaktivierung von Schaltflächen und Dropdown-Menüs je nach Dropdown-Auswahl von "Control Operation" zu steuern

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


        control_operation_ph_v_register = 17006

        value_to_write = 2
        byte0 = (value_to_write >> 24) & 0xFF
        byte1 = (value_to_write >> 16) & 0xFF
        byte2 = (value_to_write >> 8) & 0xFF
        byte3 = value_to_write & 0xFF

        client.write_multiple_registers(control_operation_ph_v_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])

        control_operation_ph_v_read_register = 16024
        operation_bytes = client.read_holding_registers(control_operation_ph_v_read_register,2)  # Lesen von 2 16-Bit-Registern

        control_operation = (operation_bytes[0] << 8) | operation_bytes[1]
        print(f"Control Operation Ph V: {mode_translation.get(control_operation, 'Unbekannt')}")


        control_operation_ph_w_register = 17008

        value_to_write = 2
        byte0 = (value_to_write >> 24) & 0xFF
        byte1 = (value_to_write >> 16) & 0xFF
        byte2 = (value_to_write >> 8) & 0xFF
        byte3 = value_to_write & 0xFF

        client.write_multiple_registers(control_operation_ph_w_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])

        control_operation_ph_w_read_register = 16026
        operation_bytes = client.read_holding_registers(control_operation_ph_w_read_register, 2)  # Lesen von 2 16-Bit-Registern

        control_operation = (operation_bytes[0] << 8) | operation_bytes[1]
        print(f"Control Operation Ph W: {mode_translation.get(control_operation, 'Unbekannt')}")


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


        control_operation_ph_v_register = 17006

        value_to_write = 1
        byte0 = (value_to_write >> 24) & 0xFF
        byte1 = (value_to_write >> 16) & 0xFF
        byte2 = (value_to_write >> 8) & 0xFF
        byte3 = value_to_write & 0xFF

        client.write_multiple_registers(control_operation_ph_v_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])

        control_operation_ph_v_read_register = 16024
        operation_bytes = client.read_holding_registers(control_operation_ph_v_read_register, 2)  # Lesen von 2 16-Bit-Registern

        control_operation = (operation_bytes[0] << 8) | operation_bytes[1]
        print(f"Control Operation Ph V: {mode_translation.get(control_operation, 'Unbekannt')}")


        control_operation_ph_w_register = 17008

        value_to_write = 1
        byte0 = (value_to_write >> 24) & 0xFF
        byte1 = (value_to_write >> 16) & 0xFF
        byte2 = (value_to_write >> 8) & 0xFF
        byte3 = value_to_write & 0xFF

        client.write_multiple_registers(control_operation_ph_w_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])

        control_operation_ph_w_read_register = 16026
        operation_bytes = client.read_holding_registers(control_operation_ph_w_read_register,2)  # Lesen von 2 16-Bit-Registern

        control_operation = (operation_bytes[0] << 8) | operation_bytes[1]
        print(f"Control Operation Ph W: {mode_translation.get(control_operation, 'Unbekannt')}")
        """
    return



### SCHALTFLÄCHEN 2 ###

# Funktion, die durch Betätigung der Schaltfläche "Power [static]" aufgerufen wird
def enable_power_static():
    print("Schaltfläche Power [static] betätigt")
    power_static_combo.config(state="normal")
    power_automatic_combo.config(state="disabled")
    global power_static_state
    power_static_state = 1 # Notwendig für if-Bedingung von Funktion "start_charging"
    global power_automatic_state
    power_automatic_state = 0 # Wichtig hier Variable auf 0 zu setzen, damit nur eine if-Bedingung von Funktion "start_charging" erfüllt ist!
    global power_manual_state
    power_manual_state = 0 # Wichtig hier Variable auf 0 zu setzen, damit nur eine if-Bedingung von Funktion "start_charging" erfüllt ist!


# Funktion, die durch Betätigung der Schaltfläche "Power [automatic]" aufgerufen wird
def enable_power_automatic():
    print("Schaltfläche Power [automatic] betätigt")
    power_automatic_combo.config(state="normal")
    power_static_combo.config(state="disabled")
    global power_static_state
    power_static_state = 0 # Wichtig hier Variable auf 0 zu setzen, damit nur eine if-Bedingung von Funktion "start_charging" erfüllt ist!
    global power_automatic_state
    power_automatic_state = 1 # Notwendig für if-Bedingung von Funktion "start_charging"
    global power_manual_state
    power_manual_state = 0 # Wichtig hier Variable auf 0 zu setzen, damit nur eine if-Bedingung von Funktion "start_charging" erfüllt ist!


# Funktion, die durch Betätigung der Schaltfläche "Current [static]" aufgerufen wird
def enable_current_static():
    print("Schaltfläche Current [static] betätigt")
    current_static_combo.config(state="normal")
    current_automatic_combo.config(state="disabled")
    global current_static_state
    current_static_state = 1  # Notwendig für if-Bedingung von Funktion "start_charging"
    global current_automatic_state
    current_automatic_state = 0  # Wichtig hier Variable auf 0 zu setzen, damit nur eine if-Bedingung von Funktion "start_charging" erfüllt ist!
    global current_manual_state
    current_manual_state = 0  # Wichtig hier Variable auf 0 zu setzen, damit nur eine if-Bedingung von Funktion "start_charging" erfüllt ist!


# Funktion, die durch Betätigung der Schaltfläche "Current [automatic]" aufgerufen wird
def enable_current_automatic():
    print("Schaltfläche Current [automatic] betätigt")
    current_automatic_combo.config(state="normal")
    current_static_combo.config(state="disabled")
    global current_static_state
    current_static_state = 0  # Wichtig hier Variable auf 0 zu setzen, damit nur eine if-Bedingung von Funktion "start_charging" erfüllt ist!
    global current_automatic_state
    current_automatic_state = 1  # Notwendig für if-Bedingung von Funktion "start_charging"
    global current_manual_state
    current_manual_state = 0  # Wichtig hier Variable auf 0 zu setzen, damit nur eine if-Bedingung von Funktion "start_charging" erfüllt ist!


### DROPDOWN-MENÜS + EINGABEFELDER ###

# Anzeige, dass Dropdown-Menü betätigt wurde
def power_static_combo_selected(event):
    print("Dropdown-Menü von Power [static] betätigt")

# Anzeige, dass Dropdown-Menü betätigt wurde
def power_automatic_combo_selected(event):
    print("Dropdown-Menü von Power [automatic] betätigt")

# Anzeige, dass Dropdown-Menü betätigt wurde
def current_static_combo_selected(event):
    print("Dropdown-Menü von Current [static] betätigt")

# Anzeige, dass Dropdown-Menü betätigt wurde
def current_automatic_combo_selected(event):
    print("Dropdown-Menü von Current [automatic] betätigt")


### FUNKTIONEN, DIE ÜBER IF-BEDINGUNGEN IN DER FKT VON DER SCHALTFLÄCHE "START CHARGING" AUFGERUFEN WIRD ###

def charge_control_power_automatic():
    print("Aufruf Fkt charge_control_power_automatic()")
    pass


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

    # Phase V einschalten
    on_off_ph_v_register = 17012

    value_to_write = 1
    byte0 = (value_to_write >> 24) & 0xFF
    byte1 = (value_to_write >> 16) & 0xFF
    byte2 = (value_to_write >> 8) & 0xFF
    byte3 = value_to_write & 0xFF

    client.write_multiple_registers(on_off_ph_v_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])

    # Phase W einschalten
    on_off_ph_w_register = 17014

    value_to_write = 1
    byte0 = (value_to_write >> 24) & 0xFF
    byte1 = (value_to_write >> 16) & 0xFF
    byte2 = (value_to_write >> 8) & 0xFF
    byte3 = value_to_write & 0xFF

    client.write_multiple_registers(on_off_ph_w_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])

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


        # Stromvorgabe Phase V
        current_fundamental_ac_ph_v_register = 27080
        value_to_write = -6.0

        # Umwandeln des Gleitkommawerts in 4 Bytes im Big-Endian-Format
        value_bytes = struct.pack('>f', value_to_write)

        # Extrahieren der Bytes in der richtigen Reihenfolge
        byte0 = value_bytes[0]
        byte1 = value_bytes[1]
        byte2 = value_bytes[2]
        byte3 = value_bytes[3]

        # Schreiben der Bytes in die Register
        client.write_multiple_registers(current_fundamental_ac_ph_v_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])


        # Stromvorgabe Phase W
        current_fundamental_ac_ph_w_register = 27088
        value_to_write = -6.0

        # Umwandeln des Gleitkommawerts in 4 Bytes im Big-Endian-Format
        value_bytes = struct.pack('>f', value_to_write)

        # Extrahieren der Bytes in der richtigen Reihenfolge
        byte0 = value_bytes[0]
        byte1 = value_bytes[1]
        byte2 = value_bytes[2]
        byte3 = value_bytes[3]

        # Schreiben der Bytes in die Register
        client.write_multiple_registers(current_fundamental_ac_ph_w_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])


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

        # Stromvorgabe Phase V
        current_fundamental_ac_ph_v_register = 27080
        value_to_write = -8.0

        # Umwandeln des Gleitkommawerts in 4 Bytes im Big-Endian-Format
        value_bytes = struct.pack('>f', value_to_write)

        # Extrahieren der Bytes in der richtigen Reihenfolge
        byte0 = value_bytes[0]
        byte1 = value_bytes[1]
        byte2 = value_bytes[2]
        byte3 = value_bytes[3]

        # Schreiben der Bytes in die Register
        client.write_multiple_registers(current_fundamental_ac_ph_v_register,[byte0 << 8 | byte1, byte2 << 8 | byte3])

        # Stromvorgabe Phase W
        current_fundamental_ac_ph_w_register = 27088
        value_to_write = -8.0

        # Umwandeln des Gleitkommawerts in 4 Bytes im Big-Endian-Format
        value_bytes = struct.pack('>f', value_to_write)

        # Extrahieren der Bytes in der richtigen Reihenfolge
        byte0 = value_bytes[0]
        byte1 = value_bytes[1]
        byte2 = value_bytes[2]
        byte3 = value_bytes[3]

        # Schreiben der Bytes in die Register
        client.write_multiple_registers(current_fundamental_ac_ph_w_register,[byte0 << 8 | byte1, byte2 << 8 | byte3])

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

        # Stromvorgabe Phase V
        current_fundamental_ac_ph_v_register = 27080
        value_to_write = -10.0

        # Umwandeln des Gleitkommawerts in 4 Bytes im Big-Endian-Format
        value_bytes = struct.pack('>f', value_to_write)

        # Extrahieren der Bytes in der richtigen Reihenfolge
        byte0 = value_bytes[0]
        byte1 = value_bytes[1]
        byte2 = value_bytes[2]
        byte3 = value_bytes[3]

        # Schreiben der Bytes in die Register
        client.write_multiple_registers(current_fundamental_ac_ph_v_register,[byte0 << 8 | byte1, byte2 << 8 | byte3])

        # Stromvorgabe Phase W
        current_fundamental_ac_ph_w_register = 27088
        value_to_write = -10.0

        # Umwandeln des Gleitkommawerts in 4 Bytes im Big-Endian-Format
        value_bytes = struct.pack('>f', value_to_write)

        # Extrahieren der Bytes in der richtigen Reihenfolge
        byte0 = value_bytes[0]
        byte1 = value_bytes[1]
        byte2 = value_bytes[2]
        byte3 = value_bytes[3]

        # Schreiben der Bytes in die Register
        client.write_multiple_registers(current_fundamental_ac_ph_w_register,[byte0 << 8 | byte1, byte2 << 8 | byte3])


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

        # Stromvorgabe Phase V
        current_fundamental_ac_ph_v_register = 27080
        value_to_write = -13.0

        # Umwandeln des Gleitkommawerts in 4 Bytes im Big-Endian-Format
        value_bytes = struct.pack('>f', value_to_write)

        # Extrahieren der Bytes in der richtigen Reihenfolge
        byte0 = value_bytes[0]
        byte1 = value_bytes[1]
        byte2 = value_bytes[2]
        byte3 = value_bytes[3]

        # Schreiben der Bytes in die Register
        client.write_multiple_registers(current_fundamental_ac_ph_v_register,[byte0 << 8 | byte1, byte2 << 8 | byte3])

        # Stromvorgabe Phase W
        current_fundamental_ac_ph_w_register = 27088
        value_to_write = -13.0

        # Umwandeln des Gleitkommawerts in 4 Bytes im Big-Endian-Format
        value_bytes = struct.pack('>f', value_to_write)

        # Extrahieren der Bytes in der richtigen Reihenfolge
        byte0 = value_bytes[0]
        byte1 = value_bytes[1]
        byte2 = value_bytes[2]
        byte3 = value_bytes[3]

        # Schreiben der Bytes in die Register
        client.write_multiple_registers(current_fundamental_ac_ph_w_register,[byte0 << 8 | byte1, byte2 << 8 | byte3])


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

        # Stromvorgabe Phase V
        current_fundamental_ac_ph_v_register = 27080
        value_to_write = -16.0

        # Umwandeln des Gleitkommawerts in 4 Bytes im Big-Endian-Format
        value_bytes = struct.pack('>f', value_to_write)

        # Extrahieren der Bytes in der richtigen Reihenfolge
        byte0 = value_bytes[0]
        byte1 = value_bytes[1]
        byte2 = value_bytes[2]
        byte3 = value_bytes[3]

        # Schreiben der Bytes in die Register
        client.write_multiple_registers(current_fundamental_ac_ph_v_register,[byte0 << 8 | byte1, byte2 << 8 | byte3])

        # Stromvorgabe Phase W
        current_fundamental_ac_ph_w_register = 27088
        value_to_write = -16.0

        # Umwandeln des Gleitkommawerts in 4 Bytes im Big-Endian-Format
        value_bytes = struct.pack('>f', value_to_write)

        # Extrahieren der Bytes in der richtigen Reihenfolge
        byte0 = value_bytes[0]
        byte1 = value_bytes[1]
        byte2 = value_bytes[2]
        byte3 = value_bytes[3]

        # Schreiben der Bytes in die Register
        client.write_multiple_registers(current_fundamental_ac_ph_w_register,[byte0 << 8 | byte1, byte2 << 8 | byte3])



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

def charge_control_current_automatic():
    print("Aufruf Fkt charge_control_current_automatic()")
    pass



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

# Erstellen eines Tab-Widgets
notebook = ttk.Notebook(root)

# Konfigurieren aller Tab-Widgets
notebook.pack(fill="both", expand=True)

# Tab "WB communication"
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="WB communication")

# Tab "Charge Parameter"
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Charge Parameter")

# Tab "Charge Manager"
tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="Charge Manager")


# Gewichtung der Spalten und Zeilen im Tab1-Widget
tab1.grid_rowconfigure(0, weight=1)
tab1.grid_columnconfigure(0, weight=1)
tab1.grid_columnconfigure(1, weight=1)

# Gewichtung der Spalten und Zeilen im Tab2-Widget
tab2.grid_rowconfigure(0, weight=1)
#tab2.grid_columnconfigure(0, weight=1)


# Gewichtung der Spalten und Zeilen im Tab3-Widget
tab3.grid_rowconfigure(0, weight=1)
tab3.grid_columnconfigure(0, weight=1)
tab3.grid_columnconfigure(1, weight=1)



# Erstellen des Frames für den LINKEN Bereich "Controllable Load"
left_frame = ttk.LabelFrame(tab3, text="Controllable Load")
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

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


# Erstellen eines Frames für den MITTLEREN Bereich "Charge Parameter"
middle_frame = ttk.LabelFrame(tab2, text="Charge Parameter")
middle_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
#middle_frame.columnconfigure(0, weight=1)

# Erstellen eines weiteren Frames ohne Überschrift innerhalb des Frames "Charge Parameter"
no_header_middle_frame = ttk.LabelFrame(middle_frame, text="")
no_header_middle_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
#no_header_middle_frame.columnconfigure(0, weight=1)

# Erstellen eines weiteren Frames "Power Control EuT-Side" innerhalb des Frames "Charge Parameter"
power_control_frame = ttk.LabelFrame(middle_frame, text="Power Control EuT-Side")
power_control_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
#power_control_frame.columnconfigure(0, weight=1)

# Erstellen eines weiteren Frames "Current Control EuT-Side" innerhalb des Frames "Charge Parameter"
current_control_frame = ttk.LabelFrame(middle_frame, text="Current Control EuT-Side")
current_control_frame.grid(row=9, column=0, padx=10, pady=10, sticky="nsew")
#current_control_frame.columnconfigure(0, weight=1)

# Erstellen eines Frames für den RECHTEN Bereich "Charge Process"
right_frame = ttk.LabelFrame(tab3, text="Charge Process")
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



# Erstellen des Dropdown-Menüs für "Power [static]" im MITTLEREN Frame
power_static_var = tk.StringVar()
power_static_button = ttk.Button(power_control_frame, text="Power [static]", command=enable_power_static)
power_static_button.config(state="disabled")
power_static_combo = ttk.Combobox(power_control_frame, textvariable=power_static_var, values=["3.7 kW", "7.4 kW", "11 kW"], state="readonly")
power_static_combo.config(state="disabled")

# Positionieren des Labels und des Dropdown-Menüs "Power [static]" im MITTLEREN Frame
power_static_button.grid(row=3, column=0, padx=5, pady=5)
power_static_combo.grid(row=3, column=1, padx=5, pady=5)

# Verknüpfung der Dropdown-Auswahl der Power [static] an die entsprechende Funktion im MITTLEREN Frame
power_static_combo.bind("<<ComboboxSelected>>", power_static_combo_selected) # --> Funktion wird nur zur Anzeige der Betätigung des Dropdown-Menüs im Terminal verwendet


# Erstellen des Dropdown-Menüs für "Power [automatic]" im MITTLEREN Frame
power_automatic_var = tk.StringVar()
power_automatic_button = ttk.Button(power_control_frame, text="Power [automatic]", command=enable_power_automatic)
power_automatic_button.config(state="disabled")
power_automatic_combo = ttk.Combobox(power_control_frame, textvariable=power_automatic_var, values=[".csv-File", ".xlsx-File"], state="readonly")
power_automatic_combo.config(state="disabled")

# Positionieren des Labels und des Dropdown-Menüs "Power [automatic]" im MITTLEREN Frame
power_automatic_button.grid(row=4, column=0, padx=5, pady=5)
power_automatic_combo.grid(row=4, column=1, padx=5, pady=5)

# Verknüpfung der Dropdown-Auswahl der Power [automatic] an die entsprechende Funktion im MITTLEREN Frame
power_automatic_combo.bind("<<ComboboxSelected>>", power_automatic_combo_selected) # --> Funktion wird nur zur Anzeige der Betätigung des Dropdown-Menüs im Terminal verwendet


# Erstellen des Dropdown-Menüs für "Current [static]" im MITTLEREN Frame
current_static_var = tk.StringVar()
current_static_button = ttk.Button(current_control_frame, text="Current [static]", command=enable_current_static)
current_static_button.config(state="disabled")
current_static_combo = ttk.Combobox(current_control_frame, textvariable=current_static_var, values=["6 A", "8 A", "10 A", "13 A", "16 A"], state="readonly")
current_static_combo.config(state="disabled")

# Positionieren des Labels und des Dropdown-Menüs "Current [static]" im MITTLEREN Frame
current_static_button.grid(row=10, column=0, padx=5, pady=5)
current_static_combo.grid(row=10, column=1, padx=5, pady=5)

# Verknüpfung der Dropdown-Auswahl der Current [static] an die entsprechende Funktion im MITTLEREN Frame
current_static_combo.bind("<<ComboboxSelected>>", current_static_combo_selected) # --> Funktion wird nur zur Anzeige der Betätigung des Dropdown-Menüs im Terminal verwendet


# Erstellen des Dropdown-Menüs für "Current [automatic]" im MITTLEREN Frame
current_automatic_var = tk.StringVar()
current_automatic_button = ttk.Button(current_control_frame, text="Current [automatic]", command=enable_current_automatic)
current_automatic_button.config(state="disabled")
current_automatic_combo = ttk.Combobox(current_control_frame, textvariable=current_automatic_var, values=[".csv-File", ".xlsx-File"], state="readonly")
current_automatic_combo.config(state="disabled")

# Positionieren des Labels und des Dropdown-Menüs "Power [automatic]" im MITTLEREN Frame
current_automatic_button.grid(row=11, column=0, padx=5, pady=5)
current_automatic_combo.grid(row=11, column=1, padx=5, pady=5)

# Verknüpfung der Dropdown-Auswahl der Power [automatic] an die entsprechende Funktion im MITTLEREN Frame
current_automatic_combo.bind("<<ComboboxSelected>>", current_automatic_combo_selected) # --> Funktion wird nur zur Anzeige der Betätigung des Dropdown-Menüs im Terminal verwendet


# Erstellen des Dropdown-Menüs für "Control Operation" im MITTLEREN Frame
control_operation_var = tk.StringVar()
control_operation_label = ttk.Label(no_header_middle_frame, text="Control Operation:")
control_operation_combo = ttk.Combobox(no_header_middle_frame, textvariable=control_operation_var, values=["Laden", "Entladen"], state="readonly")
update_button_and_combo_states()

# Verknüpfung der Dropdown-Auswahl der Control Operation an die entsprechende Funktion im MITTLEREN Frame
control_operation_combo.bind("<<ComboboxSelected>>", control_operation_selected)  # Durch bind-Methode wird Fkt "control_operation_selected(event)" jedes Mal bei Benutzung des Dropdown-Menüs aufgerufen (-->EVENT!!!)


# Positionieren des Labels und des Dropdown-Menüs "Control Operation" im MITTLEREN Frame
control_operation_label.grid(row=1, column=0, padx=8, pady=5)
control_operation_combo.grid(row=1, column=1, padx=5, pady=5)



# Starten der GUI
root.mainloop()