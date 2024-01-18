from pyModbusTCP.client import ModbusClient

# IP-Adresse und Port des GO-E Charger
host = "192.168.178.22"
port = 502
unit_id = 1

# Erstelle eine Modbus-Client-Verbindung
c = ModbusClient(host=host, port=port, unit_id=unit_id, auto_open=True)

# Funktion zum Lesen eines Registers basierend auf Typ (Input oder Holding)
def read_register(register_address, register_length, register_type):
    if register_type == "input":
        return c.read_input_registers(register_address, register_length)
    elif register_type == "holding":
        return c.read_holding_registers(register_address, register_length)
    else:
        return None

# Funktion zum Lesen aller genannten Register
def read_all_registers():
    registers = {
        "CAR_STATE": (100, 1, "input"),
        "PP_CABLE": (101, 1, "input"),
        "FWV": (105, 2, "input"),
        "ERROR": (107, 1, "input"),
        "VOLT_L1": (109, 2, "input"),
        "VOLT_L2": (111, 2, "input"),
        "VOLT_L3": (113, 2, "input"),
        "AMP_L1": (115, 2, "input"),
        "AMP_L2": (117, 2, "input"),
        "AMP_L3": (119, 2, "input"),
        "POWER_TOTAL": (121, 2, "input"),
        "ENERGY_TOTAL": (129, 2, "input"),
        "ENERGY_CHARGE": (133, 2, "input"),
        "VOLT_N": (145, 2, "input"),
        "POWER_L1": (147, 2, "input"),
        "POWER_L2": (149, 2, "input"),
        "POWER_L3": (151, 2, "input"),
        "POWER_FACTOR_L1": (153, 2, "input"),
        "POWER_FACTOR_L2": (155, 2, "input"),
        "POWER_FACTOR_L3": (157, 2, "input"),
        "POWER_FACTOR_N": (159, 2, "input"),
        "ALLOW": (200, 1, "holding"),
        "ACCESS_STATE": (201, 1, "holding"),
        "ADAPTER_INPUT": (202, 1, "input"),
        "UNLOCKED_BY": (203, 1, "input"),
        "CABLE_LOCK_MODE": (204, 1, "holding"),
        "PHASES": (205, 1, "input"),
        "LED_BRIGHTNESS": (206, 1, "holding"),
        "LED_SAVE_ENERGY": (207, 1, "holding"),
        "ELECTRICITY_PRICES_HOURS": (208, 1, "holding"),
        "ELECTRICITY_PRICES_FINISHED": (209, 1, "holding"),
        "ELECTRICITY_PRICES_ZONE": (210, 1, "holding"),
        "AMPERE_MAX": (211, 1, "holding"),
        "AMPERE_L1": (212, 1, "holding"),
        "AMPERE_L2": (213, 1, "holding"),
        "AMPERE_L3": (214, 1, "holding"),
        "AMPERE_L4": (215, 1, "holding"),
        "AMPERE_L5": (216, 1, "holding"),
        "CLOUD_DISABLED": (217, 1, "holding"),
        "NORWAY_MODE": (218, 1, "holding"),
        "AMPERE_VOLATILE": (299, 1, "holding"),
        "AMPERE_EEPROM": (300, 1, "holding"),
        "MAC": (301, 3, "input"),
        "SNR": (304, 6, "input"),
        "HOSTNAME": (310, 5, "input"),
        "IP": (315, 4, "input"),
        "SUBNET": (319, 4, "input"),
        "GATEWAY": (323, 4, "input")
    }
    return registers

