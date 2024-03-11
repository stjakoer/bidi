
### Hauptfunktion, um Error- und Alarm-Register von Cinergia auszulesen! ###

def cinergia_modbus():
    from pyModbusTCP.client import ModbusClient
    import struct

    ### ZUORDNUNG DER AUSGELESENEN WERTE DER REGISTER ###
    def description(cinergia_new):
        # Alarm description of all error registers [13000 - 13008] and [23000 - 23008]
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
        }
        # warning description [23010]
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
            17: "Isolation Device",
            18: "Overload Precharge",
            19: "SD Error",
            20: "Mains Lost",
            21: "Device not initialized",
            # Bits 22 to 31 are reserved (RSVD)
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
        }

        # register 13000,13002,13004,13006,13008 & 23000,23002,23004,23006,23008
        for register in [13000, 13002, 13004, 13006, 13008, 23000, 23002, 23004, 23006, 23008]:
            for key in alarm_dict.keys():
                if cinergia_new[register]['value'] == key:
                    cinergia_new[register]['def'] = alarm_dict[key]

        # register 23010 Warnung definieren
        for key in warning_dict.keys():
            if cinergia_new[23010]['value'] == key:
                cinergia_new[23010]['def'] = warning_dict[key]



        # Schalterstellung AC/DC Drehschalter
        var_temp = cinergia_new[16006]['value']
        if var_temp == 0:
            cinergia_new[16006]['def'] = "DC"
        elif var_temp == 1:
            cinergia_new[16006]['def'] = "AC"


        # Schalterstellung Phasenausgang Drehschalter
        var_temp = cinergia_new[16014]['value']
        if var_temp == 0:
            cinergia_new[16014]['def'] = "Independent"
        elif var_temp == 1:
            cinergia_new[16014]['def'] = "  Parallel "

        # Schalterstellung Uni/Bipolar Drehschalter
        var_temp = cinergia_new[16018]['value']
        if var_temp == 0:
            cinergia_new[16018]['def'] = "Unipolar"
        elif var_temp == 1:
            cinergia_new[16018]['def'] = "Bipolar"

        return cinergia_new

    ### ENDE VON FUNKTION DESCRIPTION(CINERGIA_NEW) !!! ###



    ### START DICTIONARY CINERGIA {} ###
    cinergia = {}
    client = ModbusClient(host="192.168.2.149", port=502)
        # Erläuterung:    (Register, Länge, Name, Typ)
    register_addresses = [(13000, 2, 'Alarm_ABR_1', 'int'),
                          (13002, 2, 'Alarm_ABR_2', 'int'),
                          (13004, 2, 'Alarm_ABR_3', 'int'),
                          (13006, 2, 'Alarm_ABR_4', 'int'),
                          (13008, 2, 'Alarm_ABR_5', 'int'),
                          (16006, 2, 'SW_AC_DC_Selector_U', 'int'),
                          (16014, 2, 'SW_OutputConnection', 'int'),
                          (16018, 2, 'SW_Bipolar', 'int'),
                          (23000, 2, 'Alarm_INV_1', 'int'),
                          (23002, 2, 'Alarm_INV_2', 'int'),
                          (23004, 2, 'Alarm_INV_3', 'int'),
                          (23006, 2, 'Alarm_INV_4', 'int'),
                          (23008, 2, 'Alarm_INV_5', 'int'),
                          (23010, 2, 'Waring_Vector_INV', 'int')]

    if client.open():
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
        cinergia = description(cinergia)
    else:
        print("Verbindung zur Cinergia konnte nicht hergestellt werden!")

    return cinergia

