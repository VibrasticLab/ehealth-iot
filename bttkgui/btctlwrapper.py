#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import pexpect
import subprocess

class BluetoothctlError(Exception):
    """ Raised when Bluetoothctl fails to start."""
    pass

class BluetoothctlWrapper:
    """ Python Wrapper for Bluetoothctl. """

    def __init__(self):
        """ Start Bluetoothctl process """
 
        out = subprocess.check_output("bluetoothctl power on",shell=True)
        out = subprocess.check_output("bluetoothctl agent on",shell=True)
        self.child = pexpect.spawn("bluetoothctl",echo=False)

    def get_output(self,command,pause=0):
        """ Run a command in bluetoothctl prompt.
        Return output as list of lines
        """

        self.child.send(command+"\n")
        time.sleep(pause)
        start_failed = self.child.expect(["bluetooth",pexpect.EOF])

        if start_failed:
            raise BluetoothctlError("Bluetoothctl failed running"+command)

        result = self.child.before.decode('utf-8').rstrip()
        return result.split("\r\n")

    def make_discoverable(self):
        """ Make discoverable"""

        try:
            out = self.get_output("discoverable on")
        except BluetoothctlError:
            return None

    def start_scan(self):
        """ Start bluetooth scanning process."""

        try:
            out = self.get_output("scan on")
        except BluetoothctlError:
            return None

    def stop_scan(self):
        """ Stop bluetooth scanning process"""

        try:
            out = self.get_output("scan off")
        except BluetoothctlError:
            return None

    def parse_device_info(self,info_string):
        """ Parse a string corresponding to a device"""

        device = {}
        block_list = ["[\x1b[0;", "removed"]
        string_valid = not any(keyword in info_string for keyword in block_list)

        if string_valid:
            try:
                device_position = info_string.index("Device")
            except ValueError:
                pass
            else:
                if device_position > -1:
                    attribute_list = info_string[device_position:].split(" ",2)
                    device = {
                            "mac_address": attribute_list[1],
                            "name": attribute_list[2]
                    }

        return device

    def get_available_devices(self):
        """ Return a list of tuples of nearby available devices"""

        try:
            out = self.get_output("devices")
        except BluetoothctlError:
            return None
        else:
            available_devices = []
            for line in out:
                device = self.parse_device_info(line)
                if device:
                    available_devices.append(device)

            return available_devices

    def get_paired_devices(self):
        """ Return a list of tuples of paired devices"""

        try:
            out = self.get_output("paired-devices")
        except BluetoothctlError:
            return None
        else:
            paired_devices = []
            for line in out:
                device = self.parse_device_info(line)
                if device:
                    paired_devices.append(device)

            return paired_devices

    def get_discoverable_devices(self):
        """ Filter discoverable device"""

        available = self.get_available_devices()
        paired = self.get_paired_devices()

        return [d for d in available if d not in paired]

    def pair(self,mac_address):
        """ Try to pair with a device by mac_address"""

        try:
            out = self.get_output("pair "+mac_address,4)
        except BluetoothctlError:
            return None
        else:
            res = self.child.expect(["Failed to pair", "Pairing successful", pexpect.EOF])
            success = True if res == 1 else False
            return success

    def trust(self,mac_address):
        """ Try to mark trust to a device by mac_address"""

        try:
            out = self.get_output("trust "+mac_address,1)
        except BluetoothctlError:
            return None

    def remove(self,mac_address):
        """ Remove a paired device by mac_address"""

        try:
            out = self.get_output("remove "+mac_address,3)
        except BluetoothctlError:
            return None
        else:
            res = self.child.expect(["not available","Device has been removed",pexpect.EOF])
            success = True if res == 1 else False
            return success

    def connect(self,mac_address):
        """ Try to connect to a device by mac_address"""

        try:
            out = self.get_output("connect "+mac_address,2)
        except BluetoothctlError:
            return None
        else:
            res = self.child.expect(["Failed to connect", "Connection successful", pexpect.EOF])
            success = True if res == 1 else False
            return success

    def disconnect(self,mac_address):
        """ Try to disconnect a device by mac_address"""

        try:
            out = self.get_output("disconnect "+mac_address,2)
        except BluetoothctlError:
            return None
        else:
            res = self.child.expect(["Failed to disconnect","Successful disconnected",pexpect.EOF])
            success = True if res == 1 else False
            return success

if __name__ == "__main__":
    btctl  = BluetoothctlWrapper()
    print("Start Scanning")
    btctl.start_scan()
    print("scanning in 10s")
    time.sleep(10)
    print(btctl.get_discoverable_devices())