# Schließe die Modbus-Verbindung
c.close()
"""
# Funktion zur Interpretation der Register
def interpretiere_register(register, wert):
    if register == 100:
        if wert == 0:
            return "unbekannt, Ladestation defekt"
        elif wert == 1:
            return "Ladestation bereit, kein Fahrzeug"
        elif wert == 2:
            return "Fahrzeug lädt"
        elif wert == 3:
            return "Warte auf Fahrzeug"
        elif wert == 4:
            return "Ladung beendet, Fahrzeug noch verbunden"
        else:
            return "Unbekannter Status"
    elif register == 101:
        print(wert)
        w = wert
        if 13 <= w <= 32:
            interpretations.append(f"Typ2 Kabel Ampere Codierung: {w}")
        elif w == 0:
            interpretations.append("Kein Kabel")
        else:
            interpretations.append("Unbekannt")
    elif register == 101:
        if 13 <= wert <= 32:
            return f"Typ2 Kabel Ampere Codierung: {wert}"
        elif wert == 0:
            return "Kein Kabel"
        else:
            return "Unbekannt"
    elif register == 105 or register == 106:
        return f"FWV - Firmware Version: {wert.decode('ascii')}"
    elif register == 107:
        if wert == 1:
            return "RCCB (Fehlerstromschutzschalter)"
        elif wert == 3:
            return "PHASE (Phasenstörung)"
        elif wert == 8:
            return "NO_GROUND (Erdungserkennung)"
        elif wert == 10:
            return "INTERNAL (sonstiges)"
        else:
            return "Unbekannter Fehlercode"
    elif register == 108 or register == 109 or register == 110 or register == 111 or register == 112 or register == 113:
        return f"Spannung auf L{((register - 108) % 6) + 1} in Volt: {wert / 10} V"
    elif register == 114 or register == 115 or register == 116 or register == 117 or register == 118 or register == 119:
        return f"Ampere auf L{((register - 114) % 6) + 1} in A: {wert / 10} A"
    elif register == 120 or register == 121:
        return f"Leistung gesamt in kW: {wert / 100} kW"
    elif register == 128 or register == 129:
        return f"Gesamt geladene Energiemenge in kWh: {wert / 10} kWh"
    elif register == 133:
        return f"Geladene Energiemenge in kWh: {wert / 10000} kWh"
    elif register == 145:
        return f"Spannung auf N in Volt: {wert / 10} V"
    elif register == 147 or register == 149 or register == 151:
        return f"Leistung auf L{((register - 147) // 2) + 1} in kW: {wert / 100} kW"
    elif register == 153 or register == 155 or register == 157:
        return f"Leistungsfaktor auf L{((register - 153) // 2) + 1} in %: {wert / 100} %"
    elif register == 159:
        return f"Leistungsfaktor auf N in %: {wert / 100} %"
    elif register == 200:
        if wert == 0:
            return "allow_charging: PWM Signal darf anliegen (nein)"
        elif wert == 1:
            return "allow_charging: PWM Signal darf anliegen (ja)"
        else:
            return "Unbekannt"
    elif register == 201:
        if wert == 0:
            return "access_state: Zugangskontrolle (Offen)"
        elif wert == 1:
            return "access_state: Zugangskontrolle (RFID / App benötigt)"
        elif wert == 2:
            return "access_state: Zugangskontrolle (Strompreis / automatisch)"
        elif wert == 3:
            return "access_state: Zugangskontrolle (Scheduler)"
        else:
            return "Unbekannt"
    elif register == 202:
        if wert == 0:
            return "adapter_in: Ladebox ist mit Adapter angesteckt (NO_ADAPTER)"
        elif wert == 1:
            return "adapter_in: Ladebox ist mit Adapter angesteckt (16A_ADAPTER)"
        else:
            return "Unbekannt"
    elif register == 203:
        return f"Nummer der RFID Karte, die den jetzigen Ladevorgang freigeschalten hat: {wert}"
    elif register == 204:
        if wert == 0:
            return "Kabelverriegelung Einstellung (Verriegeln solange Auto angesteckt)"
        elif wert == 1:
            return "Kabelverriegelung Einstellung (Nach Ladevorgang automatisch entriegeln)"
        elif wert == 2:
            return "Kabelverriegelung Einstellung (Kabel immer verriegelt lassen)"
        else:
            return "Unbekannt"
    elif register == 205:
        if wert == 0:
            return "Phasen vor und nach dem Schütz: Keine Phase vorhanden"
        elif wert == 0b00001000:
            return "Phasen vor und nach dem Schütz: Phase 1 ist vorhanden"
        elif wert == 0b00111000:
            return "Phasen vor und nach dem Schütz: Phase 1-3 ist vorhanden"
        else:
            return "Unbekannt"
    elif register == 206:
        return f"LED Helligkeit von 0-255: {wert}"
    elif register == 207:
        if wert == 0:
            return "led_save_energy: LED automatisch nach 10 Sekunden abschalten (Energiesparfunktion deaktiviert)"
        elif wert == 1:
            return "led_save_energy: LED automatisch nach 10 Sekunden abschalten (Energiesparfunktion aktiviert)"
        else:
            return "Unbekannt"
    elif register == 208:
        return f"Minimale Anzahl von Stunden in der mit 'Strompreis - automatisch' geladen werden muss: {wert}"
    elif register == 209:
        return f"Stunde (Uhrzeit) in der mit 'Strompreis - automatisch' die Ladung mindestens aho Stunden gedauert haben muss: {wert}"
    elif register == 210:
        if wert == 0:
            return "Awattar Preiszone: Österreich"
        elif wert == 1:
            return "Awattar Preiszone: Deutschland"
        else:
            return "Unbekannt"
    elif register == 211:
        return f"Absolute max. Ampere: Maximalwert für Ampere Einstellung: {wert}"
    elif register == 212 or register == 213 or register == 214 or register == 215 or register == 216:
        return f"Ampere Level {((register - 212) % 5) + 1} für Druckknopf am Gerät: {wert if wert != 0 else 'Stufe deaktiviert (wird übersprungen)'}"
    elif register == 217:
        if wert == 0:
            return "Cloud disabled: Cloud enabled"
        elif wert == 1:
            return "Cloud disabled: Cloud disabled"
        else:
            return "Unbekannt"
    elif register == 218:
        if wert == 0:
            return "Norwegen-Modus aktiviert: deaktiviert (Erdungserkennung aktiviert)"
        elif wert == 1:
            return "Norwegen-Modus aktiviert: aktiviert (keine Erdungserkennung, nur für IT-Netze gedacht)"
        else:
            return "Unbekannt"
    elif register == 299:
        return f"Ampere Wert für die PWM Signalisierung in ganzen Ampere von 6-32A: {wert}"
    elif register == 300:
        return f"Ampere Wert für die PWM Signalisierung in ganzen Ampere von 6-32A (EEPROM): {wert}"
    elif register in range(301, 304):
        return f"MAC Adresse der WLAN Station, binär: {':'.join([f'{b:02X}' for b in wert])}"
    elif register in range(304, 310):
        return f"Seriennummer des go-eCharger, als ASCII: {wert.decode('ascii')}"
    elif register in range(310, 316):
        return f"Hostname des go-eCharger, als ASCII: {wert.decode('ascii')}"
    elif register in range(315, 319):
        return f"IP Adresse des go-eCharger, 1 Byte pro Register: {':'.join([str(wert[i]) for i in range(4)])}"
    elif register in range(319, 323):
        return f"Subnetzmaske des go-eCharger, 1 Byte pro Register: {':'.join([str(wert[i]) for i in range(4)])}"
    elif register in range(323, 327):
        return f"Gateway des go-eCharger, 1 Byte pro Register: {':'.join([str(wert[i]) for i in range(4)])}"
    else:
        return "Unbekannt"
"""
# Lese alle genannten Register aus und gebe Bezeichnung, Registernummer und Wert aus
all_registers = read_all_registers()
for register_name, (register_address, register_length, register_type) in all_registers.items():
    value = read_register(register_address, register_length, register_type)
    if value is not None:
#        interpretation = interpretiere_register(register_address, value[0])
        print("Register:", register_address, "-", register_name, ":", value, """interpretation""")
    else:
        print("Fehler beim Lesen von Register:", register_address, "-", register_name)