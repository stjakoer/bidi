from pyModbusTCP.client import ModbusClient
import struct
import time
client = ModbusClient(host="192.168.2.201", port=5020, unit_id=2)


def evtec_schreiben(input_power_value,big_or_lit):
    client.open()
    # Aufteilen in High und Low 16-Bit-Werte
    high = (input_power_value >> 16) & 0xFFFF
    low = input_power_value & 0xFFFF
    if big_or_lit == 'big':
        if client.write_multiple_registers(600, [high, low]): # big endian
            print("Big Endian erfolgreich geschrieben!")
    elif big_or_lit == 'lit':
        if client.write_multiple_registers(600, [low, high]):    # little endian
            print("Little Endian erfolgreich geschrieben!")
    client.close()


def evtec_lesen():
    client.open()
    regs = client.read_holding_registers(600, 2)  # 2 Register lesen
    client.close()
    value_big = struct.unpack('>i', struct.pack('>HH', *regs))[0]
    value_little = struct.unpack('<i', struct.pack('<HH', *regs))[0]

    print(f"Big Endian: {value_big},Little Endian: {value_little}")

def main():
    evtec_schreiben(1000,'big')
    time.sleep(4)
    evtec_lesen()

if __name__ == "__main__":
    main()


