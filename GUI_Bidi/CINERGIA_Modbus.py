def cinergia_modbus():
    from pyModbusTCP.client import ModbusClient
    import struct

    cinergia = {}
    client = ModbusClient(host="192.168.2.149", port=502)
    register_addresses = [(13000, 2, 'Alarm_ABR_1', 'int'),
                          (13002, 2, 'Alarm_ABR_2', 'int'),
                          (13004, 2, 'Alarm_ABR_3', 'int'),
                          (13006, 2, 'Alarm_ABR_4', 'int'),
                          (13008, 2, 'Alarm_ABR_5', 'int'),
                          (16000, 2, 'SW_GrafcetState', 'int'),
                          (16006, 2, 'SW_AC_DC_Selector_U', 'int'),
                          (16012, 2, 'SW_GE_EL_Selector', 'int'),
                          (16014, 2, 'SW_OutputConnection', 'int'),
                          (16018, 2, 'SW_Bipolar', 'int'),
                          (16022, 2, 'SW_ControlOperationU', 'int'),
                          (23000, 2, 'Alarm_INV_1', 'int'),
                          (23002, 2, 'Alarm_INV_2', 'int'),
                          (23004, 2, 'Alarm_INV_3', 'int'),
                          (23006, 2, 'Alarm_INV_4', 'int'),
                          (23008, 2, 'Alarm_INV_5', 'int'),
                          (23010, 2, 'Waring_Vector_INV', 'int'),
                          (26094, 2, 'Voltage_Output_U_RMS', 'float'),
                          (26106, 2, 'Current_Output_Global', 'float'),
                          (26120, 2, 'Power_Active_Output_Total', 'float')]

    client.open()

    for address, length, name, typ in register_addresses:
        regs = client.read_holding_registers(address, length)
        value = regs
        if regs:
            if typ == 'float':
                value = struct.unpack('>f', struct.pack('>HH', *regs))[0]
            elif typ == 'int':
                value = (regs[0] << 8) | regs[1]
        else:
            print(f"Fehler beim Lesen des Registers {address}")
        cinergia[address] = {'name': name, 'value': value}

    client.close()

    def description(cinergia_new):
        alarm_dict = {
            0: "No alarm",
            100: "Watchdog",
            101: "Node without HB DSP",
            102: "SPI_DSP_CRC",
            103: "Node without HB BBB",
            104: "Wrong DSP Loaded Prog",
            110: "Device not initialized",
            111: "DO Version Error",
            112: "EEPROM Blank",
            120: "INV Alarmed",
            121: "ABR Alarmed",
            130: "Node_Slave_2",
            131: "Node_Slave_3",
            132: "Node_Slave_4",
            133: "Node_Slave_5",
            134: "Node_Slave_6",
            135: "Node_Slave_7",
            136: "Node_Slave_8",
            137: "Node_Slave_9",
            138: "Node_Slave_10",
            139: "Slave Alarmed",
            140: "Wrong Paralel Maximum Config",
            141: "Paralel_Master_HB",
            142: "Paralel_Slave_HB",
            143: "Paralel_Master_Config_Sl",
            144: "Paralel_CRC_Coms",
            145: "Paralel_Slave_Out_Switch",
            146: "Paralel_Slave_wrong_mode",
            150: "Wrong_AC_DC_Config",
            151: "Wrong_1_Ch_Config",
            152: "Wrong_Unipolar_Config",
            153: "Wrong_Delta_Connection",
            154: "Running_Config_Modif",
            170: "Serial_Master_HB",
            171: "Serial_CRC_Coms",
            172: "Serial_Slave_HB",
            173: "Wrong_UnitSerial_AC",
            174: "Wrong_UnitSerial_3Ch",
            175: "Wrong_UnitSerial_Bipolar",
            176: "Serial_Slave_Out_Switch",
            201: "Drivers Ph1",
            202: "Drivers Ph2",
            203: "Drivers Ph3",
            211: "Heatsink temperature ABR",
            212: "Heatsink temperature INV",
            213: "Room Temperature",
            221: "Fast precharge",
            222: "Overload precharge",
            230: "Output Contactor U",
            231: "Output Contactor V",
            232: "Output Contactor W",
            301: "DC-Link Over Voltage",
            302: "DC-Link Under Voltage",
            310: "Overvoltage Main Grid",
            311: "Overvoltage 1",
            312: "Overvoltage 2",
            313: "Overvoltage 3",
            314: "Overvoltage Peak 1",
            315: "Overvoltage Peak 2",
            316: "Overvoltage Peak 3",
            317: "Undervoltage Main Grid",
            318: "Undervoltage 1",
            319: "Undervoltage 2",
            320: "Undervoltage 3",
            330: "Overcurrent MainGrid",
            331: "Overcurrent 1",
            332: "Overcurrent 2",
            333: "Overcurrent 3",
            334: "Overcurrent Peak 1",
            335: "Overcurrent Peak 2",
            336: "Overcurrent Peak 3",
            337: "Overcurrent Capacitor 1",
            338: "Overcurrent Capacitor 2",
            339: "Overcurrent Capacitor 3",
            340: "Overcurrent Neutral",
            350: "Overload MainGrid",
            351: "Overload 1",
            352: "Overload 2",
            353: "Overload 3",
            1001: "Emergency_Sequence",
            1010: "Mains Lost",
            1011: "Isolation Device"
        }  # alarm description/error code
        warning_dict = {
            0: "WatchDog",
            1: "Heart Bit",
            2: "Emergency_Sequence",
            3: "Drivers PhR",
            4: "Drivers PhS",
            5: "Drivers PhT",
            6: "DCLink OverVolage",
            7: "DCLink UnderVoltage",
            8: "AC OverVoltage",
            9: "AC UnderVoltage",
            10: "AC Overcurrent RMS",
            11: "AC Overcurrent Peak",
            12: "OverLoad",
            13: "Heatsink Temperature ABR",
            14: "Temperature INV",
            15: "Room Temperature",
            16: "INV Alarmed",
            17: "Isolation Device Overload",
            18: "Precharge SD Error",
            19: "Mains Lost",
            20: "Device not initialized",
            # Bits 21 to 31 are reserved (RSVD)
            21: "RSVD",
            22: "RSVD",
            23: "RSVD",
            24: "RSVD",
            25: "RSVD",
            26: "RSVD",
            27: "RSVD",
            28: "RSVD",
            29: "RSVD",
            30: "RSVD",
            31: "RSVD"
        } # warining description

        # register3000,13002,13004,13006,13006 & 23000,23002,23004,23006,23008
        for register in [13000, 13002, 13004, 13006, 13008, 23000, 23002, 23004, 23006, 23008]:
            for key in alarm_dict.keys():
                if cinergia_new[register]['value'] == key:
                    cinergia_new[register]['def'] = alarm_dict[key]

        # register 23010 Warnung definieren
        for key in warning_dict.keys():
            if cinergia_new[23010]['value'] == key:
                cinergia_new[23010]['def'] = warning_dict[key]

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
            cinergia_new[16014]['def'] = "Independent"
        elif var_temp == 1:
            cinergia_new[16014]['def'] = "  Parallel "

        # register16018
        var_temp = cinergia_new[16018]['value']
        if var_temp == 0:
            cinergia_new[16018]['def'] = "Unipolar"
        elif var_temp == 1:
            cinergia_new[16018]['def'] = "Bipolar"

        return cinergia_new

    cinergia = description(cinergia)

    return cinergia


def cinergia_write_modbus(register, value_to_write, value_type):
    from pyModbusTCP.client import ModbusClient
    import struct
    client = ModbusClient(host="192.168.2.149", port=502)

    client.open()

    if value_type == 'float':     # Abfrage nacht type, da float anders umgewandelt wird als integer
        if isinstance(value_to_write, int):
            value_to_write = float(value_to_write)
        value_bytes = struct.pack('>f', value_to_write)
        byte0 = value_bytes[0]
        byte1 = value_bytes[1]
        byte2 = value_bytes[2]
        byte3 = value_bytes[3]
    elif value_type == 'int':
        if isinstance(value_to_write, float):
            value_to_write = int(value_to_write)
        byte0 = (value_to_write >> 24) & 0xFF
        byte1 = (value_to_write >> 16) & 0xFF
        byte2 = (value_to_write >> 8) & 0xFF
        byte3 = value_to_write & 0xFF
    else:
        print('Es konnte kein Bit-shifting gemacht werden.')

    client.write_multiple_registers(register, [byte0 << 8 | byte1, byte2 << 8 | byte3])
    return
