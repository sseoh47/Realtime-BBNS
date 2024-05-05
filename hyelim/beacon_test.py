from beacontools import BeaconScanner, IBeaconFilter
import time
import numpy as np

BUS = "e2c56db5-dffb-48d2-b060-d0f5a71096e0"


class Beacon:
    def __init__(self):
        print("** beacon Searching Start **")
        self.rssi_values = []
    
    def callback(self, bt_addr, rssi, packet, additional_info):
        print(f"<{bt_addr}, {rssi}> {packet} {additional_info}")
        self.rssi_values.append(rssi)
        
        if len(self.rssi_values) >= 10:
            distance_values = [self.rssi_to_distance(rssi) for rssi in self.rssi_values]
            filtered_distance = np.mean(distance_values)
            
            print("avg distance:", filtered_distance)
            self.rssi_values.clear()

    def scan(self):
        scanner = BeaconScanner(self.callback, device_filter=IBeaconFilter(major=40011), bt_device_id=0)
        scanner.start()

        try:
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            scanner.stop()
    
    def moving_average_filter(self, values, window_size):
        return np.convolve(values, np.ones(window_size)/window_size, mode='valid')
        
    def rssi_to_distance(self, rssi):
        txPower = -59
        
        if rssi == 0:
            return -1.0
    
        ratio = rssi * 1.0 / txPower
        
        if ratio < 1.0:
            return ratio ** 10
        else:
            distance = (0.89976) * (ratio ** 7.7095) + 0.111
            
            return distance


if __name__=="__main__":
    beacon = Beacon()
    beacon.scan()