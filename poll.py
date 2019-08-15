import sys, requests, os, time, math
from rgbxy import Converter, GamutC

timeout = 3
iterations = math.floor((60 - timeout) / timeout)

print(iterations)
for i in range(10):
    uri = "http://192.168.1.28/api/gBy8DB7KImW4A4KTOZFMndlc1Cqq3Fvgr13MSLpH/lights/10"
    response = requests.get(uri)
    if response:
        data = response.json()
        converter = Converter(gamut=GamutC)
        print(data)
        # Hard-code the brightness since it looks better
        # bri = data["state"]["bri"] / 255
        bri = .1
        hex = converter.xy_to_hex(data["state"]["xy"][0],data["state"]["xy"][1], bri=bri)
        liquidctlpath = "C:\\Users\\Alex\\Documents\\GitHub\\hue_poll\\liquidctl-1.1.0-bin-windows-x86_64\\liquidctl.exe"
        os.system(liquidctlpath + " set sync color fixed " + hex)
        print('Success: ' + hex)
    else:
        raise Exception('HTTP Request unsuccessful')
    time.sleep(5)