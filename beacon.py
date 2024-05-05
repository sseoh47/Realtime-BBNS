from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("New device:", dev.addr)
        elif isNewData:
            print("New data from", dev.addr)

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)

for dev in devices:
    for (adtype, desc, value) in dev.getScanData():
        if desc == 'Complete 128b Services' and value.startswith('fd6f'):
            print("UUID:", value)
            print("RSSI:", dev.rssi)
