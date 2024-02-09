import time

import can
import cantools
cms_read_dict = {}
canBus = can.interface.Bus(bustype="pcan", channel="PCAN_USBBUS1", bitrate="500000")
database_dbc = cantools.db.load_file("ISC_CMS_Automotive.dbc")
tester = cantools.tester.Tester('CMS', database_dbc, canBus, 'ISC_CMS_Automotive')

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


cms_write_dict = {
    "EVEnergyRequest": {'bot': 'EVDCEnergyLimits', 'value': None},
    "EVEnergyCapacity": {'bot': 'EVDCEnergyLimits', 'value': None},
    "EVWeldingDetectionEnable": {'bot': 'EVStatusControl', 'value': None},
    "EVReady": {'bot': 'EVStatusControl', 'value': None},
    "ChargeStopIndication": {'bot': 'EVStatusControl', 'value': None},
    "ChargeProgressIndication": {'bot': 'EVStatusControl', 'value': None},
    "EVSoC": {'bot': 'EVStatusDisplay', 'value': None},
    "EVPreChargeVoltage": {'bot': 'EVDCChargeTargets', 'value': None},
    "EVTargetVoltage": {'bot': 'EVDCChargeTargets', 'value': None},
    "EVTargetCurrent": {'bot': 'EVDCChargeTargets', 'value': None},
    "EVMaxVoltage": {'bot': 'EVDCMaxLimits', 'value': None},
    "EVMaxCurrent": {'bot': 'EVDCMaxLimits', 'value': None}
}   # dictionary um jedes Signal der Botschaft zuzuordnen


def cms_write(signal, value):

    tester.messages[signal] = value
