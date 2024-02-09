import time

import can
import cantools
cms_read_dict = {}

def cms_read():
    global cms_read_dict
    cms_read_dict = {
        "Linkstatus": None,
        "ErrorCodeLevel3": None,
        "ErrorCodeLevel2": None,
        "ErrorCodeLevel1": None,
        "ErrorCodeLevel0": None,
        "EVSEEnergyTransferType": None,
        "AliveCounter": None,   #
        "VoltageMatch": None,   #
        "ControlPilotState": None,  #
        "ControlPilotDutyCycle": None,  #
        "TCPStatus": None,
        "ActualChargeProtocol": None,   #
        "ProximityPinState": None,  #
        "StateMachineState": None,  #
        "EVSENotificationMaxDelay": None,
        "EVSENotification": None,
        "EVSEStatusCode": None,
        "EVSEPowerLimitAchieved": None,
        "EVSEVoltageLimitAchieved": None,
        "EVSECurrentLimitAchieved": None,
        "EVSEIsolationStatus": None,
        "EVSEPresentCurrent": None,
        "EVSEPresentVoltage": None,
        "EVSECurrentRegulationTolerance": None,
        "EVSEPeakCurrentRipple": None,
        "EVSEMinVoltage": None,
        "EVSEMaxCurrent": None
    }

    print(cms_read_dict)
    canBus = can.interface.Bus(bustype="pcan", channel="PCAN_USBBUS1", bitrate="500000")
    database_dbc = cantools.db.load_file("ISC_CMS_Automotive.dbc")
    start_time = time.time()
    while time.time() - start_time < 0.15:
        raw_message = canBus.recv()
        if raw_message is not None:
            coded_message = database_dbc.get_message_by_frame_id(raw_message.arbitration_id)
            decoded_botschaft = coded_message.decode(raw_message.data)
            print("Decoded message: ", decoded_botschaft)

            for keys_dict in cms_read_dict.keys():
                for key_bot in decoded_botschaft.keys():
                    if keys_dict == key_bot:
                        cms_read_dict[keys_dict] = decoded_botschaft[key_bot]

    canBus.shutdown()

    return cms_read_dict


# cms_write_dict = {
#     "EVEnergyRequest": None,
#     "EVEnergyCapacity": None,
#     "EVWeldingDetectionEnable": None,
#     "EVReady": None,
#     "ChargeStopIndication": None,
#     "ChargeProgressIndication": None,
#     "EVSoC": None,
#     "EVPreChargeVoltage": None,
#     "EVTargetVoltage": None,
#     "EVTargetCurrent": None,
#     "EVMaxVoltage": None,
#     "EVMaxCurrent": None
# }

def cms_write(botschaft, signal, value):
    canBus = can.interface.Bus(bustype="pcan", channel="PCAN_USBBUS1", bitrate="500000")
    database_dbc = cantools.db.load_file("ISC_CMS_Automotive.dbc")
    tester = cantools.tester.Tester('CMS', database_dbc, canBus, 'ISC_CMS_Automotive')

    tester.messages[botschaft][signal] = value

def cms_userguide():

    cms_write('EVStatusControl', 'BCBControl', 'Stop')

    print(cms_read())
    return