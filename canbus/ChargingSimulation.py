#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cantools # 39.3.0 needed!
import can
import threading
import time
import tkinter as tk
from tkinter import ttk

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MAX_COLUMNS = 7

visibleMessagesList = ["ChargeInfo", "ErrorCodes", "SoftwareInfo", "SLACInfo", "EVPlugStatus", "EVStatusControl", "EVStatusDisplay"]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Signal:
    def __init__(self, parent, name, init_value, mux=-2):
        self.name = name
        self._value = init_value or 0
        # create label in label frame with given text
        self.label_text = tk.Label(parent, text=name)
        self.mux = mux

    def get_name(self):
        return self.name

    def is_mux(self):
        return self.mux == -1

    def get_mux(self):
        if self.mux >= 0:
            return self.mux
        else:
            return -1


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class RxSignal(Signal):

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent, row, name, init_value=None):
        super().__init__(parent, name, init_value)

        self.value_var = tk.StringVar(parent, value=self._value)

        # create label in lable frame with given value
        self.label_value = tk.Label(parent, textvariable=self.value_var)

        self.label_text.grid(row=row, column=0, sticky='w')
        self.label_value.grid(row=row, column=1)

    # ------------------------------------------------------------------------------------------------------------------
    def update(self, value):
        self.value_var.set(value)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TxSignal(Signal):

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent, signal):
        if signal.is_multiplexer is True:
            mux = -1
        elif signal.multiplexer_ids:
            mux = signal.multiplexer_ids[0]
        else:
            mux = -2
        super().__init__(parent, signal.name, signal.initial, mux)
        self.input = None

    # ------------------------------------------------------------------------------------------------------------------
    def set_position(self, index, max_columns):
        row = index % max_columns
        col0 = (0 + 2 * int(index / max_columns))
        col1 = (1 + 2 * int(index / max_columns))

        self.label_text.grid(row=row, column=col0)
        self.input.grid(row=row, column=col1)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TxSignalCb(TxSignal):

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent, signal, event):
        super().__init__(parent, signal)
        self.value_var = tk.BooleanVar()
        self.input = tk.Checkbutton(parent, var=self.value_var, command=event)

        # Prevent value change by scrolling with mouse wheel
        self.input.unbind_class("TCheckbutton", "<MouseWheel>")

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def value(self):
        return self.value_var.get()

    # ------------------------------------------------------------------------------------------------------------------
    @value.setter
    def value(self, new_value):
        self.value_var.set(new_value)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Tx Signal slider. By creating an TxSignal object it will generate a Slider with in the label_frame.
