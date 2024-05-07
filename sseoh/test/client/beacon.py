from bluepy.btle import Scanner, DefaultDelegate
from client import*  # 클라이언트 코드를 import
from constant import*

BUS = "BUS"  
STATION = "YU_UNIV"

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.current_thread = None  # current_thread 속성 초기화
        self.is_active = False  # is_active 속성 초기화
        print("beacon init")

    def send_beacon_in_thread(self, beacon_name, rssi):
        if self.current_thread and self.current_thread.is_alive():
            self.is_active = False  # 현재 스레드에 종료 요청
            self.current_thread.join()  # 현재 스레드가 종료될 때까지 기다림

        self.is_active = True
        self.current_thread = threading.Thread(target=self.send_beacon, args=(beacon_name, rssi))  # 수정 필요: client.send_beacon -> self.send_beacon
        self.current_thread.start()

    def handleDiscovery(self, dev, isNewDev, isNewData):
        try:
            for (adtype, desc, value) in dev.getScanData():
                print("for finding beacon")
                if adtype == 9 and value in [BUS, STATION]:  # 조건 수정 필요: BUS, STATION 값 정의 필요
                    print("Name:", value)
                    print("RSSI:", dev.rssi)
                    self.send_beacon_in_thread(value, dev.rssi)

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