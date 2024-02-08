import can
import cantools

def can_bus_reader(bus, db):
    # Endlosschleife, um Nachrichten vom CAN-Bus zu lesen.
    while True:
        message = bus.recv()  # Empfangen Sie eine Nachricht vom CAN-Bus.
        if message is not None:
            try:
                # Finden Sie die entsprechende CAN-Nachricht in der DBC-Datei.
                can_message = db.get_message_by_frame_id(message.arbitration_id)

                # Dekodieren Sie die CAN-Nachricht.
                decoded_data = can_message.decode(message.data)

                print(f"ID: {message.arbitration_id}, Daten: {decoded_data}")
            except KeyError:
                print(f"Unbekannte Nachricht ID: {message.arbitration_id}")

if __name__ == "__main__":
    # Initialisieren Sie den CAN-Bus und die DBC-Datei.
    canBus = can.interface.Bus(bustype="pcan", channel="PCAN_USBBUS1", bitrate="500000")
    database_dbc = cantools.db.load_file("../GUI_Bidi/ISC_CMS_Automotive.dbc")

    can_bus_reader(canBus, database_dbc)
