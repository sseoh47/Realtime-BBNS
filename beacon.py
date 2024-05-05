from bluepy.btle import Scanner, DefaultDelegate
import struct

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

def parse_ibeacon_packet(packet):
    # iBeacon 패킷 구조에 맞게 데이터를 파싱합니다.
    if len(packet) == 31:
        uuid = packet[9:25]
        major = struct.unpack(">h", packet[25:27])[0]
        minor = struct.unpack(">h", packet[27:29])[0]
        tx_power = struct.unpack("b", packet[29:30])[0]
        # UUID, Major, Minor 및 Tx Power 값을 출력합니다.
        print(f"UUID: {uuid.hex()}, Major: {major}, Minor: {minor}, Tx Power: {tx_power}")

scanner = Scanner().withDelegate(ScanDelegate())

print("Scanning for iBeacon devices...")
devices = scanner.scan(10.0) # 10초 동안 스캔

for dev in devices:
    for (adtype, desc, value) in dev.getScanData():
        if adtype == 255: # Manufacturer specific data
            data = bytes(bytearray.fromhex(value))
            # Apple's iBeacon prefix
            if data[0:4] == b"\x4c\x00\x02\x15":
                parse_ibeacon_packet(data)
