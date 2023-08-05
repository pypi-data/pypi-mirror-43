from .shelly import (Shelly, Wifi_sta)
import logging
import json
from shellypython.helpers import (Call_shelly_api, Get_item_safe)

logging.basicConfig(level=logging.DEBUG)


x = Shelly("192.168.1.81").update_data()
print(x.__dict__)
print(type(x.wifi_sta.ssid))
print((x.wifi_sta.ssid))
# print(x)
# print(type(x))
# x.update_data()
# print (x.__dict__)