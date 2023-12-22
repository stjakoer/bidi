# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 15:37:44 2023

@author: add-picture branch
"""

import tkinter as tk
from tkinter import ttk
from pyModbusTCP.client import ModbusClient
import struct
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib import dates as mdates



# Verbindung zum Modbus-Server herstellen
client = ModbusClient(host='192.168.2.149', port=502)
client.open()


# Starten der GUI
root.mainloop()






