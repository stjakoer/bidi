from pyModbusTCP.client import ModbusClient
import time

# IP-Adresse der WAGO SPS
SPS_IP = "192.168.2.210"

# Erstellen eines Modbus-Client-Objekts
client = ModbusClient(host=SPS_IP, port=502)

# Verbindung zur SPS herstellen
if client.open():
    # Schreiben des temporären Werts in das Holding Register
    if client.write_single_register(2, 1):  # Beispielwert: 42
        print("Temporärer Wert erfolgreich geschrieben.")
        # Starten des Timers für 600 ms
        time.sleep(3)  # Hier 3 Sekunden, da Pausenzeit zwischen Ein- und Ausfahren 3 Sek betragen soll!
        # Zurücksetzen auf den ursprünglichen Wert
        if client.write_single_register(2, 0):  # Beispielwert: 0 (ursprünglicher Wert)
           print("Wert erfolgreich zurückgesetzt.")
        else:
            print("Fehler beim Zurücksetzen des Werts.")
    else:
        print("Fehler beim Schreiben des temporären Werts.")
else:
    print("Verbindung zur SPS konnte nicht hergestellt werden.")

