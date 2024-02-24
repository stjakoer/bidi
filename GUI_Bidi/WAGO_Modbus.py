from pyModbusTCP.client import ModbusClient

client = ModbusClient(host="192.168.178.202", port=502)
regs = None

if client.open():
    regs = client.read_input_registers(0, 1)
    print(regs)
else:
    print("Keine Verbindung zur Wago")

if client.write_multiple_registers(1, [1]):
    print("Erfolgreich")
else:
    print("Fehler")

