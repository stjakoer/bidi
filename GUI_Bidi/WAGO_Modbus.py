from pyModbusTCP.client import ModbusClient
client = ModbusClient(host="192.168.2.210", port=502)

wago_dict = {'wago_ac_security_check': {'value': None, 'reg-addr': 0}, # Abfrage ob AC-GUI Starten darf (Julian)
             'sps_command_stop_charging_ac': {'value': None, 'reg-addr': 1}, #
             'sps_command_stop_charging_dc': {'value': None, 'reg-addr': 2},
             'ccs_lock_closed': {'value': None, 'reg-addr': 3},
             'ccs_lock_open': {'value': None, 'reg-addr': 4},
             'wago_dc_security_check': {'value': None, 'reg-addr': 5}, # Abfrage ob DC-GUI Starten darf
             # hier fehlt noch:  Ob die Schütze wirklich zu sind 'dc_contactor_state': {'value': None, 'reg-addr': 6}
             }
""" 240315: JRU: Wurde entsprechend Julians Vorbereitung angepasst, es fehlt noch contactor state.
Vorher: JKO: So kann das Wago Dictionary aufgebaut werden. Ich denke, dass diese beiden Variablen aber reichen
sollten. Einmal der Status, ob alles OK ist und die GUI starten darf (0 = nicht starten, 1 = starten) 
und einmal, dass die Schütze wirklich zu sind, damit der Ladevorgang weiter voranschreiten kann"""


def wago_modbus():
    global wago_dict
    if client.open():
        j = 0
        for keys in wago_dict:
            wago_dict[keys]['value'] = client.read_input_registers(j, 1) # j = register & 1 entspricht die Breite
            j += 1
    else:
        print("Keine Verbindung zur Wago!")
    return wago_dict


wago_write_dict = {'close_contactor': 0,    # 'name': 'adresse'
                   'open_contactor': 1,
                   'turn_off_IMD': 2}


def wago_write_modbus(write_name, write_value):
    for keys in wago_write_dict:
        if keys == write_name:
            if client.write_multiple_registers(wago_write_dict[keys], [write_value]):
                # Abfrage ob schreiben erfolgreich war
                print("Erfolgreich")
            else:
                print("Fehler beim schreiben der Wago")


def main():
    wago_modbus()


if __name__ == "__main__":
    main()
