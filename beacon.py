from bluepy.btle import Scanner, DefaultDelegate

desired_uuid = "e2c56db5-dffb-48d2-b060-d0f5a71096e0"

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("New device:", dev.addr, "RSSI: ", dev.rssi)
        elif isNewData:
            print("New data from", dev.addr, "RSSI: ", dev.rssi)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)  # 10초 동안 스캔

for dev in devices:
    for (adtype, desc, value) in dev.getScanData():
        if desc == 'Complete 128b Services' and value.startswith('fd6f'):
            print("UUID:", value)
            print("RSSI:", dev.rssi)
