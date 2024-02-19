
import can.logger
import cantools
import sys
import traceback
import time

EVMaxCurrent = 50
EVMaxVoltage = 450
EVMaxPower = 450*50

EVPreChargeVoltage = 405
EVTargetVoltage = 400
EVTargetCurrent = 10

EVSoC = 50

CHARGE_DURATION = 5  # seconds

def cms_charge_loop(can_tester):
    import can.logger
    import cantools
    import sys
    import traceback
    import time

    EVMaxCurrent = 50
    EVMaxVoltage = 450
    EVMaxPower = 450 * 50

    EVPreChargeVoltage = 405
    EVTargetVoltage = 400
    EVTargetCurrent = 10

    EVSoC = 78

    CHARGE_DURATION = 5  # seconds

    def cms_charge_loop(can_tester):
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
        assert can_tester.expect('ChargeInfo', timeout=3) is not None, "CME dead?"
        assert can_tester.expect('ChargeInfo', {'StateMachineState': 'Default'},
                                 timeout=3) is not None, "CME not unplugged?"

        print('Please plug in...')

        can_tester.flush_input()
        assert can_tester.expect('ChargeInfo', {'ControlPilotState': 'B'}), "Didn't detect plug-in within 10s"
        print('Pilot State B detected')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        can_tester.flush_input()
        assert can_tester.expect('ChargeInfo', {'StateMachineState': 'Init'}, timeout=10), "No HLC?"
        print('Charge Init')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        can_tester.flush_input()
        assert can_tester.expect('ChargeInfo', {'StateMachineState': 'Authentication'}, timeout=10)
        print('Authentication')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        can_tester.messages['EVDCMaxLimits']['EVMaxCurrent'] = EVMaxCurrent
        can_tester.messages['EVDCMaxLimits']['EVMaxVoltage'] = EVMaxVoltage
        can_tester.messages['EVDCMaxLimits']['EVMaxPower'] = EVMaxPower

        can_tester.flush_input()
        assert can_tester.expect('ChargeInfo', {'StateMachineState': 'Parameter'}, timeout=10)
        print('Parameter')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        can_tester.messages['EVStatusDisplay']['EVErrorCode'] = 0
        can_tester.messages['EVStatusDisplay']['EVSoC'] = EVSoC
        can_tester.messages['EVStatusControl']['EVReady'] = 'True'

        can_tester.flush_input()
        assert can_tester.expect('ChargeInfo', {'StateMachineState': 'Isolation'}, timeout=20)
        print('Isolation')
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        can_tester.messages['EVDCChargeTargets']['EVPreChargeVoltage'] = EVPreChargeVoltage
        can_tester.messages['EVDCChargeTargets']['EVTargetVoltage'] = EVTargetVoltage
        can_tester.messages['EVDCChargeTargets']['EVTargetCurrent'] = EVTargetCurrent

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

        time.sleep(CHARGE_DURATION)

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

    def cms_charging(can_tester):

        # Endless loop for continuous testing
        while True:
            can_tester.start()

            try:
                cms_charge_loop(can_tester)
            except AssertionError:
                _, _, tb = sys.exc_info()
                # traceback.print_tb(tb)  # Fixed format
                tb_info = traceback.extract_tb(tb)
                filename, line, func, text = tb_info[-1]

                print('An error occurred on line {} in statement {}'.format(line, text))
                print('Restart charge cycle at the beginning.\nWaiting for Unplug...')
                can_tester.flush_input()
                assert can_tester.expect('ChargeInfo', {'ControlPilotState': 'E'})

            can_tester.stop()

    '''-------------------------------------------------------------------------------------------------
    MAIN
    -------------------------------------------------------------------------------------------------'''
    if __name__ == "__main__":
        database_dbc = cantools.db.load_file("ISC_CMS_Automotive.dbc")
        canBus = can.interface.Bus(bustype="pcan", channel="PCAN_USBBUS1", bitrate="500000")
        tester = cantools.tester.Tester('CMS', database_dbc, canBus, 'ISC_CMS_Automotive')

        cms_charging(tester)


def cms_charging(can_tester):

    # Endless loop for continuous testing
    while True:
        can_tester.start()

        try:
            cms_charge_loop(can_tester)
        except AssertionError:
            _, _, tb = sys.exc_info()
            # traceback.print_tb(tb)  # Fixed format
            tb_info = traceback.extract_tb(tb)
            filename, line, func, text = tb_info[-1]

            print('An error occurred on line {} in statement {}'.format(line, text))
            print('Restart charge cycle at the beginning.\nWaiting for Unplug...')
            can_tester.flush_input()
            assert can_tester.expect('ChargeInfo', {'ControlPilotState': 'E'})

        can_tester.stop()


'''-------------------------------------------------------------------------------------------------
MAIN
-------------------------------------------------------------------------------------------------'''
if __name__ == "__main__":
    database_dbc = cantools.db.load_file("ISC_CMS_Automotive.dbc")
    canBus = can.interface.Bus(bustype="pcan", channel="PCAN_USBBUS1", bitrate="500000")
    tester = cantools.tester.Tester('CMS', database_dbc, canBus, 'ISC_CMS_Automotive')

    cms_charging(tester)
