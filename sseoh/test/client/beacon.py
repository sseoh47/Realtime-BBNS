from bluepy.btle import Scanner, DefaultDelegate
from client import*  # 클라이언트 코드를 import
from constant import*

BUS = "BUS"  
STATION = "YU_UNIV"

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        print("beacon init")

    def handleDiscovery(self, dev, isNewDev, isNewData):
        try:
            for (adtype, desc, value) in dev.getScanData():
                print("for finding beacon")
                if adtype == 9 and value in [BUS, STATION]:  # 조건 수정
                    print("Name:", value)
                    print("RSSI:", dev.rssi)
                    client.send_beacon(SERVER_HOST, PORT, value, dev.rssi)

        except KeyboardInterrupt:
            print("Scanning stopped")
        except Exception as e:
            print(f"메시지 수신 중 오류 발생: {e}")
            
        
            

if __name__ == "__main__":
    client = Client(SERVER_HOST, PORT)
    scanner = Scanner().withDelegate(ScanDelegate())
    try:
        while True:
            print("scanner while")
            devices = scanner.scan(3.0)  # 3초 동안 스캔
    except KeyboardInterrupt:
        print("Scanning stopped")