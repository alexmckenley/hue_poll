import serial
import time

START_MARKER = 254
END_MARKER = 255
ESCAPE_MARKER = 253

ser = None
initialized = False

def sendRGB(r, g, b):
  frame = bytes([r, g, b])
  sendToArduino(frame)

def sendToArduino(data):
  waitForArduino()
  if not initialized:
      return
  length = len(data)
  frame = bytearray()
  encodedData = encodeHighBytes(data)
  frame.append(START_MARKER)
  frame.append(length)
  frame += encodedData 
  frame.append(END_MARKER)
  ser.write(frame)

def encodeHighBytes(data):
  frame = bytearray()
  s = len(data)
  for n in range(0, s):
    x = data[n]
    if x >= ESCAPE_MARKER:
       frame.append(ESCAPE_MARKER)
       frame.append(x - ESCAPE_MARKER)
    else:
       frame.append(x)
  return(frame)

def waitForArduino():
    global initialized
    global ser
    if initialized:
        return
    try:
      ser = serial.Serial("COM5", 57600, timeout=5)
    except:
      return
    result = ser.read()
    if len(result) > 0:
        initialized = True