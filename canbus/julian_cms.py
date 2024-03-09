if canConnection:  # Abfrage ob der Bus eine Verbindung hat
    start_time = time.time()
    while time.time() - start_time < 0.15: # läuft solange, damit wirklich jede nachricht einmal gesendet wurde
        raw_message = canBus.recv()
        if raw_message is not None:
            coded_message = database_dbc.get_message_by_frame_id(raw_message.arbitration_id)
            decoded_botschaft = coded_message.decode(raw_message.data)

            for key_bot in decoded_botschaft.keys():
                if "ControlPilotDutyCycle" == key_bot:
                    duty_cycle = decoded_botschaft[key_bot]
                    break   #beendet die while schleife vorzeitig
