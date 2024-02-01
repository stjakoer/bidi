from pyModbusTCP.client import ModbusClient

# IP-Adresse und Port des GO-E Charger
host = "192.168.178.201"
port = 5020
unit_id = 1

# Erstelle eine Modbus-Client-Verbindung
c = ModbusClient(host=host, port=port, unit_id=unit_id, auto_open=True)

regs = c.read_holding_registers(12, 1)

if regs:
    print(regs)
    print(len(regs))
    print(type(regs[0]))
else:
    print("read error")

if c.write_multiple_registers(202,[0]):
    print("write ok")
else:from pyModbusTCP.client import ModbusClient
    print("write error")

