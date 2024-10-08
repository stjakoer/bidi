from pyModbusTCP.client import ModbusClient
import time
client = ModbusClient(host="192.168.2.210", port=502)

wago_dict = {'wago_ac_security_check': {'value': None, 'reg-addr': 0},  # Abfrage ob AC-GUI Starten darf (Julian)
             'sps_command_stop_charging_ac': {'value': None, 'reg-addr': 1},
             'sps_command_stop_charging_dc': {'value': None, 'reg-addr': 2},
             'ccs_lock_close': {'value': None, 'reg-addr': 3},     # 1 = verriegelt ; 0 = nicht verriegelt
             'ccs_lock_open': {'value': None, 'reg-addr': 4},     # 1 = nicht verriegelt ; 0 = verriegelt
             'wago_dc_security_check': {'value': None, 'reg-addr': 5},   # Abfrage ob DC-GUI Starten darf
             'dcplus_contactor_state_open': {'value': None, 'reg-addr': 7},  # 0 = geschlossen; 1 = offen
             'dcminus_contactor_state_open': {'value': None, 'reg-addr': 8},  # 0 = geschlossen; 1 = offen
            }


def wago_modbus():
    global wago_dict
    if client.open():
        for key in wago_dict:
            reg_addr = wago_dict[key]['reg-addr']
            regs = client.read_input_registers(reg_addr, 1)
            value = regs
            if regs:
                wago_dict[key]['value'] = value[0]
            else:
                wago_dict[key]['value'] = None
        status_connection = True
    else:
        print("Keine Verbindung zur Wago!")
        status_connection = False
    return status_connection, wago_dict


wago_write_dict = {'close_contactor': 0,    # 'name': 'address'
                   'ccs_lock_close': 1,
                   'ccs_lock_open': 2,
                   'stop_imd': 3}


def wago_write_modbus(write_name, write_value):
    client.open()
    for keys in wago_write_dict:
        if keys == write_name:
            if not client.write_multiple_registers(wago_write_dict[keys], [write_value]):
                print("Fehler beim Schreiben der Wago")
                time.sleep(0.5)
                if not client.write_multiple_registers(wago_write_dict[keys], [write_value]):
                    print("2. Versuch Wago")
                    time.sleep(0.5)
                    if not client.write_multiple_registers(wago_write_dict[keys], [write_value]):
                        print("3. Versuch Wago")
    client.close()




def main():
    wago_modbus()


if __name__ == "__main__":
    main()
