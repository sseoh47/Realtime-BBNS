from bluepy.btle import Scanner, DefaultDelegate


# 원하는 비콘의 UUID
desired_uuid = "74278bda-b644-4520-8f0c-720eaf059935" # 여기에 원하는 UUID를 넣으세요

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
