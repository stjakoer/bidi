from pyModbusTCP.client import ModbusClient
import struct

evtec = {}
client = ModbusClient(host="192.168.178.201", port=5020, unit_id=2)
slave_id = 2  # Fügen Sie weitere IDs hinzu, wenn Sie mehr Stecker haben
register_addresses = [(0,1,'State'),
                      (1,1,'ChargeState'),
                      (2,1,'SessionType'),
                      (3,2,'Voltage'),
                      (5,2,'PowerUInt'),
                      (7,2,'Current'),
                      (9,2,'Power'),
                      (11,1,'SOC'),
                      (12,1,'ConnectorType'),
                      (17,2,'ChargeTime'),
                      (19,2,'ChargedEnergy'),
                      (21,2,'DischargedEnergy'),
                      (55,4,'Error'),
                      (59,2,'TotalBatteryCapacity'),
                      (61,2,'RemainingBatteryCapacity'),
                      (63,2,'MinimalBatteryCapacity'),
                      (65,2,'BulkChargeCapacity'),
                      (120,12,'EVCC ID')]     # (register,länge,name)

client.open()

for address, length, name in register_addresses:
    regs = client.read_holding_registers(address, length)
    if regs:
        if length == 1:
            value = regs[0]
            print(f"{address:}: {value}")
        elif length == 2:
            value = struct.unpack('>f', struct.pack('>HH',*regs))[0]
            print(f"{address}-{address+1}: {value}")
        elif length == 4:
            value = struct.unpack('>d', struct.pack('>HHHH', *regs))[0]
        elif length == 12:
            values = [struct.unpack('>f', struct.pack('>HH', regs[i], regs[i+1]))[0] for i in range(0, 12, 2)]
    else:
        print(f"Fehler beim Lesen des Registers {address}")
    evtec[address] = {'name': name, 'value': value}

# Schließen Sie die Verbindung
client.close()

print(evtec.items())
