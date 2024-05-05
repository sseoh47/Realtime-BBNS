from bluepy.btle import Scanner, DefaultDelegate


# 원하는 비콘의 UUID
desired_uuid = "e2c56db5-dffb-48d2-b060-d0f5a71096e0" # 여기에 원하는 UUID를 넣으세요

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        for (adtype, desc, value) in dev.getScanData():
            if value == desired_uuid:
                print("Desired UUID found:")
                print("UUID:", value)
                print("RSSI:", dev.rssi)
                return

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(30.0) 
