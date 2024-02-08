def evtec_modbus():
    from pyModbusTCP.client import ModbusClient
    import struct

    def description(evtec_new):
        # register 0
        var_temp = evtec_new[0]['value']
        if var_temp == 0:
            evtec_new[0]['def'] = "Unavailable"
        elif var_temp == 1:
            evtec_new[0]['def'] = "Available"
        elif var_temp == 2:
            evtec_new[0]['def'] = "Occupied"
        elif var_temp == 3:
            evtec_new[0]['def'] = "Preparing"
        elif var_temp == 4:
            evtec_new[0]['def'] = "Charging"
        elif var_temp == 5:
            evtec_new[0]['def'] = "Finishing"
        elif var_temp == 6:
            evtec_new[0]['def'] = "Suspended EV"
        elif var_temp == 7:
            evtec_new[0]['def'] = "Suspended EVSE"
        elif var_temp == 8:
            evtec_new[0]['def'] = "Not ready"
        elif var_temp == 9:
            evtec_new[0]['def'] = "Faulted"
        else:
            evtec_new[0]['def'] = "Couldnt do def!"

        # register 1
        var_temp = evtec_new[1]['value']
        if var_temp == 0:
            evtec_new[1]['def'] = "Charging process not started (no vehicle connected)"
        elif var_temp == 1:
            evtec_new[1]['def'] = "Connected, waiting for release (by RFID or Local)"
        elif var_temp == 2:
            evtec_new[1]['def'] = "Charging process starts"
        elif var_temp == 3:
            evtec_new[1]['def'] = "Shop"
        elif var_temp == 4:
            evtec_new[1]['def'] = "Suspended (loading paused)"
        elif var_temp == 5:
            evtec_new[1]['def'] = "Charging process successfully completed (vehicle still plugged in)"
        elif var_temp == 6:
            evtec_new[1]['def'] = "Charging process completed by user (vehicle still plugged in)"
        elif var_temp == 7:
            evtec_new[1]['def'] = "Charging ended with error (vehicle still connected)"
        else:
            evtec_new[1]['def'] = "Couldnt do def!"

        # register 3
        evtec_new[3]['def'] = "Actual Output Voltage (DC)"
        # register 5
        evtec_new[5]['def'] = "Actual Output Power (Unsigned)"
        # register 7
        evtec_new[7]['def'] = "Actual Output Current (DC)"
        # register 9
        evtec_new[9]['def'] = "Actual OUtput Power"
        # register 12
        var_temp = evtec_new[12]['value']
        if var_temp == 0:
            evtec_new[12]['def'] = "AC"
        elif var_temp == 1:
            evtec_new[12]['def'] = "CCS"
        elif var_temp == 2:
            evtec_new[12]['def'] = "CHAdeMO"
        elif var_temp == 3:
            evtec_new[12]['def'] = "GBT"
        else:
            evtec_new[12]['def'] = "Couldnt do def!"

        return evtec_new

    evtec = {}
    client = ModbusClient(host="192.168.178.201", port=5020, unit_id=2)
    register_addresses = [(0, 1, 'State'),
                          (1, 1, 'ChargeState'),
                          (2, 1, 'SessionType'),
                          (3, 2, 'Voltage'),
                          (5, 2, 'PowerUInt'),
                          (7, 2, 'Current'),
                          (9, 2, 'Power'),
                          (11, 1, 'SOC'),
                          (12, 1, 'ConnectorType'),
                          (17, 2, 'ChargeTime'),
                          (19, 2, 'ChargedEnergy'),
                          # (21, 2, 'DischargedEnergy'),
                          (55, 4, 'Error'),
                          (59, 2, 'TotalBatteryCapacity'),
                          (61, 2, 'RemainingBatteryCapacity'),
                          (63, 2, 'MinimalBatteryCapacity'),
                          (65, 2, 'BulkChargeCapacity'),
                          # (120, 12, 'EVCC ID')
                          ]  # (register,länge,name)

    if client.open():
        for address, length, name in register_addresses:
            regs = client.read_holding_registers(address, length)
            value = regs
            if regs:
                if length == 1:
                    value = regs[0]
                elif length == 2:
                    value = struct.unpack('>f', struct.pack('>HH', *regs))[0]
                elif length == 4:
                    value = struct.unpack('>d', struct.pack('>HHHH', *regs))[0]
                elif length == 12:
                    value = [struct.unpack('>f', struct.pack('>HH', regs[i], regs[i + 1]))[0] for i in range(0, 12, 2)]
            else:
                print(f"EVTEC: Fehler beim Lesen des Registers {address}")
            evtec[address] = {'name': name, 'value': value}

        client.close()

        evtec = description(evtec)
    else:
        print("Verbindung zur EVTEC konnte nicht hergestellt werden!")

    return evtec

evtec_modbus = evtec_modbus()
