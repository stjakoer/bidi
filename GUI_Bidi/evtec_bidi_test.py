from pyModbusTCP.client import ModbusClient


client = ModbusClient(host="192.168.2.201", port=5020, unit_id=2)

client.open()

input_power_value = 100  # Beispielwert in Watt

# Aufteilen in High und Low 16-Bit-Werte
high = (input_power_value >> 16) & 0xFFFF
low = input_power_value & 0xFFFF

client.write_multiple_registers(600, [high, low])

client.close()
