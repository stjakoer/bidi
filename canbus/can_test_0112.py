import can.logger
import cantools

def receive_can_messages(tester):
    # Setze eine Endlosschleife für den Nachrichtenempfang auf
    try:
        while True:
            message = tester.recv()
            if message is not None:
                # Gib die decodierte Nachricht aus
                print(f"Received Message: {message}")

    except KeyboardInterrupt:
        # Bei Tastaturunterbrechung (Ctrl+C) beende das Programm
        pass
    finally:
        # Stoppe den Tester
        tester.stop()

if __name__ == "__main__":
    # Lade die DBC-Datei und initialisiere den Tester
    database_dbc = cantools.db.load_file("ISC_CMS_Automotive.dbc")
    canBus = can.interface.Bus(bustype="pcan", channel="PCAN_USBBUS1", bitrate="500000")
    tester = cantools.tester.Tester('CMS', database_dbc, canBus, 'ISC_CMS_Automotive')

    # Rufe die Funktion für den CAN-Nachrichtenempfang auf
    receive_can_messages(tester)
