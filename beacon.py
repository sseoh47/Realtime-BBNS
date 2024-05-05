from beacontools import BeaconScanner, IBeaconFilter

def callback(bt_addr, rssi, packet, additional_info):
    print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))

my_ibeacon_filter = IBeaconFilter(uuid="e2c56db5-dffb-48d2-b060-d0f5a71096e0")
scanner = BeaconScanner(callback, bt_device_id=0 ,device_filter=my_ibeacon_filter)
scanner.start()