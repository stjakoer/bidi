import pymodbus
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

# IP-Adresse der Wallbox
ip_address = "192.168.178.201"

# Modbus-Slave-ID
slave_id = 1

# Modbus-Registeradressen
register_addresses = [
    100, 101, 102, 103, 110, 130, 200, 201, 202, 203
]

# Modbus-Registerlängen
register_lengths = [
    1, 1, 1, 4, 20, 20, 1, 1, 1, 1
]

# Modbus-Client erstellen
client = ModbusTcpClient(ip_address)

try:
    # Verbindung zum Modbus-Gerät herstellen
    client.connect()

    # Modbus-Register auslesen
    registers = []
    for i in range(len(register_addresses)):
        result = client.read_input_registers(register_addresses[i], register_lengths[i], unit=slave_id)
        if result.isError():
            print(f"Fehler beim Lesen von Modbus-Register {register_addresses[i]}: {result}")
        else:
            registers.append(result.registers)

    # Ergebnisse verarbeiten
    decoder = BinaryPayloadDecoder.fromRegisters(registers[4], byteorder=Endian.Big, wordorder=Endian.Little)
    charger_serial = decoder.decode_string(20)
    decoder = BinaryPayloadDecoder.fromRegisters(registers[5], byteorder=Endian.Big, wordorder=Endian.Little)
    charger_model = decoder.decode_string(20)

    # Ausgelesene Daten ausgeben
    print("ChargerState:", registers[0][0])
    print("ChargerVersion:", registers[1][0])
    print("ChargerNofConnectors:", registers[2][0])
    print("ChargerError:", registers[3][0])
    print("ChargerSerial:", charger_serial)
    print("ChargerModel:", charger_model)
    print("ChargeControl:", registers[6][0])
    print("ComTimeoutEnbled:", registers[7][0])
    print("ComTimeoutValue:", registers[8][0])
    print("FallbackPower:", registers[9][0])

finally:
    # Verbindung zum Modbus-Gerät trennen
    client.close()
