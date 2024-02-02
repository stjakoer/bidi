# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 15:37:44 2023

@author: Team-Bidi
"""

import tkinter as tk
from tkinter import ttk
from pyModbusTCP.client import ModbusClient
from tkinter.messagebox import showerror, showwarning, showinfo
import struct
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib import dates as mdates
from EVTEC_Modbus import evtec_modbus
from CINERGIA_Modbus import cinergia_modbus, cinergia_write_modbus

cinergia_dict = {}
evtec_dict = {}

global CMS_current_set
global CNG_voltage_set
current_ch = 0
current_dch = 0

# Verbindung zum Modbus-Server herstellen
client = ModbusClient(host='192.168.2.149', port=502)
client.open()

# schnelle Modbus-Abfrage
"""
regs = client.read_holding_registers(16006, 2)
print(regs)
regs_1 = client.read_holding_registers(16008, 2)
print(regs_1)
regs_2 = client.read_holding_registers(16010, 2)
print(regs_2)
"""

### AKTUALISIERUNG AUSGELESENE WERTE ###



def update_cinergia_dict():
    global cinergia_dict
    cinergia_dict = cinergia_modbus()
    root.after(1000, update_cinergia_dict)
    return

def update_evtec_dict():
    global evtec_dict
    evtec_dict = evtec_modbus()
    root.after(1000, update_evtec_dict)
    return



# CNG Output
# Funktion für den aktuellen Status (Grafcet) der CNG
def update_sw_grafcet_state():
    sw_grafcet_state_label.config(text=f"{cinergia_dict[16000]['def']}")
    if cinergia_dict[16000]['value'] == 2:  # 2: Standby
        enable_button.config(state="normal")
        disable_button.config(state="disable")
        start_charging_button.config(state="disable")
        stop_charging_button.config(state="disable")
        reset_button.config(state="disable")
    elif cinergia_dict[16000]['value'] == 4:    # 4: Ready
        enable_button.config(state="disable")
        disable_button.config(state="normal")
        start_charging_button.config(state="normal")
        stop_charging_button.config(state="disable")
        reset_button.config(state="disable")
    elif cinergia_dict[16000]['value'] == 5:    # 5: Run
        enable_button.config(state="disable")
        disable_button.config(state="normal")
        start_charging_button.config(state="disable")
        stop_charging_button.config(state="normal")
        reset_button.config(state="disable")
    elif cinergia_dict[16000]['value'] == 6 or cinergia_dict[16000]['value'] == 7:  # 6: Warning; 7: Alarm
        enable_button.config(state="disable")
        disable_button.config(state="normal")
        start_charging_button.config(state="disable")
        stop_charging_button.config(state="disable")
        reset_button.config(state="normal")
    # Hier wird der aktuelle Grafcet-Status periodisch abgefragt. Zyklus hier ist 1000 ms
    root.after(1000, update_sw_grafcet_state)
    return

### SICHERHEITSABFRAGEN ###


# CNG Output
def update_sw_ac_dc_selector_u():
    sw_ac_dc_selector_u_label.config(text=f"{cinergia_dict[16006]['def']}")
    # Entspricht vermutlich 1:1 der Drehschalter Position; 0: DC, 1: AC
    root.after(1000, update_sw_ac_dc_selector_u)
    return
# Für die Phasen v (16008) und w (16010) ist dies nicht mehr nötig, da sich im parallel 1 channel- und unipolar mode
# sowieso alle drei Phasen gleich verhalten (Branch_Control = Unified) Gegenprüfen???????????????????????????????????????


# CNG Output
def update_sw_ge_el_selector():
    sw_ge_el_selector_label.config(text=f"{cinergia_dict[16012]['def']}")
    # Entspricht vermutlich 1:1 der Drehschalter Position; 0: EL, 1: GE; noch unklar, ob nutzbar
    root.after(1000, update_sw_ge_el_selector)
    return


# CNG Output
def update_sw_output_connection():
    sw_output_connection_label.config(text=f"{cinergia_dict[16014]['def']}")
    # Entspricht vermutlich 1:1 der Drehschalter Position; 0: independent 3 channel, 1: parallel 1 channel
    root.after(1000, update_sw_output_connection)
    return


# CNG Output
def update_sw_bipolar():
    sw_bipolar_label.config(text=f"{cinergia_dict[16018]['def']}")
    # Entspricht vermutlich 1:1 der Drehschalter Position; 0: unipolar, 1: bipolar
    root.after(1000, update_sw_bipolar)
    return


#
#
# CNG Output
# Funktion zum Auslesen der aktuellen Spannung U-NEG (EuT-Side)
def update_voltage_un():
    global cinergia_dict
    voltage_un_label.config(text=f"{cinergia_dict[26094]['value']}")  # Anzeige auf 2 Dezimalstellen
    # if client.open():
    #     voltage_un_register = 26094
    #     voltage_bytes = client.read_holding_registers(voltage_un_register, 2)
    #     if voltage_bytes:
    #         if len(voltage_bytes) == 2:
    #             msb = voltage_bytes[0] # Wert des MSB-Registers
    #             lsb = voltage_bytes[1] # Wert des LSB-Registers
    #
    #             # Kombiniere die beiden Werte in einen 32-Bit-Wert (Big-Endian)
    #             combined_value = (msb << 16) | lsb
    #
    #             # Konvertiere den kombinierten Wert in den Datentyp float32
    #             global voltage_un # Variable die für Bedingungen in anderen Funktionen genutzt werden kann
    #             voltage_un = struct.unpack('!f', struct.pack('!I', combined_value))[0]
    #
    #             voltage_un_label.config(text="{0:.2f}".format(voltage_un)) # Anzeige auf 2 Dezimalstellen
    #         else:
    #             voltage_un_label.config(text='Fehler beim Lesen des Registers')
    #
    # else:
    #     voltage_un_label.config(text="Verbindung zum Modbus-Server fehlgeschlagen.")
    #
    # # Hier wird der aktuelle Spannungswert UN periodisch abgefragt. Zyklus hier ist 1000 ms
    root.after(1000, update_voltage_un)
    return

# CNG Output
# Funktion zum Auslesen des aktuellen Gesamt-Stroms (EuT-Side)
def update_current_total():
    global cinergia_dict
    current_total_label.config(text=f"{cinergia_dict[26106]['value']}")  # Anzeige auf 2 Dezimalstellen
    # if client.open():
    #     current_total_register = 26106
    #
    #     current_bytes = client.read_holding_registers(current_total_register, 2)
    #     if current_bytes:
    #         if len(current_bytes) == 2:
    #             msb = current_bytes[0]  # Wert des MSB-Registers
    #             lsb = current_bytes[1]  # Wert des LSB-Registers
    #
    #             # Kombiniere die beiden Werte in einen 32-Bit-Wert (Big-Endian)
    #             combined_value = (msb << 16) | lsb
    #
    #             # Konvertiere den kombinierten Wert in den Datentyp float32
    #             global current_total  # Variable die für Bedingungen in anderen Funktionen genutzt werden kann
    #             current_total = struct.unpack('!f', struct.pack('!I', combined_value))[0]
    #
    #             current_total_label.config(text="{0:.2f}".format(current_total))  # Anzeige auf 2 Dezimalstellen
    #         else:
    #             current_total_label.config(text='Fehler beim Lesen des Registers')
    #
    # else:
    #     current_total_label.config(text="Verbindung zum Modbus-Server fehlgeschlagen.")
    #
    # # Hier wird der aktuelle Stromwert periodisch abgefragt. Zyklus hier ist 1000 ms
    root.after(1000, update_current_total)
    return

# CNG Output
# Funktion zum Auslesen der aktuellen Gesamt-Leistung (EuT-Side)
def update_power_total():
    global cinergia_dict
    power_total_label.config(text=f"{cinergia_dict[26120]['value']}")   # Anzeige auf 2 Dezimalstellen
    # if client.open():
    #     power_total_register = 26120
    #
    #     power_bytes = client.read_holding_registers(power_total_register, 2)
    #     if power_bytes:
    #         if len(power_bytes) == 2:
    #             msb = power_bytes[0]  # Wert des MSB-Registers
    #             lsb = power_bytes[1]  # Wert des LSB-Registers
    #
    #             # Kombiniere die beiden Werte in einen 32-Bit-Wert (Big-Endian)
    #             combined_value = (msb << 16) | lsb
    #
    #             # Konvertiere den kombinierten Wert in den Datentyp float32
    #             global power_total  # Variable die für Bedingungen in anderen Funktionen genutzt werden kann
    #             power_total = struct.unpack('!f', struct.pack('!I', combined_value))[0]
    #
    #             power_total_label.config(
    #                 text="{0:.2f}".format(power_total))  # Anzeige auf 2 Dezimalstellen
    #         else:
    #             power_total_label.config(text='Fehler beim Lesen des Registers')
    #
    # else:
    #     power_total_label.config(text="Verbindung zum Modbus-Server fehlgeschlagen.")
    #
    # # Hier wird der aktuelle Leistungswert periodisch abgefragt. Zyklus hier ist 1000 ms
    root.after(1000, update_power_total)
    return

# CNG Input
# Funktionen für die Schaltflächen
def enable_cng():
    if cinergia_dict[16000]['value'] == 2:  # 2: Standby
        cinergia_write_modbus(17000, 1, 'int')

    # if client.open() and sw_grafcet_state == 2:
    #     enable_disable_cng_register = 17000
    #
    #     value_to_write = 1
    #     byte0 = (value_to_write >> 24) & 0xFF
    #     byte1 = (value_to_write >> 16) & 0xFF
    #     byte2 = (value_to_write >> 8) & 0xFF
    #     byte3 = value_to_write & 0xFF
    #
    #     client.write_multiple_registers(enable_disable_cng_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])
    #     print("Schaltfläche Enable_CNG betätigt")
    return

# CNG Input
def disable_cng():
    if cinergia_dict[16000]['value'] >= 4:  # 4: Ready; 5: Run; 6: Warning; 7: Alarm
        cinergia_write_modbus(17000, 0, 'int')

    # if client.open() and sw_grafcet_state >= 4:
    #     enable_disable_cng_register = 17000
    #
    #     value_to_write = 0
    #     byte0 = (value_to_write >> 24) & 0xFF
    #     byte1 = (value_to_write >> 16) & 0xFF
    #     byte2 = (value_to_write >> 8) & 0xFF
    #     byte3 = value_to_write & 0xFF
    #
    #     client.write_multiple_registers(enable_disable_cng_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])
    # print("Schaltfläche Disable_CNG betätigt")
    return

# CNG Input
def reset_alarm_warning():
    ## ---> Hier noch überlegen, ob Ladevorgang bei Status Alarm automatisch abgebrochen werden soll? Das Gleiche für Status Warning überlegen! ##
    if cinergia_dict[16000]['value'] == 6 or cinergia_dict[16000]['value'] == 7:    # 6: Warning; 7: Alarm
        cinergia_write_modbus(17018, 0, 'int')  # Sequenz erstellen: [0, 1, 0]
        time.sleep(1)
        cinergia_write_modbus(17018, 1, 'int')
        time.sleep(1)
        cinergia_write_modbus(17018, 0, 'int')
        time.sleep(1)
    # if client.open() and sw_grafcet_state == 6 or sw_grafcet_state ==7: # Status 6 = Warning, Status 7 = Alarm
    #     start_charging_button.config(state="normal")
    #
    #     reset_register = 17018
    #
    #
    #     sequence = [0, 1, 0]
    #
    #     values = [sequence[0] << 8 | sequence[1], sequence[1] << 8 | sequence[2]]
    #
    #     # Werte in das Register schreiben
    #     client.write_multiple_registers(reset_register, values)
    #
    #     print("Schaltfläche Reset betätigt")
    #     print("Sequenz [0, 1, 0] wurde erfolgreich in das Modbus-Register geschrieben.")
    #
    # else:
    #     print("Sequenz [0, 1, 0] wurde nicht in das Register geschrieben!")
    return

# Interne Funktion
### DROPDOWN-MENÜ "CONTROL OPERATION" ###
# Funktion, die INDIREKT durch Betätigung des Dropdown-Menüs "Control Operation" aufgerufen wird
def update_operation_combo_states():
    global selected_operation  # Globale Variable, die für Fkt "control_operation_selected(event)" und für Schaltfläche "Start Charging" als if-Bedingung verwendet wird
    selected_operation = control_operation_var.get()
    print("Die Operation-Variable lautet:", selected_operation, "; Datentyp:", type(selected_operation))

    # Basierend auf der Auswahl in "Control Operation" aktiviere die entsprechenden Schaltflächen
    if selected_operation == "Charge":
        current_ch_static_combo.config(state="normal")
        current_ch = 0
        current_dch = 0
        current_dch_static_combo.set("0")
        current_dch_static_combo.config(state="disabled")
        power_calculation(current_ch, current_dch, CNG_voltage_set)

    elif selected_operation == "Discharge":
        current_dch_static_combo.config(state="normal")
        current_ch = 0
        current_dch = 0
        current_ch_static_combo.set("0")
        current_ch_static_combo.config(state="disabled")
        power_calculation(current_ch, current_dch, CNG_voltage_set)

    return

# Interne Funktion
# Anzeige, dass Dropdown-Menü betätigt wurde
def current_ch_static_combo_selected(event):
    current_ch = current_ch_static_var.get()
    print("Dropdown-Menü von Current [static] betätigt:", current_ch, "A", "; Datentyp:", type(current_ch))
    CMS_current_set = current_ch - current_dch
    # Anzeige der erwarteten Ladeleistung:
    power_calculation(current_ch, current_dch, CNG_voltage_set)
    return
# Interne Funktion
# Anzeige, dass Dropdown-Menü betätigt wurde
def current_dch_static_combo_selected(event):
    current_dch = current_dch_static_var.get()
    print("Dropdown-Menü von Current [static] betätigt", current_dch, "A", "; Datentyp:", type(current_dch))
    CMS_current_set = current_ch - current_dch
    # Anzeige der erwarteten Entladeleistung:
    power_calculation(current_ch, current_dch, CNG_voltage_set)# Aufruf der Funktion, Übergabe an vorherige Label-Variable (text="")
    return
# Interne Funktion
# Prüfung der Leistung
def power_calculation(current_ch, current_dch, CNG_voltage_set):
    calculated_power = CNG_voltage_set * (current_ch + current_dch)
    power_calculation_label_text.config(text=f"{calculated_power}W")
    if calculated_power > 10000:
        power_calculation_status_label.config(text="Error, to high!")
    else:
        power_calculation_status_label.config(text="Ok!")
    return
# CNG Input
# Funktion, die DIREKT durch Betätigung des Dropdown-Menüs "Control Operation" aufgerufen wird
def control_operation_selected(event):  # event-Argument hier wichtig, damit Fkt bei jeder Betätigung des Dropdown-Menüs aufgerufen wird!
    update_operation_combo_states()  # Aufruf einer weiteren Funktion, um Aktivierung/Deaktivierung von Schaltflächen und Dropdown-Menüs je nach Dropdown-Auswahl von "Control Operation" zu steuern
    # Wird diese Funktion nicht auskommentiert, kommt es zu Fehlermeldung
    cinergia_write_modbus(17004, 0, 'int')  # Einstellen von u (v, w) als Voltage Source: 0


    # control_operation_ph_u_write_register = 17004
    #
    # value_to_write = 0 # Einstellen als Voltage Source: 0
    # byte0 = (value_to_write >> 24) & 0xFF
    # byte1 = (value_to_write >> 16) & 0xFF
    # byte2 = (value_to_write >> 8) & 0xFF
    # byte3 = value_to_write & 0xFF
    #
    # client.write_multiple_registers(control_operation_ph_u_write_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])
    #
    # mode_translation = {
    #     0: "Voltage Source",
    # }
    #
    # control_operation_ph_u_read_register = 16022
    # operation_bytes = client.read_holding_registers(control_operation_ph_u_read_register,2)  # Lesen von 2 16-Bit-Registern
    # control_operation_ph_u_read = (operation_bytes[0] << 8) | operation_bytes[1]
    #
    # print(f"Control Operation Ph U: {mode_translation.get(control_operation_ph_u_read, 'Unbekannt')}")
    #
    # control_operation_ph_v_read_register = 16024
    # operation_bytes = client.read_holding_registers(control_operation_ph_v_read_register,2)  # Lesen von 2 16-Bit-Registern
    # control_operation_ph_v_read = (operation_bytes[0] << 8) | operation_bytes[1]
    #
    # print(f"Control Operation Ph V: {mode_translation.get(control_operation_ph_v_read, 'Unbekannt')}")
    #
    # control_operation_ph_w_read_register = 16026
    # operation_bytes = client.read_holding_registers(control_operation_ph_w_read_register,2)  # Lesen von 2 16-Bit-Registern
    # control_operation_ph_w_read = (operation_bytes[0] << 8) | operation_bytes[1]
    #
    # print(f"Control Operation Ph W: {mode_translation.get(control_operation_ph_w_read, 'Unbekannt')}")
    return


# CNG Input
### FUNKTIONEN, DIE ÜBER IF-BEDINGUNGEN IN DER FKT VON DER SCHALTFLÄCHE "START CHARGING" AUFGERUFEN WIRD ###
def charge_control_voltage_static():

    # print("Aufruf Fkt charge_control_voltage_static()")
    # # Kontrolle der Richtigkeit (Phasen schalten, wenn es keine gibt?)
    # ### Zuerst alle 3 Phasen einschalten. Stromwert aus Dropdown-Auswahl fließt über jede einzelne Phase! ###
    #
    # # Phase U einschalten
    # on_off_ph_u_register = 17010
    #
    # value_to_write = 0
    # byte0 = (value_to_write >> 24) & 0xFF
    # byte1 = (value_to_write >> 16) & 0xFF
    # byte2 = (value_to_write >> 8) & 0xFF
    # byte3 = value_to_write & 0xFF
    #
    # client.write_multiple_registers(on_off_ph_u_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])
    #
    # # Phase V einschalten
    # on_off_ph_v_register = 17012
    #
    # value_to_write = 0
    # byte0 = (value_to_write >> 24) & 0xFF
    # byte1 = (value_to_write >> 16) & 0xFF
    # byte2 = (value_to_write >> 8) & 0xFF
    # byte3 = value_to_write & 0xFF
    #
    # client.write_multiple_registers(on_off_ph_v_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])
    #
    # # Phase W einschalten
    # on_off_ph_w_register = 17014
    #
    # value_to_write = 0
    # byte0 = (value_to_write >> 24) & 0xFF
    # byte1 = (value_to_write >> 16) & 0xFF
    # byte2 = (value_to_write >> 8) & 0xFF
    # byte3 = value_to_write & 0xFF
    #
    # client.write_multiple_registers(on_off_ph_w_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])
    #
    # time.sleep(1)  # Hier Wartezeit, damit CNG ausreichend Zeit hat alle Phasen einzuschalten

    cinergia_write_modbus(27666, CNG_voltage_set, 'float')
    cinergia_write_modbus(17020, 1, 'int')

    # magnitude_voltage_dc_global_sp_register = 27666
    # value_to_write = CNG_voltage_set
    # print(value_to_write)
    #
    # # Umwandeln des Gleitkommawertes in 4 Bytes im Big-Endian-Format
    # value_bytes = struct.pack('>f', value_to_write)
    #
    # # Extrahieren der Bytes in der richtigen Reihenfolge
    # byte0 = value_bytes[0]
    # byte1 = value_bytes[1]
    # byte2 = value_bytes[2]
    # byte3 = value_bytes[3]
    #
    # # Schreiben der Bytes in die Register
    # client.write_multiple_registers(magnitude_voltage_dc_global_sp_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])
    #
    #
    # # Selektierte Spannungsvorgabe senden
    # trigger_config_register = 17020
    #
    # value_to_write = 1
    #
    # byte0 = (value_to_write >> 24) & 0xFF
    # byte1 = (value_to_write >> 16) & 0xFF
    # byte2 = (value_to_write >> 8) & 0xFF
    # byte3 = value_to_write & 0xFF
    #
    # client.write_multiple_registers(trigger_config_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])
    return

# CNG Input
# Funktionen für Schaltflächen
def start_charging():
    charge_control_voltage_static()  # Aufruf Funktion
    print("Funktion charge_control_voltage_static() erfolgreich aufgerufen")
    if client.open() and cinergia_dict[16000]['value'] >= 4: # Status 4 = Ready, Status 5 = Run

        run_ready_register = 17002

        value_to_write = 1
        byte0 = (value_to_write >> 24) & 0xFF
        byte1 = (value_to_write >> 16) & 0xFF
        byte2 = (value_to_write >> 8) & 0xFF
        byte3 = value_to_write & 0xFF

        client.write_multiple_registers(run_ready_register, [byte0 << 8 | byte1, byte2 << 8 | byte3])
        print("Schaltfläche Start Charging betätigt")
        time.sleep(1)

        if cinergia_dict[16000]['value'] == 4:
            time.sleep(1)  # Hier Wartezeit, damit CNG ausreichend Zeit hat in Status "Run" zu gehen

            charge_control_voltage_static()  # Aufruf Funktion
            print("Funktion charge_control_voltage_static() erfolgreich aufgerufen")
    return

# CNG Input
def stop_charging():
    cinergia_write_modbus(17002, 0, 'int')
    return

# Sicherheitskriterien von RaPi abfragen:
# def rapi_cng_switch_test():
#     global rapi_cng_switch_status
#     if sw_output_connection == 1 and sw_bipolar == 0 and sw_ac_dc_selector_u == 0 and sw_ac_dc_selector_v == 0 and sw_ac_dc_selector_w == 0:
#         rapi_cng_switch_status = 1
#         print("RaPi_CNG_switch_status =", rapi_cng_switch_status)
#     else:
#         rapi_cng_switch_status = 0
#         print("RaPi_CNG_switch_status =", rapi_cng_switch_status)
#     return
#
# sw_output_connection = 1
# sw_bipolar = 0
# sw_ac_dc_selector_u = 0
# sw_ac_dc_selector_v = 0
# sw_ac_dc_selector_w = 0
#
# rapi_cng_switch_test()
# # Sicherheitskriterien von Wago abfragen, 1 = alles richtig, 0 = Fehler:
# wago_cng_switch_status = 1
#
# # Erstellen des GUI-Hauptfensters, wenn Sicherheitskriterien erfüllt sind.
# while rapi_cng_switch_status == 1 and wago_cng_switch_status == 1:


def update_evtec():
    global evtec_dict
    j = 0
    for i in evtec_dict.keys():
        EVTEC_name = ttk.Label(information_EVTEC_frame_3_0, text=f"{evtec_dict[i]['name']}:")
        EVTEC_name.grid(row=j, column=0, padx=5, pady=5)
        EVTEC_def = ttk.Label(information_EVTEC_frame_3_0, text="")
        if i in [0, 1, 12]:
            EVTEC_def.config(text=f"{evtec_dict[i]['def']}")
            EVTEC_def.grid(row=j, column=1, padx=5, pady=5)
        else:
            EVTEC_def.config(text=f"{evtec_dict[i]['value']}")
            EVTEC_def.grid(row=j, column=1, padx=5, pady=5)
        j += 1
    root.after(1000, update_evtec)
    return



root = tk.Tk()
root.title("EV-Emulator")
root.iconbitmap("Logo_Bidi.ico")

update_cinergia_dict()
update_evtec_dict()

print(cinergia_dict.items())

"""
#get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = screen_width
window_height = screen_height
print(screen_width)
print(screen_height)
print(window_width)
print(window_height)
# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)
root.attributes('-topmost', 1)
"""

### ERSTE SPALTE ###

# Erstellen des Frames_0_0 (1. Haupt-Frame von links) "Charge Parameter"
frame_0_0 = ttk.LabelFrame(text="Charge Parameter")
frame_0_0.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
frame_0_0.columnconfigure(0, weight=1)

# Erstellen eines Frames im Frame_0_0 für "Control Operation"
no_header_frame_0_0 = ttk.LabelFrame(frame_0_0, text="")
no_header_frame_0_0.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
# Erstellen des Dropdown-Menüs im "no_header_frame_0_0", sowie Positionierung
control_operation_var = tk.StringVar()
control_operation_label = ttk.Label(no_header_frame_0_0, text="Control Operation:")
control_operation_label.grid(row=1, column=0, padx=5, pady=5)
control_operation_combo = ttk.Combobox(no_header_frame_0_0, textvariable=control_operation_var, values=["Charge", "Discharge"], state="readonly")
control_operation_combo.grid(row=1, column=1, padx=5, pady=5)
# Verknüpfung der Dropdown-Auswahl an die zugehörige Eventfunktion
# Bind-Methode ruft die Fkt "control_operation_selected(event)" immer bei Benutzung des Dropdown-Menüs auf
control_operation_combo.bind("<<ComboboxSelected>>", control_operation_selected)
no_header_frame_0_0.columnconfigure(0, weight=1)
no_header_frame_0_0.columnconfigure(1, weight=1)

# Erstellen des Frames "Voltage Control" im Frame_0_0
voltage_control_frame = ttk.LabelFrame(frame_0_0, text="Voltage Control --> Cinergia")
voltage_control_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
# Erstellen der Spannungsausgabe im "voltage_control_frame", sowie Positionierung
CNG_voltage_set = 40  # Spannung zunächst fest auf 400V eingestellt
voltage_static_label = ttk.Label(voltage_control_frame, text=f"Voltage fixed on {CNG_voltage_set}V.")
voltage_static_label.grid(row=3, column=0, padx=5, pady=5)
voltage_static_label.config(state="normal")

# Erstellen des Frames "Charge Current → CMS" im Frame_0_0
current_ch_control_frame = ttk.LabelFrame(frame_0_0, text="Charge Current → CMS")
current_ch_control_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
# Erstellen des Dropdown-Menüs im "current_ch_control_frame", sowie Positionierung
current_ch_static_var = tk.IntVar()  # Variable als Integer definieren
current_ch_static_label = ttk.Label(current_ch_control_frame, text="Charge Current in A:")
current_ch_static_label.grid(row=5, column=0, padx=5, pady=5)
current_ch_static_combo = ttk.Combobox(current_ch_control_frame, textvariable=current_ch_static_var, values=["4", "8", "12", "16", "20", "24", "28"], state="readonly")
current_ch_static_combo.grid(row=5, column=1, padx=5, pady=5)
current_ch_static_combo.config(state="disabled")
# Verknüpfung der Dropdown-Auswahl an die zugehörige Eventfunktion
current_ch_static_combo.bind("<<ComboboxSelected>>",
current_ch_static_combo_selected)  # --> Funktion wird nur zur Anzeige der Betätigung des Dropdown-Menüs im Terminal verwendet
# Konfigurieren der Spalten, um die Inhalte zu zentrieren
current_ch_control_frame.columnconfigure(0, weight=1)
current_ch_control_frame.columnconfigure(1, weight=1)

# Erstellen des Frames "Discharge Current → CMS" im Frame_0_0
current_dch_control_frame = ttk.LabelFrame(frame_0_0, text="Discharge Current →  CMS")
current_dch_control_frame.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")
# Erstellen des Dropdown-Menüs im "current_dch_control_frame", sowie Positionierung
current_dch_static_var = tk.IntVar()  # Variable als Integer definieren
current_dch_static_label = ttk.Label(current_dch_control_frame, text="Discharge Current in A:")
current_dch_static_label.grid(row=7, column=0, padx=5, pady=5)
current_dch_static_combo = ttk.Combobox(current_dch_control_frame, textvariable=current_dch_static_var, values=["4", "8", "12", "16", "20", "24", "28"], state="readonly")
current_dch_static_combo.grid(row=7, column=1, padx=5, pady=5)
current_dch_static_combo.config(state="disabled")
# Verknüpfung der Dropdown-Auswahl an die zugehörige Eventfunktion
current_dch_static_combo.bind("<<ComboboxSelected>>", current_dch_static_combo_selected)  # --> Funktion wird nur zur Anzeige der Betätigung des Dropdown-Menüs im Terminal verwendet
# Konfigurieren der Spalten, um die Inhalte zu zentrieren
current_dch_control_frame.columnconfigure(0, weight=1)
current_dch_control_frame.columnconfigure(1, weight=1)
# Erstellen des Frames "Power Calculation" im Frame_0_0
power_calculation_frame = ttk.LabelFrame(frame_0_0, text="Power Calculation")
power_calculation_frame.grid(row=8, column=0, padx=10, pady=10, sticky="nsew")
power_calculation_label = ttk.Label(power_calculation_frame, text=f"Expected power is:")
power_calculation_label.grid(row=9, column=0, padx=5, pady=5)
power_calculation_label_text = ttk.Label(power_calculation_frame, text="")
power_calculation_label_text.grid(row=9, column=1, padx=5, pady=5)
power_calculation_status_label = ttk.Label(power_calculation_frame, text="")
power_calculation_status_label.grid(row=9, column=2, padx=5, pady=5)
power_calculation(CNG_voltage_set, current_dch, current_ch)

### ZWEITE SPALTE ###

# Erstellen des Frames_1_0 (2. Haupt-Frame von links) "Controllable Load"
frame_1_0 = ttk.LabelFrame(text="Controllable Load")
frame_1_0.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
frame_1_0.columnconfigure(1, weight=1)

# Erstellen des Frames "Control Cinergia" im Frame_1_0
control_frame_1_0 = ttk.LabelFrame(frame_1_0, text="Control Cinergia")
control_frame_1_0.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
# Erstellen der Schaltflächen "Enable CNG", "Disable CNG" und "Reset" im "control_frame_1_0", sowie Positionierung
enable_button = ttk.Button(control_frame_1_0, text="Enable CNG", command=enable_cng)
enable_button.grid(row=1, column=0, padx=5, pady=5)
disable_button = ttk.Button(control_frame_1_0, text="Disable CNG", state="disabled", command=disable_cng)
disable_button.grid(row=1, column=1, padx=5, pady=5)
reset_button = ttk.Button(control_frame_1_0, text="Reset", state="disabled", command=reset_alarm_warning)
reset_button.grid(row=1, column=2, padx=5, pady=5)

# Erstellen eines weiteren Frames "Voltage EuT-Side" im Frame_1_0
voltage_display_frame = ttk.LabelFrame(frame_1_0, text="Voltage EuT-Side")
voltage_display_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
# Erstellen eines Labels zur Anzeige von Spannungswerts im "voltage_display_frame"
voltage_un_label_text = ttk.Label(voltage_display_frame, text="Voltage U-N:")
voltage_un_label_text.grid(row=3, column=0, padx=5, pady=5)
voltage_un_label = ttk.Label(voltage_display_frame, text="")
voltage_un_label.grid(row=3, column=1, padx=5, pady=5)
update_voltage_un()  # Aufruf der Funktion, Übergabe an vorherige Label-Variable (text="")
unit_label_un = ttk.Label(voltage_display_frame, text="[V_rms]")
unit_label_un.grid(row=3, column=2, padx=5, pady=5)

# Erstellen eines Frames "Current EuT-Side" im Frame_1_0
current_display_frame = ttk.LabelFrame(frame_1_0, text="Current EuT-Side")
current_display_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
# Erstellen eines Labels zur Anzeige des Stromwerts im "current_display_frame"
current_total_label_text = ttk.Label(current_display_frame, text="Current total:")
current_total_label_text.grid(row=5, column=0, padx=5, pady=5)
current_total_label = ttk.Label(current_display_frame, text="")
current_total_label.grid(row=5, column=1, padx=5, pady=5)
update_current_total()  # Aufruf der Funktion, Übergabe an vorherige Label-Variable (text="")
unit_label_current_total = ttk.Label(current_display_frame, text="[A_rms]")
unit_label_current_total.grid(row=5, column=2, padx=5, pady=5)

# Erstellen eines Frames "Power EuT-Side" im Frame_1_0
power_display_frame = ttk.LabelFrame(frame_1_0, text="Power EuT-Side")
power_display_frame.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")
# Erstellen eines Labels zur Anzeige der Leistung im Frame "power_display_frame"
power_total_label_text = ttk.Label(power_display_frame, text="Power total:")
power_total_label_text.grid(row=7, column=1, padx=5, pady=5)
power_total_label = ttk.Label(power_display_frame, text="")
power_total_label.grid(row=7, column=2, padx=5, pady=5)
update_power_total()  # Aufruf der Funktion, Übergabe an vorherige Label-Variable (text="")
unit_label_power_total = ttk.Label(power_display_frame, text="[W]")
unit_label_power_total.grid(row=7, column=3, padx=5, pady=5)

### DRITTE SPALTE ###

# Erstellen des Frames_2_0 (3. Haupt-Frame von links) "Charge Process"
frame_2_0 = ttk.LabelFrame(text="Charge Process")
frame_2_0.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")
frame_2_0.columnconfigure(2, weight=1)

# Erstellen eines Frames im Frame_2_0
no_header_frame_2_0 = ttk.LabelFrame(frame_2_0, text="")
no_header_frame_2_0.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
# Erstellen der Schaltflächen "Start Charging", "Stop Charging"
start_charging_button = ttk.Button(no_header_frame_2_0, text="Start Charging", state="disabled", command=start_charging)
start_charging_button.grid(row=1, column=0, padx=5, pady=5)
stop_charging_button = ttk.Button(no_header_frame_2_0, text="Stop Charging", state="normal", command=stop_charging)
stop_charging_button.grid(row=1, column=1, padx=5, pady=5)
# Konfigurieren der Spalten, um die Inhalte zu zentrieren
no_header_frame_2_0.columnconfigure(0, weight=1)
no_header_frame_2_0.columnconfigure(1, weight=1)

# Erstellen des Frames "Information CNG" im Frame_2_0
information_CNG_frame_2_0 = ttk.LabelFrame(frame_2_0, text="Information CNG")
information_CNG_frame_2_0.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
sw_grafcet_state_label_text = ttk.Label(information_CNG_frame_2_0, text="Grafcet State:")
sw_grafcet_state_label_text.grid(row=3, column=0, padx=5, pady=5)
sw_grafcet_state_label = ttk.Label(information_CNG_frame_2_0, text="")
sw_grafcet_state_label.grid(row=3, column=1, padx=5, pady=5)
update_sw_grafcet_state()  # Aufruf der Funktion, Übergabe an vorherige Label-Variable (text="")
sw_output_connection_label_text = ttk.Label(information_CNG_frame_2_0, text="Output Connection State:")
sw_output_connection_label_text.grid(row=4, column=0, padx=5, pady=5)
sw_output_connection_label = ttk.Label(information_CNG_frame_2_0, text="")
sw_output_connection_label.grid(row=4, column=1, padx=5, pady=5)
update_sw_output_connection()  # Aufruf der Funktion, Übergabe an vorherige Label-Variable (text="")
sw_bipolar_label_text = ttk.Label(information_CNG_frame_2_0, text="Bipolar State:")
sw_bipolar_label_text.grid(row=5, column=0, padx=5, pady=5)
sw_bipolar_label = ttk.Label(information_CNG_frame_2_0, text="")
sw_bipolar_label.grid(row=5, column=1, padx=5, pady=5)
update_sw_bipolar()  # Aufruf der Funktion, Übergabe an vorherige Label-Variable (text="")
sw_ge_el_selector_label_text = ttk.Label(information_CNG_frame_2_0, text="GE_EL_Selector:")
sw_ge_el_selector_label_text.grid(row=6, column=0, padx=5, pady=5)
sw_ge_el_selector_label = ttk.Label(information_CNG_frame_2_0, text="")
sw_ge_el_selector_label.grid(row=6, column=1, padx=5, pady=5)
update_sw_ge_el_selector()  # Aufruf der Funktion, Übergabe an vorherige Label-Variable (text="")
sw_ac_dc_selector_u_label_text = ttk.Label(information_CNG_frame_2_0, text="AC_DC_Selector_U:")
sw_ac_dc_selector_u_label_text.grid(row=7, column=0, padx=5, pady=5)
sw_ac_dc_selector_u_label = ttk.Label(information_CNG_frame_2_0, text="")
sw_ac_dc_selector_u_label.grid(row=7, column=1, padx=5, pady=5)
update_sw_ac_dc_selector_u()  # Aufruf der Funktion, Übergabe an vorherige Label-Variable (text="")
# Konfigurieren der Spalten, um die Inhalte zu zentrieren
information_CNG_frame_2_0.columnconfigure(0, weight=1)
information_CNG_frame_2_0.columnconfigure(1, weight=1)

### VIERTE SPALTE ###

# Erstellen des Frames_3_0 (4. Haupt-Frame von links) "EVSE"
frame_3_0 = ttk.LabelFrame(text="EVSE")
frame_3_0.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")
frame_3_0.columnconfigure(0, weight=1)
information_EVTEC_frame_3_0 = ttk.LabelFrame(frame_3_0, text="EVTEC Parameter")
information_EVTEC_frame_3_0.grid(row=1, column=4, padx=10, pady=10, sticky="nsew")
update_evtec()


# Starten der GUI
root.mainloop()



# while not rapi_cng_switch_status == 1 and wago_cng_switch_status == 1:
#     print("FALSCH")
#     # create the root window
#     root = tk.Tk()
#     root.title('Warnung')
#     root.resizable(False, False)
#     root.geometry('600x300')
#
#     #
#     options = {'fill': 'both', 'padx': 10, 'pady': 10, 'ipadx': 5}
#     if rapi_cng_switch_status != 1:
#
#         ttk.Button(root, text='Raspberry Pi: Cinergia falsch eingestellt!', command=lambda:
#         showerror(title='Drehschalter der CNG falsch eingestellt',
#                   message=f"RaPi: Alle Drehschalter auf 1!")).pack(**options)
#     if wago_cng_switch_status != 1:
#         ttk.Button(root, text='WAGO: Cinergia falsch eingestellt!', command=lambda:
#         showerror(title='Drehschalter der CNG falsch eingestellt', message=f"WAGO: Noch nicht vergeben.")).pack(**options)
#     # run the app
#     root.mainloop()
