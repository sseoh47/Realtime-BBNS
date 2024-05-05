from beacontools import BeaconScanner, IBeaconFilter
import time
import numpy as np

BUS = "e2c56db5-dffb-48d2-b060-d0f5a71096e0"


class Beacon:
    def __init__(self):
        print("** beacon Searching Start **")
        self.rssi_values = []  # RSSI 값 저장을 위한 리스트 초기화

    # def callback(self, uuid, rssi, packet, additional_info):
    #     print("<%s, %d> %s %s" % (uuid, rssi, packet, additional_info))
    
    def callback(self, bt_addr, rssi, packet, additional_info):
        print(f"<{bt_addr}, {rssi}> {packet} {additional_info}")
        self.rssi_values.append(rssi)
        
        if len(self.rssi_values) >= 10:  # RSSI 값이 10개 이상 쌓이면
            distance_values = [self.rssi_to_distance(rssi) for rssi in self.rssi_values]
            filtered_distance = np.mean(distance_values)  # 평균 거리 계산
            
            print("평균 거리 값:", filtered_distance)
            self.rssi_values.clear()  # 분석 후 RSSI 값 초기화

    def scan(self):
        scanner = BeaconScanner(self.callback, device_filter=IBeaconFilter(major=40011))  #, bt_device_id=0)
        scanner.start()

        try:
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            scanner.stop()
    
    # 평균 필터 적용 함수
    def moving_average_filter(self, values, window_size):
        return np.convolve(values, np.ones(window_size)/window_size, mode='valid')
        
    # RSSI 값을 거리로 변환하는 함수 (단순화된 예시, 실제 환경에서는 보정 필요)
    def rssi_to_distance(self, rssi):
        # 이 부분은 측정 환경에 따라 조정해야 할 수 있습니다.
        txPower = -59  # 1미터 떨어진 지점에서의 RSSI 값. 실제 환경에서 측정 필요
        
        if rssi == 0:
            return -1.0  # 불가능한 값
    
        ratio = rssi * 1.0 / txPower
        
        if ratio < 1.0:
            return ratio ** 10
        else:
            distance = (0.89976) * (ratio ** 7.7095) + 0.111
            
            return distance


if __name__=="__main__":
    beacon = Beacon()
    
    
    # # RSSI 값 예시
    # rssi_values = [-70, -72, -68, -71, -70, -69, -72, -73, -71, -70]

    # # RSSI를 거리로 변환
    # distance_values = [beacon.rssi_to_distance(rssi) for rssi in rssi_values]

    # # 평균 필터 적용
    # window_size = 3
    # filtered_distances = beacon.moving_average_filter(distance_values, window_size)

    # print("원본 거리 값:", distance_values)
    # print("평균 필터 적용 후:", filtered_distances)
    
    beacon.scan()