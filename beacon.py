from beacontools import BeaconScanner, IBeaconFilter
import time


class Beacon:
    def __init__(self):
        print("beacon탐색 시작")

    def callback(self, uuid, rssi, packet, additional_info):
        print("<%s, %d> %s %s" % (uuid, rssi, packet, additional_info))



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