from bluepy.btle import Scanner, DefaultDelegate

# 원하는 비콘의 이름
desired_name = "BUS"  # 여기에 원하는 비콘의 이름을 넣으세요

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        for (adtype, desc, value) in dev.getScanData():
            if adtype == 9 and value == desired_name:
                print("Desired Beacon found:")
                print("Name:", value)
                print("UUID:", dev.getValueText(7))
                print("RSSI:", dev.rssi)
                return

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan()
