import can
import cantools


# Lade DBC-Datei
database = cantools.database.load_file("ISC_CMS_Automotive.dbc")

# CAN-Nachricht
can_message = can.Message(arbitration_id=8194, data=[0x31, 0x00, 0x01, 0x00, 0x02, 0x14, 0x00, 0x00])
# ID=8194x,Type=D,Length=8,Data=310001000214


# Dekodiere
decoded_message = database.decode_message(can_message.arbitration_id, can_message.data)

# Gib Nachricht aus
print(decoded_message)
