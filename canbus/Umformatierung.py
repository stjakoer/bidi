import struct

# Der Stromwert, den Sie setzen möchten
current = 10  # Ampere

# Umwandeln des Stromwerts in das Format für den CAN-Bus
current_can = int(current / 0.1)

# Umwandeln des CAN-Werts in ein Byte-Array
current_bytes = struct.pack('<H', current_can)

# Ausgabe des Byte-Arrays als hexadezimale Zeichenkette
current_hex = ''.join(f'{b:02x}' for b in current_bytes)

print(current_hex)
