import can
import cantools
import time

def can_bus_reader(tester):
    # Starten Sie den Tester.
    tester.start()

    # Schreiben Sie Werte in die CAN-Attribute.
    tester.messages['EVStatusControl']['EVWeldingDetectionEnable'] = 0
    tester.send('EVStatusControl')

    # Endlosschleife, um Nachrichten vom CAN-Bus zu lesen.
    while True:
        # Empfangen Sie eine Nachricht vom CAN-Bus.
        message = canBus.recv(timeout=1.0)

        # Überprüfen Sie, ob eine Nachricht empfangen wurde.
        if message is not None:
            # Dekodieren Sie die Nachricht mit der DBC-Datei.
            decoded_message = database_dbc.decode_message(message.arbitration_id, message.data)

            # Geben Sie die dekodierte Nachricht aus.
            print(decoded_message)

        # Warten Sie eine kurze Zeit, bevor Sie die nächste Nachricht empfangen.
        time.sleep(0.1)

if __name__ == "__main__":
    # Initialisieren Sie den CAN-Bus und die DBC-Datei.
    canBus = can.interface.Bus(bustype="pcan", channel="PCAN_USBBUS1", bitrate="500000")
    database_dbc = cantools.db.load_file("../GUI_Bidi/ISC_CMS_Automotive.dbc")
    tester = cantools.tester.Tester('CMS', database_dbc, canBus, 'ISC_CMS_Automotive')

    can_bus_reader(tester)

