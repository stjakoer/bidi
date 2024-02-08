def cms_read():
    cms_read_dict = {
        "Linkstatus": None,
        "ErrorCodeLevel3": None,
        "ErrorCodeLevel2": None,
        "ErrorCodeLevel1": None,
        "ErrorCodeLevel0": None,
        "EVSEEnergyTransferType": None,
        "AliveCounter": None,
        "VoltageMatch": None,
        "ControlPilotState": None,
        "ControlPilotDutyCiycle": None,
        "TCPStatus": None,
        "ActualChargeProtocol": None,
        "ProximityPinState": None,
        "StateMachineState": None,
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
    return cms_read_dict

cms_write_dict = {
    "EVEnergyRequest": None,
    "EVEnergyCapacity": None,
    "EVWeldingDetectionEnable": None,
    "EVReady": None,
    "ChargeStopIndication": None,
    "ChargeProgressIndication": None,
    "EVSoC": None,
    "EVPreChargeVoltage": None,
    "EVTargetVoltage": None,
    "EVTargetCurrent": None,
    "EVMaxVoltage": None,
    "EVMaxCurrent": None
}

def cms_write (name, value):
