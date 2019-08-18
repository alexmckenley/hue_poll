import sys, subprocess, time, math
import requests
import ctypes
from rgbxy import Converter, GamutC
from bg import processImages, getClosestImg

POLL_INTERVAL = 4 # seconds
led_bri = .1

def adjust(num, max):
    pct = num / 255
    val = math.floor(max * pct)
    return val

def loop():
    lastColor = ""
    while True:
        uri = "http://192.168.1.28/api/gBy8DB7KImW4A4KTOZFMndlc1Cqq3Fvgr13MSLpH/lights/10"
        response = requests.get(uri)
        if response:
            data = response.json()
            converter = Converter(gamut=GamutC)
            print(data)
            # Hard-code the brightness since it looks better
            bri = data["state"]["bri"] / 255
            rgb = converter.xy_to_rgb(data["state"]["xy"][0],data["state"]["xy"][1], bri=bri)

            if str(rgb) != lastColor:
                # Cache last value
                lastColor = str(rgb)

                # Update liquidctl
                hex_adjusted = converter.xy_to_hex(data["state"]["xy"][0],data["state"]["xy"][1], bri=led_bri)
                liquidctlpath = "C:\\Users\\Alex\\Documents\\GitHub\\hue_poll\\liquidctl-1.1.0-bin-windows-x86_64\\liquidctl.exe"
                subprocess.Popen([liquidctlpath, "set",  "sync", "color", "fixed", hex_adjusted], shell=True)

                # Update MSIRBG
                (r, g, b) = converter.xy_to_rgb(data["state"]["xy"][0],data["state"]["xy"][1], bri=led_bri)
                r = adjust(r, 255)
                g = adjust(g, 255)
                b = adjust(b, 255)
                print(r, g, b)
                huepollmsipath = "C:\\Users\\Alex\\Documents\\GitHub\\HuePollMSIRGB\\HuePollMSIRGB\\bin\\x64\\Debug\\HuePollMSIRGB.exe"
                subprocess.Popen([huepollmsipath, str(r), str(g), str(b)], shell=True)

                # Update windows background
                processImages()
                bestImg = getClosestImg(rgb)
                if bestImg is not None:
                    print('setting bg to:' + bestImg)
                    ctypes.windll.user32.SystemParametersInfoW(20, 0, bestImg , 0)

                print('Success: ' + str(rgb))
        else:
            print('Request failed')
        time.sleep(POLL_INTERVAL)

if __name__ == '__main__':
    loop()
