import can
import cantools


# Lade DBC-Datei
database = cantools.database.load_file("ISC_CMS_Automotive.dbc")

# CAN-Nachricht
can_message = can.Message(arbitration_id=8193, data=[0x02, 0x03, 0x04, 0x02, 0x00, 0x00, 0x00, 0x00])


# Dekodiere
decoded_message = database.decode_message(can_message.arbitration_id, can_message.data)

# Gib Nachricht aus
print(decoded_message)
