import time
import can
import cantools
cms_read_dict = {}

EVMaxCurrent = 25
EVMaxVoltage = 450
EVMaxPower = 450*50

canBus = can.interface.Bus(bustype="pcan", channel="PCAN_USBBUS1", bitrate="500000")
database_dbc = cantools.db.load_file("ISC_CMS_Automotive.dbc")
can_tester = cantools.tester.Tester('CMS', database_dbc, canBus, 'ISC_CMS_Automotive')


def cms_canbus_listener():
    global cms_read_dict
    cms_read_dict = {
        #"Linkstatus": None,
        #"ErrorCodeLevel3": None,
        #"ErrorCodeLevel2": None,
        #"ErrorCodeLevel1": None,
        #"ErrorCodeLevel0": None,
        #"EVSEEnergyTransferType": None,
        #"AliveCounter": None,   #
        "VoltageMatch": None,   #
        "ControlPilotState": None,  #
        "ControlPilotDutyCycle": None,  #
        "TCPStatus": None,
        #"ActualChargeProtocol": None,   #
        "ProximityPinState": None,  #
        "StateMachineState": None,  #
        #"EVSENotificationMaxDelay": None,
        #"EVSENotification": None,
        #"EVSEStatusCode": None,
        #"EVSEPowerLimitAchieved": None,
        #"EVSEVoltageLimitAchieved": None,
        #"EVSECurrentLimitAchieved": None,
        "EVSEIsolationStatus": None,
        "EVSEPresentVoltage": None,
        #"EVSECurrentRegulationTolerance": None,
        #"EVSEPeakCurrentRipple": None,
        "EVSEMinVoltage": None,
        "EVSEMaxCurrent": None
    }
    start_time = time.time()
    while time.time() - start_time < 0.15:
        raw_message = canBus.recv()
        if raw_message is not None:
            coded_message = database_dbc.get_message_by_frame_id(raw_message.arbitration_id)
            decoded_botschaft = coded_message.decode(raw_message.data)

            for keys_dict in cms_read_dict.keys():
                for key_bot in decoded_botschaft.keys():
                    if keys_dict == key_bot:
                        cms_read_dict[keys_dict] = decoded_botschaft[key_bot]


def cms_read_dict_handover():
    global cms_read_dict
    cms_canbus_listener()
    return cms_read_dict


def receive_and_decode_signal(signal_name):
    cms_canbus_listener()
    global cms_read_dict
    return cms_read_dict.get(signal_name)

def start_charging_cms(evcurrent, evvoltage, evsoc):

    can_tester.start()
    can_tester.messages['EVStatusControl']['BCBControl'] = 'Stop'
    can_tester.messages['EVStatusControl']['ChargeProgressIndication'] = 'Stop'
    can_tester.messages['EVStatusControl']['ChargeProtocolPriority'] = 'DIN_only'
    can_tester.messages['EVStatusControl']['ChargeStopIndication'] = 'NoStop'
    can_tester.messages['EVStatusControl']['EVReady'] = 'False'
    can_tester.messages['EVStatusControl']['EVWeldingDetectionEnable'] = 'False'

    can_tester.messages['EVPlugStatus']['EVACReqStateC'] = 'SNA'
    can_tester.messages['EVPlugStatus']['EVProximityPinState'] = 'SNA'
    can_tester.messages['EVPlugStatus']['EVControlPilotState'] = 'SNA'
    can_tester.messages['EVPlugStatus']['EVControlPilotDutyCycle'] = 'SNA'

    can_tester.flush_input()
    assert can_tester.expect('ChargeInfo', timeout=5) is not None, "CME dead?"
    assert can_tester.expect('ChargeInfo', {'StateMachineState': 'Default'},
                             timeout=3) is not None, "CME not unplugged?"

    print('Please plug in...')

    can_tester.flush_input()
    assert can_tester.expect('ChargeInfo', {'ControlPilotState': 'B'}), "Didn't detect plug-in within 10s"
    print('Pilot State B detected')
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    can_tester.flush_input()
    assert can_tester.expect('ChargeInfo', {'StateMachineState': 'Init'}), "No HLC?"
    print('Charge Init')
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    can_tester.flush_input()
    assert can_tester.expect('ChargeInfo', {'StateMachineState': 'Authentication'})
    print('Authentication')
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    can_tester.messages['EVDCMaxLimits']['EVMaxCurrent'] = EVMaxCurrent
    can_tester.messages['EVDCMaxLimits']['EVMaxVoltage'] = EVMaxVoltage
    can_tester.messages['EVDCMaxLimits']['EVMaxPower'] = EVMaxPower

    can_tester.flush_input()
    assert can_tester.expect('ChargeInfo', {'StateMachineState': 'Parameter'})
    print('Parameter')
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    can_tester.messages['EVStatusDisplay']['EVErrorCode'] = 0
    can_tester.messages['EVStatusDisplay']['EVSoC'] = evsoc
    can_tester.messages['EVStatusControl']['EVReady'] = 'True'

    can_tester.flush_input()
    assert can_tester.expect('ChargeInfo', {'StateMachineState': 'Isolation'}, timeout=20)
    print('Isolation')
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    can_tester.messages['EVDCChargeTargets']['EVPreChargeVoltage'] = evvoltage+5
    can_tester.messages['EVDCChargeTargets']['EVTargetVoltage'] = evvoltage
    can_tester.messages['EVDCChargeTargets']['EVTargetCurrent'] = evcurrent

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    can_tester.flush_input()
    assert can_tester.expect('ChargeInfo', {'StateMachineState': 'PreCharge'}, timeout=10)
    print('PreCharge')
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    cnt = 0
    matched = False
    can_tester.flush_input()
    while not matched:
        charge_info = can_tester.expect('ChargeInfo')
        if 'VoltageMatch' in charge_info and charge_info['VoltageMatch'] == 'True':
            matched = True
        charge_targets = can_tester.expect('EVSEDCStatus')
        current = charge_targets['EVSEPresentCurrent']
        voltage = charge_targets['EVSEPresentVoltage']
        if voltage == 'SNA':
            voltage = 0.0
        if current == 'SNA':
            current = 0.0
        print("%10d sec Voltage: %f, Current: %f" % (cnt, voltage, current))
        time.sleep(0.1)
        cnt += 1
        can_tester.flush_input()

    can_tester.messages['EVStatusControl']['ChargeProgressIndication'] = 'Start'

    can_tester.flush_input()
    assert can_tester.expect('ChargeInfo', {'StateMachineState': 'Charge'}, timeout=3)
    print('Charge')
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    can_tester.stop()

def stop_charging_cms():
    can_tester.start()
    can_tester.messages['EVStatusControl']['ChargeProgressIndication'] = 'Stop'

    can_tester.messages['EVDCChargeTargets']['EVTargetVoltage'] = 0
    can_tester.messages['EVDCChargeTargets']['EVTargetCurrent'] = 0

    can_tester.flush_input()
    assert can_tester.expect('ChargeInfo', {'StateMachineState': 'ShutOff'})
    print('ShutOff')
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    print('Waiting for Unplug')
    can_tester.flush_input()
    assert can_tester.expect('ChargeInfo', {'ControlPilotState': 'E'})
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    can_tester.stop()


def main():
    start_charging_cms(10, 350, 23)
    time.sleep(20)
    stop_charging_cms()


if __name__ == "__main__":
    main()
