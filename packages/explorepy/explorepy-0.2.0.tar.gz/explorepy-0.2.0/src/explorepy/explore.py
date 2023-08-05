# -*- coding: utf-8 -*-

from explorepy.bt_client import BtClient
from explorepy.parser import Parser
import bluetooth
import csv
import os
import time
from pylsl import StreamInfo, StreamOutlet


class Explore:
    r"""Mentalab Explore device"""
    def __init__(self, n_device=1):
        r"""
        Args:
            n_device (int): Number of devices to be connected
        """
        self.device = []
        self.socket = None
        self.parser = None
        for i in range(n_device):
            self.device.append(BtClient())

    def connect(self, device_name=None, device_addr=None, device_id=0):
        r"""
        Connects to the nearby device. If there are more than one device, the user is asked to choose one of them.

        Args:
            device_name (str): Device name in the format of "Explore_XXXX"
            device_addr (str): The MAC address in format "XX:XX:XX:XX:XX:XX" Either Address or name should be in
            the input

            device_id (int): device id

        """

        self.device[device_id].init_bt(device_name=device_name, device_addr=device_addr)

    def disconnect(self, device_id=None):
        r"""Disconnects from the device

        Args:
            device_id (int): device id (id=None for disconnecting all devices)
        """
        self.device[device_id].socket.close()

    def acquire(self, device_id=0):
        r"""Start getting data from the device

        Args:
            device_id (int): device id (id=None for disconnecting all devices)
        """

        self.socket = self.device[device_id].bt_connect()

        if self.parser is None:
            self.parser = Parser(self.socket)

        is_acquiring = True
        while is_acquiring:
            try:
                self.parser.parse_packet(mode="print")
            except ValueError:
                # If value error happens, scan again for devices and try to reconnect (see reconnect function)
                print("Disconnected, scanning for last connected device")
                socket = self.device[device_id].bt_connect()
                self.parser.socket = socket
            except bluetooth.BluetoothError as error:
                print("Bluetooth Error: attempting reconnect. Error: ", error)
                self.parser.socket = self.device[device_id].bt_connect()

    def record_data(self, file_name, do_overwrite=False, device_id=0):
        r"""Records the data in real-time

        Args:
            file_name (str): output file name
            device_id (int): device id
            do_overwrite (bool): Overwrite if files exist already
        """

        exg_out_file = file_name + "_ExG.csv"
        orn_out_file = file_name + "_ORN.csv"

        assert not (os.path.isfile(exg_out_file) and do_overwrite), exg_out_file + " already exists!"
        assert not (os.path.isfile(orn_out_file) and do_overwrite), orn_out_file + " already exists!"

        self.socket = self.device[device_id].bt_connect()

        if self.parser is None:
            self.parser = Parser(self.socket)

        with open(exg_out_file, "w") as f_eeg, open(orn_out_file, "w") as f_orn:
            f_orn.write("TimeStamp, ax, ay, az, gx, gy, gz, mx, my, mz \n")
            f_orn.write(
                "hh:mm:ss, mg/LSB, mg/LSB, mg/LSB, mdps/LSB, mdps/LSB, mdps/LSB, mgauss/LSB, mgauss/LSB, mgauss/LSB\n")
            f_eeg.write("TimeStamp, ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8\n")
            csv_eeg = csv.writer(f_eeg, delimiter=",")
            csv_orn = csv.writer(f_orn, delimiter=",")

            is_acquiring = True
            print("Recording...")

            while is_acquiring:
                try:
                    self.parser.parse_packet(mode="record", csv_files=(csv_eeg, csv_orn))
                except ValueError:
                    # If value error happens, scan again for devices and try to reconnect (see reconnect function)
                    print("Disconnected, scanning for last connected device")
                    self.parser.socket = self.device[device_id].bt_connect()
                except bluetooth.BluetoothError as error:
                    print("Bluetooth Error: Probably timeout, attempting reconnect. Error: ", error)
                    self.parser.socket = self.device[device_id].bt_connect()

    def push2lsl(self, n_chan, device_id=0):
        r"""Push samples to two lsl streams

        Args:
            device_id (int): device id
            n_chan (int): Number of channels (4 or 8)
        """
        self.socket = self.device[device_id].bt_connect()

        if self.parser is None:
            self.parser = Parser(self.socket)

        assert (n_chan is not None), "Number of channels missing"
        assert (n_chan == 4) or (n_chan == 8), "Number of channels should be either 4 or 8"

        info_orn = StreamInfo('Mentalab', 'Orientation', 9, 20, 'float32', 'explore_orn')
        info_eeg = StreamInfo('Mentalab', 'EEG', n_chan, 250, 'float32', 'explore_eeg')

        orn_outlet = StreamOutlet(info_orn)
        eeg_outlet = StreamOutlet(info_eeg)

        is_acquiring = True

        while is_acquiring:
            print("Pushing to lsl...")

            try:
                self.parser.parse_packet(mode="lsl", outlets=(orn_outlet, eeg_outlet))
            except ValueError:
                # If value error happens, scan again for devices and try to reconnect (see reconnect function)
                print("Disconnected, scanning for last connected device")
                self.socket = self.device[device_id].bt_connect()
                time.sleep(1)
                self.parser = Parser(self.socket)

            except bluetooth.BluetoothError as error:
                print("Bluetooth Error: Probably timeout, attempting reconnect. Error: ", error)
                self.socket = self.device[device_id].bt_connect()
                time.sleep(1)
                self.parser = Parser(self.socket)

    def visualize(self):
        r"""Start visualization of the data in the viewer (NOT IMPLEMENTED)

        Returns:

        """
        pass


if __name__ == '__main__':
    pass
