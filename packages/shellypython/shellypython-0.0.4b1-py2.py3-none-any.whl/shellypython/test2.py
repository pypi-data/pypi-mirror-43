from .shelly import (Shelly, Wifi_sta)
import logging
import json
from shellypython.helpers import (Call_shelly_api, Get_item_safe, Rssi_to_percentage)

logging.basicConfig(level=logging.DEBUG)


print(Rssi_to_percentage(None))
print(Rssi_to_percentage(-100))
print(Rssi_to_percentage(-70))
x = Shelly("192.168.1.82").update_data()
print(len(x.rollers))
print(x.rollers[0].__dict__)
x = Shelly("192.168.1.81").update_data()
print(len(x.relays))
print(x.relays[0].__dict__)
# print(x)
# print(type(x))
# x.update_data()
# print (x.__dict__)