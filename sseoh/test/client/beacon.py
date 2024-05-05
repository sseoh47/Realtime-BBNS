from bluepy.btle import Scanner, DefaultDelegate
import time
from client import*  # 클라이언트 코드를 import
from constant import*

BUS = "BUS"  
STATION = "YU_UNIV"

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        print("beacon init")

    def handleDiscovery(self, dev, isNewDev, isNewData):
        for (adtype, desc, value) in dev.getScanData():
            print("for finding beacon")
            if adtype == 9 and value in [BUS, STATION]:  # 조건 수정
                print("Name:", value)
                print("RSSI:", dev.rssi)
                client.send_beacon(SERVER_HOST, PORT, value, dev.rssi)

    try:
        while True:
            devices = scanner.scan(3.0)  # 3초 동안 스캔
    except KeyboardInterrupt:
        print("Scanning stopped")

if __name__ == "__main__":
    client = Client()
    scanner = Scanner().withDelegate(ScanDelegate())
   

