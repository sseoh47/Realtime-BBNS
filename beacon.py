from beacontools import BeaconScanner, IBeaconFilter
import time

#iBeacon 예제를 사용
class Beacon:
    def __init__(self):
        print("beacon탐색 시작")

    # bluetooth address(MAC), rssi(신호세기), major, minnor 등 값을 출력
    # BeaconScanner 클래스를 만들 때 callback으로 들어가게되는 함수
    def callback(self, uuid, rssi, packet, additional_info):
        print("<%s, %d> %s %s" % (uuid, rssi, packet, additional_info))
        # uuid로 현재 위치 먼저 판별
        if uuid=='station':
            print("영남대 정류장")
            # 버스 검색
            
        
        elif uuid=='bus':
            if(rssi<=40):
                print("들어오는 중")
            elif(rssi>=70):
                print("가까이 오는 중")
            else:
                print("버스 정차")


    def scan(self):
        scanner = BeaconScanner(self.callback, device_filter=IBeaconFilter(uuid="e2c56db5-dffb-48d2-b060-d0f5a71096e0"), bt_device_id=0)

        scanner.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            scanner.stop()
    

if __name__=="__main__":
    beacon=Beacon()
    beacon.scan()