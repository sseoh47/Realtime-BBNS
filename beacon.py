# -*- coding: utf-8 -*-
from bluepy.btle import Scanner, DefaultDelegate
import struct

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

def parse_ibeacon_packet(packet):
    if len(packet) == 31:
        uuid = packet[9:25]
        major = struct.unpack(">h", packet[25:27])[0]
        minor = struct.unpack(">h", packet[27:29])[0]
        tx_power = struct.unpack("b", packet[29:30])[0]
        print("UUID: {}, Major: {}, Minor: {}, Tx Power: {}".format(uuid.hex(), major, minor, tx_power))


scanner = Scanner().withDelegate(ScanDelegate())

print("Scanning for iBeacon devices...")
devices = scanner.scan(10.0)

for dev in devices:
    for (adtype, desc, value) in dev.getScanData():
        if adtype == 255:
            data = bytes(bytearray.fromhex(value))
            if data[0:4] == b"\x4c\x00\x02\x15":
                parse_ibeacon_packet(data)
