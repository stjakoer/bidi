from GUI_Bidi.EVTEC_Modbus import evtec_modbus

evtec = evtec_modbus()

# dictionary = {
#     'schalter1': {'Wert': 20, 'Bedeutung': 'parallel'},
#     'schalter2': {'Wert': 2, 'Bedeutung': 'inter'},
# }

#print(dictionary.items())
print(evtec.items())

value_1 = evtec[0]['value']
print(value_1)


