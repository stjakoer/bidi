import can
import cantools


def receive_can_messages(can_bus):
    # Lade die DBC-Datei
    database_dbc1 = cantools.db.load_file("ISC_CMS_Automotive.dbc")
    for i in range(100):

        # Empfange die nächste CAN-Nachricht
        message = can_bus.recv()
        if message is not None:
            # Dekodiere die CAN-Nachricht mit Hilfe der DBC-Datei
            decoded_message = database_dbc1.decode_message(message.arbitration_id, message.data)

            # Gib die decodierte Nachricht aus
            print(f"Received Message: {decoded_message}")


if __name__ == "__main__":
    # Initialisiere den CAN-Bus
    canBus = can.interface.Bus(bustype="pcan", channel="PCAN_USBBUS1", bitrate="500000")
    database_dbc = cantools.db.load_file("ISC_CMS_Automotive.dbc")

    # Initialisiere den Tester (falls benötigt)
    tester = cantools.tester.Tester('CMS', database_dbc, canBus, 'ISC_CMS_Automotive')

    # Gib die gewünschte Nachrichten-ID an

    #message_id = input("Bitte Message ID eingeben:")
    #print(type(message_id))

    # Rufe die Funktion für den CAN-Nachrichtenempfang auf
    receive_can_messages(canBus)

    # Schließe den CAN-Bus
    canBus.shutdown()
