from pyModbusTCP.client import ModbusClient
client = ModbusClient(host="192.168.2.210", port=502)

wago_dict = {'wago_ac_security_check': {'value': None, 'reg-addr': 0},  # Abfrage ob AC-GUI Starten darf (Julian)
             'sps_command_stop_charging_ac': {'value': None, 'reg-addr': 1},
             'sps_command_stop_charging_dc': {'value': None, 'reg-addr': 2},
             'ccs_lock_status': {'value': None, 'reg-addr': 3},     # 1 = verriegelt ; 0 = nicht verriegelt
             'contactor_state': {'value': None, 'reg-addr': 4},     # 1 = zu ; 0 = offen
             'wago_dc_security_check': {'value': None, 'reg-addr': 5}   # Abfrage ob DC-GUI Starten darf
             }


def wago_modbus():
    global wago_dict
    if client.open():
        j = 0
        for keys in wago_dict:
            wago_dict[keys]['value'] = client.read_input_registers(j, 1) # j = register & 1 entspricht die Breite
            j += 1
        status_connection = True
    else:
        print("Keine Verbindung zur Wago!")
        status_connection = False
    return status_connection, wago_dict


wago_write_dict = {'contactor': 0,    # 'name': 'adresse'
                   'ccs_lock': 1,
                   'IMD': 2}


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
