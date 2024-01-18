import tkinter as tk
from tkinter import ttk


# Funktion, die bei Auswahl des Dropdown-Menüs aufgerufen wird
def dropdown_selected(event):
    print(dropdown_var.get())
    selected_value.set("Ausgewählt: " + dropdown_var.get())


# Hauptfenster erstellen
root = tk.Tk()

# Dropdown-Menü erstellen
selected_value = tk.StringVar()
print(type(selected_value))
options = ["Option 1", "Option 2", "Option 3"]
dropdown_var = ttk.Combobox(root, values=options)
dropdown_var.set("Wähle eine Option")
dropdown_var.bind("<<ComboboxSelected>>", dropdown_selected)
dropdown_var.pack(pady=10)

selected_label = tk.Label(root, textvariable=selected_value)
selected_label.pack(pady=10)

root.mainloop()
