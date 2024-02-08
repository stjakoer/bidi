import can.logger
import cantools
import sys
import traceback
import time

# Konstanten für den Ladevorgang
EVMaxCurrent = 50
EVMaxVoltage = 450
EVMaxPower = 450 * 50

EVPreChargeVoltage = 405
EVTargetVoltage = 400
EVTargetCurrent = 10

EVSoC = 50

CHARGE_DURATION = 40  # Ladedauer in Sekunden

def cms_charge_loop(can_tester):
    # Vorbereitung der CAN-Nachrichten für den Ladevorgang
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

    # Initialisierung des Ladevorgangs
    can_tester.flush_input()
    assert can_tester.expect('ChargeInfo', timeout=3) is not None, "CME dead?"
    assert can_tester.expect('ChargeInfo', {'StateMachineState': 'Default'},
                             timeout=3) is not None, "CME not unplugged?"

    print('Bitte Ladestecker einstecken....')

    can_tester.flush_input()
    assert can_tester.expect('ChargeInfo', {'ControlPilotState': 'B'}), "Didn't detect plug-in within 10s"
    print('Pilot State B detected')

    # ... Weitere Initialisierungs- und Authentifizierungsschritte ...

    # Setzen der maximalen Ladeleistung
    can_tester.messages['EVDCMaxLimits']['EVMaxCurrent'] = EVMaxCurrent
    can_tester.messages['EVDCMaxLimits']['EVMaxVoltage'] = EVMaxVoltage
    can_tester.messages['EVDCMaxLimits']['EVMaxPower'] = EVMaxPower

    # ... Weitere Schritte des Ladevorgangs ...

    # Anpassung der Status- und Steuerungsnachrichten für den Ladevorgang
    can_tester.messages['EVStatusDisplay']['EVErrorCode'] = 0
    can_tester.messages['EVStatusDisplay']['EVSoC'] = EVSoC
    can_tester.messages['EVStatusControl']['EVReady'] = 'True'

    can_tester.flush_input()
    assert can_tester.expect('ChargeInfo', {'StateMachineState': 'Isolation'}, timeout=20)
    print('Isolation')

    # Setzen der Ladeziele
    can_tester.messages['EVDCChargeTargets']['EVPreChargeVoltage'] = EVPreChargeVoltage
    can_tester.messages['EVDCChargeTargets']['EVTargetVoltage'] = EVTargetVoltage
    can_tester.messages['EVDCChargeTargets']['EVTargetCurrent'] = EVTargetCurrent

    # ... Weitere Schritte des Ladevorgangs ...

    # Warten auf Übereinstimmung von Spannung und Strom
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

    # Starten des Ladevorgangs
    can_tester.messages['EVStatusControl']['ChargeProgressIndication'] = 'Start'

    can_tester.flush_input()
    assert can_tester.expect('ChargeInfo', {'StateMachineState': 'Charge'}, timeout=3)
    print('Charge')

    # Warten während des Ladevorgangs
    time.sleep(CHARGE_DURATION)

    # Stoppen des Ladevorgangs
    can_tester.messages['EVStatusControl']['ChargeProgressIndication'] = 'Stop'

    can_tester.messages['EVDCChargeTargets']['EVTargetVoltage'] = 0
    can_tester.messages['EVDCChargeTargets']['EVTargetCurrent'] = 0

    can_tester.flush_input()
    assert can_tester.expect('ChargeInfo', {'StateMachineState': 'ShutOff'})
    print('ShutOff')

    # Warten auf das Abziehen des Steckers
    print('Waiting for Unplug')
    can_tester.flush_input()
    assert can_tester.expect('ChargeInfo', {'ControlPilotState': 'E'})
    # ... Weitere Schritte nach dem Ladevorgang ...

def cms_charging(can_tester):
    # Endlose Schleife für kontinuierliches Testen
    while True:
        can_tester.start()

        try:
            cms_charge_loop(can_tester)
        except AssertionError:
            _, _, tb = sys.exc_info()
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
    # Laden der DBC-Datei und Initialisierung des CAN-Bus
    database_dbc = cantools.db.load_file("../GUI_Bidi/ISC_CMS_Automotive.dbc")
    canBus = can.interface.Bus(bustype="pcan", channel="PCAN_USBBUS1", bitrate="500000")
    tester = cantools.tester.Tester('CMS', database_dbc, canBus, 'ISC_CMS_Automotive')

    # Starten des Ladevorgangs
    cms_charging(tester)
