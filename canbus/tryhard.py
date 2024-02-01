import can
import cantools

# Laden Sie die DBC-Datei
db = cantools.db.load_file('ISC_CMS_Automotive.dbc')

# Erstellen Sie eine CAN-Nachricht
message_data = [0x02, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]  # Ersetzen Sie dies durch Ihre tatsächlichen Daten
message_id = 0x1400  # Ersetzen Sie dies durch Ihre tatsächliche ID 2147491842
message = can.Message(arbitration_id=message_id, data=message_data, is_extended_id=False)

# Finden Sie die entsprechende CAN-Nachricht in der DBC-Datei
can_message = db.get_message_by_frame_id(message.arbitration_id)

# Dekodieren Sie die CAN-Nachricht
decoded_data = can_message.decode(message.data)

print(decoded_data)
