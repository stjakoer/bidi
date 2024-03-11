from pyModbusTCP.client import ModbusClient

# Modbus TCP Client (TCP immer geöffnet)
c = ModbusClient(host="192.168.2.210", port=502, unit_id=1, auto_open=True)



#
if c.write_single_register(1, 0):
    print("Schreiben erfolgreich")
else:
    print("Schreibfehler")

# 16-Bit-Register an Modbus-Adresse 4 lesen
regs = c.read_holding_registers(4, 1)
if regs:
    print(regs)
else:
    print("Lesefehler")