class TxSignalSl(TxSignal):

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent, signal, event):
        super().__init__(parent, signal)
        if self._value == "SNA":
            for k, v in signal.choices.items():
                if v == self._value:
                    self.value_var = tk.IntVar(value=k)
        else:
            self.value_var = tk.IntVar(value=self._value)
        self.input = tk.Scale(parent,
                              variable=self.value_var,
                              from_=signal.minimum,
                              to=signal.maximum,
                              resolution=signal.scale,
                              orient=tk.HORIZONTAL)
        # input is Slider object. Binds modify_periodic_message method to slider when leftclick(-1) button release
        # event is triggered
        self.input.bind("<ButtonRelease-1>", event)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def value(self):
        return self.value_var.get()

    # ------------------------------------------------------------------------------------------------------------------
    @value.setter
    def value(self, new_value):
        self.value_var.set(new_value)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TxSignalEd(TxSignal):

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent, signal, event):
        super().__init__(parent, signal)
        self.value_var = tk.IntVar(value=self._value)
        vcmd = (parent.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.input = tk.Entry(parent, textvariable=self.value_var, validate='all', validatecommand=vcmd)
        self.input.bind("<Return>", event)

    # ------------------------------------------------------------------------------------------------------------------
    def validate(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if value_if_allowed:
            try:
                int(value_if_allowed)
                return True
            except ValueError:
                return False
        else:
            return True

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def value(self):
        try:
            return self.value_var.get()
        except:
            return 0

    # ------------------------------------------------------------------------------------------------------------------
    @value.setter
    def value(self, new_value):
        self.value_var.set(new_value)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TxSignalDd(TxSignal):

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent, signal, event):
        super().__init__(parent, signal)
        self.input = ttk.Combobox(parent, values=list(signal.choices.values()))
        self.input.bind("<<ComboboxSelected>>", event)

        # Prevent value change by scrolling with mouse wheel
        self.input.unbind_class("TCombobox", "<MouseWheel>")

        for i, val in enumerate(list(signal.choices.values())):
            if val == self._value:
                self.input.current(i)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def value(self):
        return self.input.get()

    # ------------------------------------------------------------------------------------------------------------------
    @value.setter
    def value(self, new_value):
        self.input.set(new_value)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Message(tk.LabelFrame):

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent, database, message_name):
        super().__init__(parent, text=message_name)
        self.name = message_name
        self.signal_list = []
        # get message object from database
        self.dbc_message = database.get_message_by_name(message_name)

        self.dbc_message.signals.sort(key=Signal.get_name)

    def get_name(self):
        return self.name


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class TxMessage(Message):

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, parent, database, can_bus, message_name):
        super().__init__(parent, database, message_name)

        self.can_bus = can_bus
        self.task_tx_periodic = None

        self.isVisible = tk.IntVar()

        self.visibleLabel = tk.Label(self, text="visible")
        self.visibleLabel.grid(row=0, column=0, sticky='NWSE')

        self.visibleCB = tk.Checkbutton(self, var=self.isVisible,
                                                    command=self.set_visible)
        self.visibleCB.grid(row=0, column=1, sticky='NWSE')

        self.outPanel = tk.Frame(self)
        self.outPanel.grid(row=1, column=0, columnspan=2)
        if message_name in visibleMessagesList:
            self.isVisible.set(1)
        else:
            self.outPanel.grid_remove()

        self.maxMux = -1
        self.curMux = 0
        self.muxSig = None

        if self.dbc_message.is_multiplexed() is True:
            for sig in self.dbc_message.signals:
                if sig.multiplexer_ids:
                    if sig.multiplexer_ids[0] > self.maxMux:
                        self.maxMux = sig.multiplexer_ids[0]

        # append different widget objects to signal list
        for index, signal in enumerate(self.dbc_message.signals):
            # if the txmessage is 16 or 10 bits long, then create slider with init values of the signal
            if signal.length == 16 or signal.length == 10 or signal.length == 15:
                tx_signal = TxSignalSl(self.outPanel, signal, self.modify_periodic_message)

            # create label and checkbox if just 1 bit long
            elif signal.length == 1:
                tx_signal = TxSignalCb(self.outPanel, signal, self.modify_periodic_message)

            # create dropdown if signal has defined choices and more than 1 choice, event return key pressed  ->
            # modify_periodic_message
            elif signal.choices and len(signal.choices) > 2:
                tx_signal = TxSignalDd(self.outPanel, signal, self.modify_periodic_message)

            # create entry frame, event return key pressed -> modify_periodic_message
            else:
                tx_signal = TxSignalEd(self.outPanel, signal, self.modify_periodic_message)

            # set widget in grid (10 rows each signal list has a textlabel and a specific widget input)
            tx_signal.set_position(index, 11)
            if tx_signal.is_mux():
                self.muxSig = tx_signal
                self.muxSig.input.config(state=tk.DISABLED)
            self.signal_list.append(tx_signal)

    # ------------------------------------------------------------------------------------------------------------------
    def set_position(self, index, max_columns):
        row = int(index / max_columns)
        column = index % max_columns

        self.grid(row=row, column=column, sticky='NWSE')

    def mux_task(self):
        # when active, cycle through all possible mux values
        if self.task_tx_periodic:
            self.curMux += 1
            self.curMux %= self.maxMux + 1
            self.muxSig.value_var.set(self.curMux)
            self.muxSig.value = self.curMux
            self.modify_periodic_message()
            # do this with half the cycle time, so each value is sent definitely
            self.outPanel.after(self.dbc_message.cycle_time*2, self.mux_task)

    # ------------------------------------------------------------------------------------------------------------------
    # local method that start the periodic sending
    def start_sending_periodic(self):
        if not self.task_tx_periodic:
            signal_dictionary = {}
            # write signal values to the corresponding signal names in dbc messages
            if self.muxSig:
                self.curMux = self.muxSig.value
            for signal in self.signal_list:
                if signal.get_mux() == self.curMux or signal.get_mux() < 0:
                    signal_dictionary[signal.name] = signal.value
            # write signal values to the corresponding signal names in dbc messages
            #signal_dictionary = {signal.name: signal.value for signal in self.signal_list}

            # create message object with configurations of dbc_message
            message = can.Message(arbitration_id=self.dbc_message.frame_id,
                                  data=self.dbc_message.encode(signal_dictionary),
                                  is_extended_id=self.dbc_message.is_extended_frame)

            # starts a send thread that sends the message object periodic
            self.task_tx_periodic = self.can_bus.send_periodic(message, 0.10)

        else:
            self.task_tx_periodic.start()
        # when there is a muxing signal, enable muxing timer with half of message cycletime
        if self.muxSig:
            self.outPanel.after(self.dbc_message.cycle_time*2, self.mux_task)

    # ------------------------------------------------------------------------------------------------------------------
    def stop_sending_periodic(self):
        # write signal values to the corresponding signal names in dbc messages
        if self.task_tx_periodic:
            self.task_tx_periodic.stop()

    # ------------------------------------------------------------------------------------------------------------------
    def modify_periodic_message(self, event=0):
        if self.task_tx_periodic:
            signal_dictionary = {}
            if self.muxSig:
                self.curMux = self.muxSig.value
            # write signal values to the corresponding signal names in dbc messages
            for signal in self.signal_list:
                if signal.get_mux() == self.curMux or signal.get_mux() < 0:
                    signal_dictionary[signal.name] = signal.value

            # signal_dictionary = {signal.name: signal.value for signal in self.signal_list}

            # write all values to the corresponding signals of the message into message
            message = can.Message(arbitration_id=self.dbc_message.frame_id,
                                  data=self.dbc_message.encode(signal_dictionary),
                                  is_extended_id=self.dbc_message.is_extended_frame)

            # modify the send message
            self.task_tx_periodic.modify_data(message)

    def set_visible(self):
        if self.isVisible.get() == 1:
            self.outPanel.grid()
        else:
            self.outPanel.grid_remove()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class RxMessage(Message):
    def __init__(self, parent, database, message_name):
        super().__init__(parent, database, message_name)
        self.isVisible = tk.IntVar()

        self.visibleLabel = tk.Label(self, text="visible")
        self.visibleLabel.grid(row=0, column=0, sticky='NWSE')

        self.visibleCB = tk.Checkbutton(self, var=self.isVisible,
                                                    command=self.set_visible)
        self.visibleCB.grid(row=0, column=1, sticky='NWSE')

        self.outPanel = tk.Frame(self)
        self.outPanel.grid(row=1, column=0, columnspan=2)
        if message_name in visibleMessagesList:
            self.isVisible.set(1)
        else:
            self.outPanel.grid_remove()

        # add all signals of this message to signal list
        self.signals = [RxSignal(self.outPanel, row+1, signal.name, '-') for row, signal in enumerate(self.dbc_message.signals)]

    # ------------------------------------------------------------------------------------------------------------------
    def update(self, rx_data):
        for name, value in rx_data.items():
            [signal.update(value) for signal in self.signals if signal.name == name]

    # ------------------------------------------------------------------------------------------------------------------
    def set_position(self, index, max_columns):
        row = int(index / max_columns)
        column = index % max_columns

        self.grid(row=row, column=column, sticky='NWSE')

    def set_visible(self):
        if self.isVisible.get() == 1:
            self.outPanel.grid()
        else:
            self.outPanel.grid_remove()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ScrollFrame(tk.LabelFrame):

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.canvas = tk.Canvas(self, borderwidth=0)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", self.__on_frame_configure)

        # Add mouse scroll event
        self.canvas.bind_all("<MouseWheel>", self.__on_mousewheel)

    # ------------------------------------------------------------------------------------------------------------------
    def __on_frame_configure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    # ------------------------------------------------------------------------------------------------------------------
    # Scroll by mouse wheel
    def __on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class MessageList:

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, database, can_bus, target_name, tester_name, parent):
        self.database = database
        self.can_bus = can_bus

        self.__setup_config_frame(parent)
        self.__setup_rx_frame(parent, target_name)
        self.__setup_tx_frame(parent, tester_name)

        # Print every sender which is not handled
        [print(msg.senders[0]) for msg in self.database.messages if msg.senders[0] not in [target_name, tester_name]]

        parent.bind('<<Connect>>', self.__event_connect, add='+')

    # ------------------------------------------------------------------------------------------------------------------
    def __setup_config_frame(self, parent):

        self.configuration_frame = tk.LabelFrame(parent, text="Config")
        self.enable_periodic_tx = tk.IntVar()

        self.enable_periodic_tx_label = tk.Label(self.configuration_frame, text="Enable period transmit")
        self.enable_periodic_tx_label.grid(row=0, column=0, sticky='NWSE')
        self.enable_periodic_tx_cb = tk.Checkbutton(self.configuration_frame, var=self.enable_periodic_tx,
                                                    command=self.send_messages)
        self.enable_periodic_tx_cb.grid(row=0, column=1, sticky='NWSE')

        self.configuration_frame.pack(fill='x')

    # ------------------------------------------------------------------------------------------------------------------
    def __setup_rx_frame(self, parent, target_name):

        # Rx Frame in tab_frame
        self.target_frame = ScrollFrame(parent, text="Rx Messages")
        self.target_list = [RxMessage(self.target_frame.frame, self.database, msg.name)
                            for msg in self.database.messages if msg.senders[0] == target_name]

        self.target_list.sort(key=Message.get_name)

        [target.set_position(index, MAX_COLUMNS) for index, target in enumerate(self.target_list)]

        self.target_frame.pack(fill='both', expand=True)

        self.receive_thread = threading.Thread(target=self.__receive_messages, daemon=True)
        self.receive_thread.start()

    # ------------------------------------------------------------------------------------------------------------------
    def __setup_tx_frame(self, parent, tester_name):

        # Tx Frame in tab_frame
        self.tester_frame = ScrollFrame(parent, text="Tx Messages")

        self.tester_list = [TxMessage(self.tester_frame.frame, self.database, self.can_bus, msg.name)
                            for msg in self.database.messages if msg.senders[0] == tester_name]

        self.tester_list.sort(key=Message.get_name)

        [tester.set_position(index, MAX_COLUMNS) for index, tester in enumerate(self.tester_list)]

        self.tester_frame.pack(fill='both', expand=True)

    # ------------------------------------------------------------------------------------------------------------------
    def send_messages(self):
        if self.enable_periodic_tx.get():
            for msg in self.tester_list:
                msg.start_sending_periodic()
        else:
            for msg in self.tester_list:
                msg.stop_sending_periodic()

    # ------------------------------------------------------------------------------------------------------------------
    def __receive_messages(self):

        try:
            while 1:
                for msg in self.can_bus:
                    for rx_message in self.target_list:
                        if msg.arbitration_id == rx_message.dbc_message.frame_id:
                            decoded_data = self.database.decode_message(msg.arbitration_id, msg.data)
                            rx_message.update(decoded_data)

                time.sleep(0.1)
        except can.interfaces.pcan.pcan.PcanError:
            pass

    # ------------------------------------------------------------------------------------------------------------------
    def update_signals(self, signal_list):
        for key, value in signal_list.items():
            for message in self.tester_list:
                for signal in message.signal_list:
                    if key == signal.name:
                        signal.value = value

    # ------------------------------------------------------------------------------------------------------------------
    def __event_connect(self, event):
        if event.state == 1:
            self.send_messages()
            self.receive_thread = threading.Thread(target=self.__receive_messages, daemon=True)
            self.receive_thread.start()
        else:
            for msg in self.tester_list:
                msg.stop_sending_periodic()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ChargingSimulation:
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        # get application path
        script_dir = os.path.dirname(os.path.realpath(__file__))
        script_dir = os.path.join(script_dir, "../../40_Network")
        # join path -> "application_path + 'DBC_CCL_BCU.db'"
        vcu_dbc_path = os.path.join(script_dir, 'ISC_CMS_Automotive.dbc')

        self.database_vcu = cantools.db.load_file(vcu_dbc_path)

        # Main window
        self.root = tk.Tk()
        self.root.title("CMS Can Interface")
        self.root.minsize(1800, 800)

        # Create parent tab/notebook object
        self.tab_parent = ttk.Notebook(self.root)

        # Create tab objects in parent tab
        self.tab_vcu = ttk.Frame(self.tab_parent)

        # Add tab to parent tab
        self.tab_parent.add(self.tab_vcu, text="VCU")

        self.button = tk.Button(self.root, text="Disconnect", command=self.__connect)
        self.button.pack(side=tk.TOP, anchor=tk.NW, padx=5, pady=5)
        self.connected = True
        self.tab_parent.pack(expand=1, fill='both')

        self.can_bus = [can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)]

        if len(self.can_bus) > 0:
            # Go through database_vcu and generate GUI in tab_vcu out of it
            self.vcu_list = MessageList(self.database_vcu, self.can_bus[0], 'CMS', 'VCU', self.tab_vcu)

            vcu_init_list = {'ChargeStopIndication': 'NoStop',
                             'ChargeProgressIndication': 'Start',
                             'EVMaxVoltage': 500,
                             'EVMaxCurrent': 150,
                             'EVTargetVoltage': 450,
                             'EVPreChargeVoltage': 440,
                             'EVTargetCurrent': 75,
                             'EVReady': 'True',
                             'EVErrorCode': 'NO_ERROR',
                             'EVChargingComplete': 'False',
                             'EVSoC': 50,
                             'ChargeProtocolPriority': 'ISO_only',
                             'DBCVersion': 'ISO_20_READY'}
            self.vcu_list.update_signals(vcu_init_list)
            self.vcu_list.send_messages()

        self.root.mainloop()

    # ------------------------------------------------------------------------------------------------------------------
    def __connect(self):
        if self.connected:
            self.connected = False
            self.button['text'] = 'Connect'
            self.tab_vcu.event_generate('<<Connect>>', state=0)

            for bus in self.can_bus:
                bus.shutdown()

        else:
            self.can_bus = [can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS1', bitrate=500000)]

            self.tab_vcu.event_generate('<<Connect>>', state=1)

            self.button['text'] = 'Disconnect'
            self.connected = True


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == "__main__":
    # execute only if run as a script
    ChargingSimulation()
