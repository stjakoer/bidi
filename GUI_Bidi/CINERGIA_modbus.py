def cinergia_modbus():
    from pyModbusTCP.client import ModbusClient
    import struct

    cinergia = {}
    client = ModbusClient(host="192.168.2.149", port=502)
    register_addresses = [(13000, 2, 'Alarm_ABR_1', 'int'),
                          (13002, 2, 'Alarm_ABR_2', 'int'),
                          (13004, 2, 'Alarm_ABR_3', 'int'),
                          (13006, 2, 'Alarm_ABR_4', 'int'),
                          (16000, 2, 'SW_GrafecetState', 'int'),
                          (16006, 2, 'SW_AC_DC_Selector_U', 'int'),
                          (16012, 2, 'SW_GE_EL_Selector', 'int'),
                          (16014, 2, 'SW_OutputConnection', 'int'),
                          (16018, 2, 'SW_Bipolar', 'int'),
                          (16020, 2, 'SW_BranchControl', 'int'),
                          (16022, 2, 'SW_ControlOperationU', 'int'),
                          (26094, 2, 'Voltage_Output_U_RMS', 'float'),
                          (26106, 2, 'Current_Output_Global', 'float'),
                          (26120, 2, 'Power_Active_Output_Total', 'float')]

    for address, length, name, typ in register_addresses:
        regs = client.read_holding_registers(address, length)
        value = regs
        if regs:
            if length == 1:
                value = regs[0]
                print(f"{address:}: {value}")
            elif length == 2:
                if typ == 'float':
                    value = struct.unpack('>f', struct.pack('>HH', *regs))[0]
                elif typ == 'int':
                    value = (regs[0] << 8) | regs[1]
                print(f"{address}-{address + 1}: {value}")
            elif length == 4:
                value = struct.unpack('>d', struct.pack('>HHHH', *regs))[0]
        else:
            print(f"Fehler beim Lesen des Registers {address}")
        cinergia[address] = {'name': name, 'value': value}

    def description(cinergia_new):
        # register16000
        var_temp = cinergia_new[16000]['value']
        if var_temp == 2:
            cinergia_new[16000]['def'] = "Standby"
        elif var_temp == 3:
            cinergia_new[16000]['def'] = "PreCharge"
        elif var_temp == 4:
            cinergia_new[16000]['def'] = "Ready"
        elif var_temp == 5:
            cinergia_new[16000]['def'] = "Run"
        elif var_temp == 6:
            cinergia_new[16000]['def'] = "Warning"
        elif var_temp == 7:
            cinergia_new[16000]['def'] = "Alarm"

        # register16006
        var_temp = cinergia_new[16006]['value']
        if var_temp == 0:
            cinergia_new[16006]['def'] = "DC"
        elif var_temp == 1:
            cinergia_new[16006]['def'] = "AC"

        # register16012
        var_temp = cinergia_new[16012]['value']
        if var_temp == 0:
            cinergia_new[16012]['def'] = "EL"
        elif var_temp == 1:
            cinergia_new[16012]['def'] = "GE"

        # register16014
        var_temp = cinergia_new[16014]['value']
        if var_temp == 0:
            cinergia_new[16014]['def'] = "Independent 3 Channel"
        elif var_temp == 1:
            cinergia_new[16014]['def'] = "Parallel 1 Channel"

        # register16018
        var_temp = cinergia_new[16018]['value']
        if var_temp == 0:
            cinergia_new[16018]['def'] = "Unipolar"
        elif var_temp == 1:
            cinergia_new[16018]['def'] = "Bipolar"

        return cinergia_new

    print(description(cinergia))

cinergia_modbus()


def schreiben(register, value)
    dkfaslfödk

    return



schreiben(1703, 0)