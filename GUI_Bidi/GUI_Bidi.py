# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 15:37:44 2023

@author: Team-Bidi
"""

import threading
import tkinter as tk
from tkinter import ttk
import time
from connect_gpio import control_indicator_light
from connect_evtec import evtec_modbus
from connect_cinergia import cinergia_modbus, cinergia_write_modbus
from connect_wago import wago_modbus, wago_write_modbus
from connect_cms import precharge_cms, start_charging_cms, cms_read_dict_handover, stop_charging_cms, start_cms

cinergia_dict = {}  # Leeres dictionary für cinergia variablen
evtec_dict = {}     # Leeres dictionary für evtec variablen
cms_dict = {}       # Leeres dictionary für cms values
wago_dict = {}      # Leeres dictionary für wago values
CMS_current_set = 0
CNG_voltage_set = 240
current_ch = 0
current_dch = 0
selected_operation = {}
power_ok = False
update_time = 3000  # Zeit bis sich jede Funktion wiederholt
gui_state = ''  # Not Ready, Ready, Charging, Ready to Charge
all_connected = False   # Um zu speichern, ob alle Verbunden sind.



def update_dicts():
    global cinergia_dict
    global cms_dict
    global evtec_dict
    global wago_dict
    global all_connected
    while True:
        cinergia_status, cinergia_dict = cinergia_modbus()
        cms_status, cms_dict = cms_read_dict_handover()
        evtec_status, evtec_dict = evtec_modbus()
        wago_status, wago_dict = wago_modbus()
        if cinergia_status and cms_status and evtec_status and wago_status:
            all_connected = True
        else:
            all_connected = False
            #Aufruf der Charge Abbruch funktion
        time.sleep(1)

# CNG Output
# Funktion für den aktuellen Status (Grafcet) der CNG
def update_cng_buttons():
    sw_grafcet_state_label.config(text=f"{cinergia_dict[16000]['value']}")
    if cinergia_dict[16000]['value'] == 2:  # 2: Standby
        enable_button.config(state="normal")
        disable_button.config(state="disable")
        start_cng_button.config(state="disable")
        stop_cng_button.config(state="disable")
        reset_button.config(state="disable")
    elif cinergia_dict[16000]['value'] == 4:    # 4: Ready
        enable_button.config(state="disable")
        disable_button.config(state="normal")
        if power_ok and CMS_current_set != 0:
            start_cng_button.config(state="normal")
        else:
            start_cng_button.config(state="disable")
        stop_cng_button.config(state="disable")
        reset_button.config(state="disable")
    elif cinergia_dict[16000]['value'] == 5:    # 5: Run
        enable_button.config(state="disable")
        disable_button.config(state="disable")
        start_cng_button.config(state="disable")
        stop_cng_button.config(state="normal")
        reset_button.config(state="disable")
    elif cinergia_dict[16000]['value'] == 6 or cinergia_dict[16000]['value'] == 7:  # 6: Warning; 7: Alarm
        enable_button.config(state="disable")
        disable_button.config(state="normal")
        start_cng_button.config(state="disable")
        start_cng_button.config(state="disable")
        reset_button.config(state="normal")
    root.after(1000, update_cng_buttons)
    return


def update_ctrl_button():
    global gui_state
    if power_ok and CMS_current_set != 0 and cinergia_dict[16000]['value'] == 5 and gui_state == 'ready' and round(cinergia_dict[26094]['value'], 0) == CNG_voltage_set:
        start_charging_button.config(state="normal")
    else:
        start_charging_button.config(state="disable")
    root.after(1000, update_ctrl_button)



#   ==============================================================================================

def update_selectors():
    sw_ac_dc_selector_u_label.config(text=f"{cinergia_dict[16006]['value']}")
    # Entspricht vermutlich 1:1 der Drehschalter Position; 0: DC, 1: AC
    sw_ge_el_selector_label.config(text=f"{cinergia_dict[16012]['value']}")
    # Entspricht vermutlich 1:1 der Drehschalter Position; 0: EL, 1: GE; noch unklar, ob nutzbar
    sw_output_connection_label.config(text=f"{cinergia_dict[16014]['value']}")
    # Entspricht vermutlich 1:1 der Drehschalter Position; 0: independent 3 channel, 1: parallel 1 channel
    sw_bipolar_label.config(text=f"{cinergia_dict[16018]['value']}")
    # Entspricht vermutlich 1:1 der Drehschalter Position; 0: unipolar, 1: bipolar
    sw_control_operation_u_label.config(text=f"{cinergia_dict[16022]['value']}")
    # Entspricht vermutlich 1:1 der Drehschalter Position; 0: Voltage Source, 1: Current Source
    root.after(update_time, update_selectors)
    return


def update_alarm_abr():
    alarm_def_ABR[0].config(text=f"{cinergia_dict[13000]['value']}")
    alarm_def_ABR[1].config(text=f"{cinergia_dict[13002]['value']}")
    alarm_def_ABR[2].config(text=f"{cinergia_dict[13004]['value']}")
    alarm_def_ABR[3].config(text=f"{cinergia_dict[13006]['value']}")
    alarm_def_ABR[4].config(text=f"{cinergia_dict[13008]['value']}")
    root.after(update_time, update_alarm_abr)
    return


def update_alarm_inv():
    alarm_def_INV[0].config(text=f"{cinergia_dict[23000]['value']}")
    alarm_def_INV[1].config(text=f"{cinergia_dict[23002]['value']}")
    alarm_def_INV[2].config(text=f"{cinergia_dict[23004]['value']}")
    alarm_def_INV[3].config(text=f"{cinergia_dict[23006]['value']}")
    alarm_def_INV[4].config(text=f"{cinergia_dict[23008]['value']}")
    root.after(update_time, update_alarm_inv)
    return


# CNG Output
def update_cng_para():
    global cinergia_dict
    #   Spannung:
    voltage_un_label.config(text=round((cinergia_dict[26094]['value']), 1))
    #   Strom:
    if cinergia_dict[26106]['value'] is None:   # Abfrage ob None oder ob ein Wert gelesen werden konnte
        current_total_label.config(text="None")
    else:
        current_total_label.config(text="{:.3f}".format(cinergia_dict[26106]['value']))
    #   Power:
    if cinergia_dict[26120]['value'] is None: # Abfrage ob None oder ob ein Wert gelesen werden konnte
        power_total_label.config(text="None")
    else:
        power_total_label.config(text="{:.3f}".format(cinergia_dict[26120]['value']))
    root.after(update_time, update_cng_para)
    return


#   ==============================================================================================
# CNG Input
def enable_cng():
    if cinergia_dict[16000]['value'] == 2:  # 2: Standby
        cinergia_write_modbus(17000, 1, 'int')
        cinergia_write_modbus(17004, 0, 'int')  # Einstellen von u (v, w) als Voltage Source: 0
    return


def disable_cng():
    if cinergia_dict[16000]['value'] >= 4:  # 4: Ready; 5: Run; 6: Warning; 7: Alarm
        cinergia_write_modbus(17000, 0, 'int')
    return


def reset_alarm_warning():
    if cinergia_dict[16000]['value'] == 6 or cinergia_dict[16000]['value'] == 7:    # 6: Warning; 7: Alarm
        cinergia_write_modbus(17018, 0, 'int')  # Sequenz erstellen: [0, 1, 0]
        time.sleep(1)
        cinergia_write_modbus(17018, 1, 'int')
        time.sleep(1)
        cinergia_write_modbus(17018, 0, 'int')
        time.sleep(1)
    return

#   ================================================================================================
# Interne Funktion
# Dropdown:
def update_operation_combo_states(event):   # Auswahl Charge/Discharge
    global selected_operation, CMS_current_set, CNG_voltage_set, current_ch, current_dch
    selected_operation = control_operation_var.get()
    print("Die Operation-Variable lautet:", selected_operation, "; Datentyp:", type(selected_operation))
    current_ch = 0
    current_dch = 0
    current_ch_static_combo.set("0")
    current_dch_static_combo.set("0")

    # Basierend auf der Auswahl in "Control Operation" aktiviere die entsprechenden Schaltflächen
    if selected_operation == "Charge":
        current_ch_static_combo.config(state="normal")
        current_dch_static_combo.config(state="disabled")
    elif selected_operation == "Discharge":
        current_dch_static_combo.config(state="normal")
        current_ch_static_combo.config(state="disabled")

    CMS_current_set = current_ch - current_dch
    power_calculation()
    update_cng_buttons()
    return


# Anzeige, dass Dropdown-Menü betätigt wurde
def current_ch_static_combo_selected(event):
    global CMS_current_set, CNG_voltage_set, current_ch, current_dch
    current_ch = current_ch_static_var.get()
    print("Dropdown-Menü von Current [static] betätigt:", current_ch, "A", "; Datentyp:", type(current_ch))
    CMS_current_set = current_ch - current_dch
    # Anzeige der erwarteten Ladeleistung:
    power_calculation()
    return


# Anzeige, dass Dropdown-Menü betätigt wurde
def current_dch_static_combo_selected(event):
    global CMS_current_set, CNG_voltage_set, current_ch, current_dch
    current_dch = current_dch_static_var.get()
    print("Dropdown-Menü von Current [static] betätigt", current_dch, "A", "; Datentyp:", type(current_dch))
    CMS_current_set = current_ch - current_dch
    power_calculation()
    return


# Prüfung der Leistung
def power_calculation():
    global CNG_voltage_set, power_ok
    calculated_power = CNG_voltage_set * CMS_current_set
    power_calculation_label_text.config(text=f"{calculated_power}W")
    if abs(calculated_power) > 10000:
        power_calculation_status_label.config(text="Error, to high!")#
        power_ok = False
    else:
        power_calculation_status_label.config(text="Ok!")
        power_ok = True
    return


#   ==============================================================================================
def start_cng():
    global CNG_voltage_set
    if cinergia_dict[16000]['value'] == 4:  # 4: Ready
        cinergia_write_modbus(17002, 1, 'int')  # RunReady
        time.sleep(1)
    if cinergia_dict[16000]['value'] == 5:  # 5: Run:
        print("Erfolgreich gestartet.")
    cinergia_write_modbus(27666, CNG_voltage_set, 'float')  # Magnitude_Voltage_DC_Global_SP
    time.sleep(1)
    cinergia_write_modbus(17020, 1, 'int')  # Trigger_Config


def stop_cng():
    cinergia_write_modbus(17002, 0, 'int')


def start_charging():
    canbus_manage_cms_charging_thread = threading.Thread(target=manage_cms_charging, daemon=True)
    canbus_manage_cms_charging_thread.start()
    return


def manage_cms_charging():
    global wago_dict
    global all_connected
    global cms_dict
    start_cms()
    wago_write_modbus('stop_imd', 1)
    while True:
        if cms_dict['ControlPilotState'] == "B":
            time.sleep(1)
            wago_write_modbus('ccs_lock_open', 0)
            wago_write_modbus('ccs_lock_close', 1)
            break
    while True:
        if wago_dict['ccs_lock_close']['value'] == 1:
            break
    while True:
        if wago_dict['dcplus_contactor_state_open']['value'] == 1 and wago_dict['dcminus_contactor_state_open']['value'] == 1:
            break
    precharge_cms(CMS_current_set, CNG_voltage_set)  # precharge + parameter übergeben
    while True:
        if int(cms_dict["EVSEPresentVoltage"]) < (CNG_voltage_set+10) and int(cms_dict["EVSEPresentVoltage"]) > (CNG_voltage_set-10):
            break       # schauen, dass der precharge +/- 10 V von der CNG Spannung erreicht hat
        #CMS spannung abfragen und schauen ob precharge erfolgreich war
    wago_write_modbus('close_contactor', 1)   # schütze schließen
    while True:
        if wago_dict['dcplus_contactor_state_open']['value'] == 0 and wago_dict['dcminus_contactor_state_open']['value'] == 0:  # Wenn 0 = Schütz zu
            print("Schütze durch Raspberry Pi geschlossen")
            start_charging_cms()
            break


    while True:
        if wago_dict['sps_command_stop_charging_dc']['value'] == 1:    # wenn von wago der "not-aus" kommt
            control_indicator_light('rot', 'an')
            stop_charging()     # Normales beenden
            break
        if not all_connected:    # wenn cng die Verbindung verliert....? Notwendig
            control_indicator_light('rot','an')
            stop_charging()     # Normales beenden
            break
        if not cms_dict['StateMachineState'] == 'Charge':
            stop_charging()     # Normales beenden
            break
    if wago_dict['sps_command_stop_charging_dc']['value'] == 0 and all_connected:
        control_indicator_light('rot', 'aus')
# CNG Input
def stop_charging():
    stop_charging_cms()
    wago_write_modbus('close_contactor', 0)
    wago_write_modbus('stop_imd', 0)
    wago_write_modbus('ccs_lock_close', 0)
    wago_write_modbus('ccs_lock_open', 1)
    #while True:
     #   if cms_dict['StateMachineState'] == 'ShutOff' and int(cms_dict['EVSEPresentCurrent']) < 1:
      #      wago_write_modbus('close_contactor', 0)
       #     print("Schütze durch Raspberry Pi geöffnet")
        #    break
    #while True:
     #   if int(cms_dict['EVSEPresentVoltage']) <= 60 and wago_dict['dcminus_contactor_state_open']['value'] == 1 and wago_dict['dcplus_contactor_state_open']['value'] == 0:
      #      wago_write_modbus('ccs_lock_close', 0)
       #     wago_write_modbus('ccs_lock_open', 1)
        #    break
    return

### Sicherheitskriterien von RaPi abfragen ###


def start_erlaubnis():
    global gui_state
    if cinergia_dict[16006]['value'] == 0 and cinergia_dict[16014]['value'] == 1 and cinergia_dict[16018]['value'] == 0:
        # 16006: sw_ac_dc_selector_u; 16014: sw_output_connection; 16018: sw_bipolar
        if wago_dict['wago_dc_security_check']['value'] == 1:
            start_status_label.config(text='Bereit')
            control_indicator_light('grün','an')
            gui_state = 'ready'
        else:
            start_status_label.config(text='WAGO blockiert')
            control_indicator_light('grün', 'aus')
            gui_state = ''
    else:
        start_status_label.config(text='CNG blockiert')
        control_indicator_light('grün', 'aus')
        gui_state = ''
    root.after(update_time, start_erlaubnis)
    return

#================================================================================================
#GUI FRAMES
def update_evtec():
    global evtec_dict
    j = 0
    for i in evtec_dict.keys():
        evtec_name = ttk.Label(information_EVTEC_frame_3_0, text=f"{evtec_dict[i]['name']}:")
        evtec_name.grid(row=j, column=0, padx=5, pady=2)
        evtec_def = ttk.Label(information_EVTEC_frame_3_0, text="")

        existing_widget = information_EVTEC_frame_3_0.grid_slaves(row=j, column=1)
        if existing_widget:
            existing_widget[0].destroy()  # Zerstöre das vorhandene Widget
        if i in [0, 1, 12]:
            evtec_def.config(text=f"{evtec_dict[i]['value']}")
            evtec_def.grid(row=j, column=1, padx=5, pady=2)
        else:
            if isinstance(evtec_dict[i]['value'], float):
                evtec_def.config(text=f"{evtec_dict[i]['value']:.3f}")
            else:
                evtec_def.config(text=f"{evtec_dict[i]['value']}")
            evtec_def.grid(row=j, column=1, padx=5, pady=2)
        j += 1

    root.after(update_time, update_evtec)
    return


def update_cms_frame():
    global cms_dict
    j = 0
    for keys in cms_dict.keys():
        existing_widget = cms_frame.grid_slaves(row=j, column=0)
        if existing_widget:
            existing_widget[0].destroy()  # Zerstöre das vorhandene Widget
        cms_name = ttk.Label(cms_frame, text=f"{keys}:      {cms_dict[keys]}",anchor='w')
        cms_name.grid(row=j, column=0, padx=5, pady=2, sticky='w')
        j += 1
    root.after(update_time, update_cms_frame)
    return


root = tk.Tk()
root.title("EV-Emulator")
root.geometry('1260x680')
# root.iconbitmap("Logo_Bidi.ico")

update_thread = threading.Thread(target=update_dicts, daemon=True)
update_thread.start()
time.sleep(1)

notebook = ttk.Notebook(root)
tab1 = ttk.Frame(notebook)

### ERSTE SPALTE ###

# Erstellen des Frames_0_0 (1. Haupt-Frame von links) "Charge Parameter"
frame_0_0 = ttk.LabelFrame(tab1, text="Charge Parameter")
frame_0_0.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
frame_0_0.columnconfigure(0, weight=1)

# Erstellen eines Frames im Frame_0_0 für "Control Operation"
no_header_frame_0_0 = ttk.LabelFrame(frame_0_0, text="")
no_header_frame_0_0.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
# Erstellen des Dropdown-Menüs im "no_header_frame_0_0", sowie Positionierung
control_operation_var = tk.StringVar()
control_operation_label = ttk.Label(no_header_frame_0_0, text="Control Operation:")
control_operation_label.grid(row=1, column=0, padx=5, pady=5)
control_operation_combo = ttk.Combobox(no_header_frame_0_0, textvariable=control_operation_var, values=["Charge", "Discharge"], state="readonly", width=7)
control_operation_combo.grid(row=1, column=1, padx=5, pady=5)
# Verknüpfung der Dropdown-Auswahl an die zugehörige Eventfunktion
# Bind-Methode ruft die Fkt "update_operation_combo_states(event)" immer bei Benutzung des Dropdown-Menüs auf
control_operation_combo.bind("<<ComboboxSelected>>", update_operation_combo_states)
no_header_frame_0_0.columnconfigure(0, weight=1)
no_header_frame_0_0.columnconfigure(1, weight=1)

# Erstellen des Frames "Voltage Control" im Frame_0_0
voltage_control_frame = ttk.LabelFrame(frame_0_0, text="Voltage Control --> Cinergia")
voltage_control_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
# Erstellen der Spannungsausgabe im "voltage_control_frame", sowie Positionierung
voltage_static_label = ttk.Label(voltage_control_frame, text=f"Voltage fixed on {CNG_voltage_set}V.")
voltage_static_label.grid(row=3, column=0, padx=5, pady=5)
voltage_static_label.config(state="normal")

# Erstellen des Frames "Charge Current → CMS" im Frame_0_0
current_ch_control_frame = ttk.LabelFrame(frame_0_0, text="Charge Current → CMS")
current_ch_control_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
# Erstellen des Dropdown-Menüs im "current_ch_control_frame", sowie Positionierung
current_ch_static_var = tk.IntVar()  # Variable als Integer definieren
current_ch_static_label = ttk.Label(current_ch_control_frame, text="Charge Current [A]:")
current_ch_static_label.grid(row=5, column=0, padx=5, pady=5)
current_ch_static_combo = ttk.Combobox(current_ch_control_frame, textvariable=current_ch_static_var, values=["4", "8", "12", "16", "20", "24", "28"], state="readonly", width=5)
current_ch_static_combo.grid(row=5, column=1, padx=5, pady=5)
current_ch_static_combo.config(state="disabled")
# Verknüpfung der Dropdown-Auswahl an die zugehörige Eventfunktion
current_ch_static_combo.bind("<<ComboboxSelected>>", current_ch_static_combo_selected)  # --> Funktion wird nur zur Anzeige der Betätigung des Dropdown-Menüs im Terminal verwendet
# Konfigurieren der Spalten, um die Inhalte zu zentrieren
current_ch_control_frame.columnconfigure(0, weight=1)
current_ch_control_frame.columnconfigure(1, weight=1)

# Erstellen des Frames "Discharge Current → CMS" im Frame_0_0
current_dch_control_frame = ttk.LabelFrame(frame_0_0, text="Discharge Current →  CMS")
current_dch_control_frame.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")
# Erstellen des Dropdown-Menüs im "current_dch_control_frame", sowie Positionierung
current_dch_static_var = tk.IntVar()  # Variable als Integer definieren
current_dch_static_label = ttk.Label(current_dch_control_frame, text="Discharge Current [A]:")
current_dch_static_label.grid(row=7, column=0, padx=5, pady=5)
current_dch_static_combo = ttk.Combobox(current_dch_control_frame, textvariable=current_dch_static_var, values=["4", "8", "12", "16", "20", "24", "28"], state="readonly", width=5)
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
power_calculation()
#   Start-Erlaubnis
start_status_frame = ttk.Frame(frame_0_0)
start_status_frame.grid(row=10, column=0)
start_status_label = ttk.Label(start_status_frame, text='test')
start_status_label.grid(row=0, column=0, columnspan=3)
start_erlaubnis()

#   ======================================================================================================
### ZWEITE SPALTE ###

# Erstellen des Frames_1_0 (2. Haupt-Frame von links) "Controllable Load"
frame_1_0 = ttk.LabelFrame(tab1, text="Controllable Load")
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
reset_button.grid(row=2, column=0, columnspan=2, pady=5)
start_cng_button = ttk.Button(control_frame_1_0, text="Start CNG", state="disabled", command=start_cng)
start_cng_button.grid(row=3, column=0, padx=5, pady=5)
stop_cng_button = ttk.Button(control_frame_1_0, text="Stop CNG", state="normal", command=stop_cng)
stop_cng_button.grid(row=3, column=1, padx=5, pady=5)

# Erstellen eines weiteren Frames "Stats EuT-Side" im Frame_1_0
stats_display_frame = ttk.LabelFrame(frame_1_0, text="Stats Eut-Side")
stats_display_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
# Erstellen eines Labels zur Anzeige von Spannungswerts im "voltage_display_frame"
voltage_un_label_text = ttk.Label(stats_display_frame, text="Voltage U-N:")
voltage_un_label_text.grid(row=3, column=0, padx=5, pady=5)
voltage_un_label = ttk.Label(stats_display_frame, text="")
voltage_un_label.grid(row=3, column=1, padx=5, pady=5)
  # Aufruf der Funktion, Übergabe an vorherige Label-Variable (text="")
unit_label_un = ttk.Label(stats_display_frame, text="[V_rms]")
unit_label_un.grid(row=3, column=2, padx=5, pady=5)
current_total_label_text = ttk.Label(stats_display_frame, text="Current total:")
current_total_label_text.grid(row=5, column=0, padx=5, pady=5)
current_total_label = ttk.Label(stats_display_frame, text="")
current_total_label.grid(row=5, column=1, padx=5, pady=5)
# update_current_total()   Aufruf der Funktion, Übergabe an vorherige Label-Variable (text="")
unit_label_current_total = ttk.Label(stats_display_frame, text="[A_rms]")
unit_label_current_total.grid(row=5, column=2, padx=5, pady=5)
power_total_label_text = ttk.Label(stats_display_frame, text="Power total:")
power_total_label_text.grid(row=7, column=0, padx=5, pady=5)
power_total_label = ttk.Label(stats_display_frame, text="")
power_total_label.grid(row=7, column=1, padx=5, pady=5)
# update_power_total()   Aufruf der Funktion, Übergabe an vorherige Label-Variable (text="")
unit_label_power_total = ttk.Label(stats_display_frame, text="[W]")
unit_label_power_total.grid(row=7, column=2, padx=5, pady=5)
update_cng_para()

#   Funktion zum allgemeinen Erstellen des Alarmfensters
def create_alarm_frame(frame, title, row, alarm_dict):
    alarm_texts = ["Alarm 1:", "Alarm 2:", "Alarm 3:", "Alarm 4:", "Alarm 5:"]
    alarm_display_frame = ttk.LabelFrame(frame, text=title)
    alarm_display_frame.grid(row=row, column=0, padx=10, pady=5, sticky="nsew")
    for i, alarm_text in enumerate(alarm_texts, start=9):
        alarm_label_text = ttk.Label(alarm_display_frame, text=alarm_text)
        alarm_label_text.grid(row=i, column=1, padx=5, pady=2)
        alarm_label = ttk.Label(alarm_display_frame, text="")
        alarm_label.grid(row=i, column=2, padx=5, pady=2)
        alarm_dict.append(alarm_label)

#   Erstellen des Alarmfensters für ABR
alarm_def_ABR = []
create_alarm_frame(frame_1_0, "Alarm E.U.T. side [ABR]", 13, alarm_def_ABR)
update_alarm_abr()  # Aufruf der Funktion, Übergabe an vorherigen 5 Label-Variable (text="")
#   Erstellen des Alarmfensters für INV
alarm_def_INV = []
create_alarm_frame(frame_1_0, "Alarm E.U.T. side [INV]", 14, alarm_def_INV)
update_alarm_inv()

warning_frame = ttk.Label(frame_1_0, text="")
warning_frame.grid(row=15, column=0, padx=5, pady=5, sticky="nsew")
warning_vector_label_text = ttk.Label(warning_frame, text=f"Waring_Vector_INV:  {cinergia_dict[23010]['value']}")
warning_vector_label_text.grid(row=16, column=0, padx=5, pady=5)

#   ======================================================================================================
### DRITTE SPALTE ###

# Erstellen des Frames_2_0 (3. Haupt-Frame von links) "Charge Process"
frame_2_0 = ttk.LabelFrame(tab1, text="Charge Process")
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
update_ctrl_button()

# Erstellen des Frames "Information CNG" im Frame_2_0
information_CNG_frame_2_0 = ttk.LabelFrame(frame_2_0, text="Information CNG")
information_CNG_frame_2_0.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
sw_grafcet_state_label_text = ttk.Label(information_CNG_frame_2_0, text="Grafcet State:")
sw_grafcet_state_label_text.grid(row=3, column=0, padx=5, pady=5)
sw_grafcet_state_label = ttk.Label(information_CNG_frame_2_0, text="")
sw_grafcet_state_label.grid(row=3, column=1, padx=5, pady=5)
update_cng_buttons()  # Aufruf der Funktion, Übergabe an vorherige Label-Variable (text="")
sw_output_connection_label_text = ttk.Label(information_CNG_frame_2_0, text="Output Connection State:")
sw_output_connection_label_text.grid(row=4, column=0, padx=5, pady=5, sticky='W')
sw_output_connection_label = ttk.Label(information_CNG_frame_2_0, text="")
sw_output_connection_label.grid(row=4, column=1, padx=5, pady=5)

sw_bipolar_label_text = ttk.Label(information_CNG_frame_2_0, text="Bipolar State:")
sw_bipolar_label_text.grid(row=5, column=0, padx=5, pady=5, sticky='W')
sw_bipolar_label = ttk.Label(information_CNG_frame_2_0, text="")
sw_bipolar_label.grid(row=5, column=1, padx=5, pady=5)

sw_ge_el_selector_label_text = ttk.Label(information_CNG_frame_2_0, text="GE_EL_Selector:")
sw_ge_el_selector_label_text.grid(row=6, column=0, padx=5, pady=5, sticky='W')
sw_ge_el_selector_label = ttk.Label(information_CNG_frame_2_0, text="")
sw_ge_el_selector_label.grid(row=6, column=1, padx=5, pady=5)

sw_ac_dc_selector_u_label_text = ttk.Label(information_CNG_frame_2_0, text="AC_DC_Selector_U:")
sw_ac_dc_selector_u_label_text.grid(row=7, column=0, padx=5, pady=5, sticky='W')
sw_ac_dc_selector_u_label = ttk.Label(information_CNG_frame_2_0, text="")
sw_ac_dc_selector_u_label.grid(row=7, column=1, padx=5, pady=5)
  # Aufruf der Funktion, Übergabe an vorherige Label-Variable (text="")
sw_control_operation_u_label_text = ttk.Label(information_CNG_frame_2_0, text="Control_Operation_U:")
sw_control_operation_u_label_text.grid(row=8, column=0, padx=5, pady=5, sticky='W')
sw_control_operation_u_label = ttk.Label(information_CNG_frame_2_0, text="")
sw_control_operation_u_label.grid(row=8, column=1, padx=5, pady=5)
update_selectors()
# Konfigurieren der Spalten, um die Inhalte zu zentrieren
information_CNG_frame_2_0.columnconfigure(0, weight=1)
information_CNG_frame_2_0.columnconfigure(1, weight=1)

cms_frame = ttk.LabelFrame(frame_2_0, text="CMS")
cms_frame.grid(row=8, column=0, padx=5, pady=2, sticky="nsew")
cms_frame.columnconfigure(0, weight=1)
update_cms_frame()

### VIERTE SPALTE ###

# Erstellen des Frames_3_0 (4. Haupt-Frame von links) "EVSE"
frame_3_0 = ttk.LabelFrame(tab1, text="EVSE")
frame_3_0.grid(row=0, column=4, padx=5, pady=2, sticky="nsew")
frame_3_0.columnconfigure(0, weight=1)
information_EVTEC_frame_3_0 = ttk.LabelFrame(frame_3_0, text="EVTEC Parameter")
information_EVTEC_frame_3_0.grid(row=1, column=4, padx=5, pady=2, sticky="nsew")
update_evtec()

""" Erste Spalte - TAB 2 """


notebook.add(tab1, text="Startseite")
# notebook.add(tab2, text="Tab2")
notebook.pack(expand=True, fill='both')

# Starten der GUI
root.mainloop()


