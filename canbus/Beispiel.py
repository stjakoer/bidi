# Auslesen des EVControlPilotState
import can
import cantools


def receive_can_messages(can_bus, database):
    for i in range(1000):
        message = can_bus.recv()
        if message is not None:
            decoded_message = database.decode_message(message.arbitration_id, message.data)
            if 'EVPlugStatus' in decoded_message:
                pilot_state = decoded_message['EVPlugStatus']['EVControlPilotState']# Auslesen des EVControlPilotState
             #   print(f"Aktueller Pilotenstatus: {pilot_state}")
             elif 'EVSEMacCurrent' in decoded_message:
                maxcurrent = decoded_message['EVSEMacCurrent']['']


if __name__ == "__main__":
    canBus = can.interface.Bus(bustype="pcan", channel="PCAN_USBBUS1", bitrate="500000")
    database_dbc = cantools.db.load_file("ISC_CMS_Automotive.dbc")

    tester = cantools.tester.Tester('CMS', database_dbc, canBus, 'ISC_CMS_Automotive')

    receive_can_messages(canBus, database_dbc)

    canBus.shutdown()
