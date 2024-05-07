from bluepy.btle import Scanner, DefaultDelegate
from client import*  # 클라이언트 코드를 import
from constant import*

BUS = "BUS"  
STATION = "YU_UNIV"

class ScanDelegate(DefaultDelegate):
    def __init__(self, client):
        DefaultDelegate.__init__(self)
        self.client = client  # Client 인스턴스를 저장
        self.current_thread = None
        self.is_active = False
        print("beacon init")

    def send_beacon_in_thread(self, beacon_name, rssi):
        if self.current_thread and self.current_thread.is_alive():
            self.is_active = False  # 현재 스레드에 종료 요청
            self.current_thread.join()  # 현재 스레드가 종료될 때까지 기다림

        self.is_active = True
        # Client 인스턴스의 send_beacon 메소드를 호출
        self.current_thread = threading.Thread(target=self.client.send_beacon, args=(beacon_name, rssi))
        self.current_thread.start()

    def handleDiscovery(self, dev, isNewDev, isNewData):
        try:
            for (adtype, desc, value) in dev.getScanData():
                print("for finding beacon")
                if adtype == 9 and value in [BUS, STATION]:  # 조건 수정 필요: BUS와 STATION 값을 정의해야 합니다.
                    print("Name:", value)
                    print("RSSI:", dev.rssi)
                    self.send_beacon_in_thread(value, dev.rssi)

        except KeyboardInterrupt:
            print("Scanning stopped")
        except Exception as e:
            print(f"Error occurred while receiving message: {e}")

if __name__ == "__main__":
    client = Client(SERVER_HOST, PORT)  # 이 부분에서 Client 클래스를 인스턴스화
    scanner = Scanner().withDelegate(ScanDelegate(client))  # Client 인스턴스를 ScanDelegate에 전달
    try:
        while True:
            print("scanner while")
            devices = scanner.scan(3.0)  # 3초 동안 스캔
    except KeyboardInterrupt:
        print("Scanning stopped")
