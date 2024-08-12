import time

import RPi.GPIO as GPIO
import signal
import sys

# Dictionary zur Zuordnung der Farben
COLOR_PIN_MAP = {
    'rot': 5,
    'grün': 6,
}
# Dictionary zur Zuordnung von Zustand zu GPIO-Zuständen
STATE_GPIO_MAP = {
    'an': GPIO.LOW,
    'aus': GPIO.HIGH,
}


### Ansteuerung Leuchtmelder auf Frontseite EV-Emulator ###
def control_indicator_light(color, state):
    # Initialisierung der RasPi Relais zur Ansteuerung der Leuchtmelder des EV-Emulators
    GPIO.setmode(GPIO.BCM)  # Legt fest, dass die Pinnummern gemäß der Broadcom SOC-Kanalnummerierung angegeben werden
    GPIO.setwarnings(False)  # Deaktiviert Warnungen von der RPi.GPIO-Bibliothek, um den Output sauber zu halten

    GPIO.setup(COLOR_PIN_MAP[color], GPIO.OUT) # Konfiguriert den Relay-Pin als Ausgang

    # Aktuellen Zustand des Pins abfragen
    current_state = GPIO.input(COLOR_PIN_MAP[color])

    # Nur schalten, wenn der gewünschte Zustand vom aktuellen Zustand abweicht
    if current_state != STATE_GPIO_MAP[state]:
        GPIO.output(COLOR_PIN_MAP[color], STATE_GPIO_MAP[state]) # Setzt den GPIO-Zustand entsprechend des angegebenen Zustands
        print(f"Leuchtmelder {color} auf {state} gestellt.")


def main():
    control_indicator_light('rot','an')
    time.sleep(2)
    control_indicator_light('rot','aus')
    time.sleep(5)
    control_indicator_light('grün','an')
    time.sleep(2)
    control_indicator_light('grün','aus')


if __name__ == "__main__":
    main()