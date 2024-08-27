from pyModbusTCP.client import ModbusClient

client = ModbusClient(host="192.168.2.201", port=5020, unit_id=2)

client.open()

input_power_value = 1000  # Beispielwert in Watt (negativ)

# Korrektur: Umwandeln in 32-Bit vor dem Aufteilen
if input_power_value < 0:
    input_power_value = (1 << 32) + input_power_value

# Aufteilen in High und Low 16-Bit-Werte
high = (input_power_value >> 16) & 0xFFFF
low = input_power_value & 0xFFFF

client.write_multiple_registers(600, [high, low])

registers = client.read_holding_registers(600, 2)  # 2 Register lesen

client.close()

# Überprüfen, ob das Lesen erfolgreich war
if registers:
    # Die beiden 16-Bit-Werte zu einem 32-Bit-Wert kombinieren
    high = registers[0]
    low = registers[1]
    output_power_value = (high << 16) + low

    # Korrektur: Zurück zu einer negativen Zahl, falls das Vorzeichenbit gesetzt ist
    if output_power_value >= (1 << 31):
        output_power_value -= (1 << 32)

    print(f"Wert des Registers 600: {output_power_value}")