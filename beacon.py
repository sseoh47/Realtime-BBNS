from beacontools import BeaconScanner, IBeaconFilter

def callback(bt_addr, rssi, packet, additional_info):
    print("<%s, %d> %s %s" % (bt_addr, rssi, packet, additional_info))

scanner = BeaconScanner(callback, bt_device_id=0 ,device_filter=IBeaconFilter)
scanner.start()