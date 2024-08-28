from pyModbusTCP.client import ModbusClient
import struct
import time
client = ModbusClient(host="192.168.2.201", port=5020, unit_id=2)


def evtec_schreiben(input_power_value):
    client.open()
    # Aufteilen in High und Low 16-Bit-Werte
    high = (input_power_value >> 16) & 0xFFFF
    low = input_power_value & 0xFFFF

    client.write_multiple_registers(600, [high, low])
    client.close()


def evtec_lesen():
    client.open()
    regs = client.read_holding_registers(600, 2)  # 2 Register lesen
    client.close()
    value = struct.unpack('>i', struct.pack('>HH', *regs))[0]

    print(f"Wert des Registers 600: {value}")

def main():
    evtec_schreiben(1000)
    time.sleep(4)
    evtec_lesen()

if __name__ == "__main__":
    main()


