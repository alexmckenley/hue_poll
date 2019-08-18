import sys, os, time, math
import requests
import ctypes
from rgbxy import Converter, GamutC

timeout = 3
iterations = math.floor((60 - timeout) / timeout)

# def adjust(num, max):
#     pct = num / 255
#     val = math.floor(max * pct)
#     return val

lastHex = ""
for i in range(iterations):
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

        if hex != lastHex:
            lastHex = hex
            # Update liquidctl
            liquidctlpath = "C:\\Users\\Alex\\Documents\\GitHub\\hue_poll\\liquidctl-1.1.0-bin-windows-x86_64\\liquidctl.exe"
            os.system(liquidctlpath + " set sync color fixed " + hex)

            # Update MSIRBG
            # (r, g, b) = converter.xy_to_rgb(data["state"]["xy"][0],data["state"]["xy"][1], bri=0.05)
            # r = adjust(r, 255)
            # g = adjust(g, 255)
            # b = adjust(b, 255)
            # print(r, g, b)
            # huepollmsipath = "C:\\Users\\Alex\\Documents\\GitHub\\HuePollMSIRGB\\HuePollMSIRGB\\bin\\x64\\Debug\\HuePollMSIRGB.exe"
            # os.system(huepollmsipath + " " + str(r) + " " + str(g) + " " + str(b))

            print('Success: ' + hex)
    else:
        raise Exception('HTTP Request unsuccessful')
    time.sleep(timeout)