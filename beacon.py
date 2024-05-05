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

        for (adtype, desc, value) in dev.getScanData():
            if desc == 'Complete 128b Services' and value.startswith('fd6f'):
                if value == desired_uuid:
                    print("Desired UUID found:")
                    print("UUID:", value)
                    print("RSSI:", dev.rssi)
                    return

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0) 
