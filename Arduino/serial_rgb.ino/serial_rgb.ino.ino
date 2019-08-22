// 12 Mar 2014
// this works with ComArduino.py and ComArduinoA4e.rb
// this version uses a start marker 254 and an end marker of 255
//  it uses 253 as a special byte to be able to reproduce 253, 254 and 255
// it also sends data to the PC using the same system
//   if the number of bytes is 0 the PC will assume a debug string and just print it to the screen

//================

#define startMarker 254
#define endMarker 255
#define specialByte 253
#define maxMessage 16
#define R_PIN 11
#define G_PIN 6
#define B_PIN 3

byte bytesRecvd = 0;
byte dataSentNum = 0; // the transmitted value of the number of bytes in the package i.e. the 2nd byte received
byte dataRecvCount = 0;

byte outputPins[3] = {R_PIN, G_PIN, B_PIN};
byte dataRecvd[maxMessage];
byte dataSend[maxMessage];
byte tempBuffer[maxMessage];

boolean inProgress = false;
boolean startFound = false;
boolean allReceived = false;

//================

void setup() {
  pinMode(LED_BUILTIN, OUTPUT); // for debugging
  pinMode(R_PIN, OUTPUT);
  pinMode(G_PIN, OUTPUT);
  pinMode(B_PIN, OUTPUT);
  Serial.begin(57600);
  while (!Serial) {
    ;
  }
  Serial.write(255);
  blinkLED(20); // just so we know it's alive
}

//================

void loop() {
  getSerialData();
  processData();
}

//================

void getSerialData() {
  // Receives data into tempBuffer[]
  //   saves the number of bytes that the PC said it sent - which will be in tempBuffer[1]
  //   uses decodeHighBytes() to copy data from tempBuffer to dataRecvd[]

  // the Arduino program will use the data it finds in dataRecvd[]
  if (Serial.available() > 0) {
    byte x = Serial.read();
    if (x == startMarker) {
      bytesRecvd = 0;
      inProgress = true;
      digitalWrite(LED_BUILTIN, HIGH);
    }

    if (inProgress) {
      tempBuffer[bytesRecvd] = x;
      bytesRecvd ++;
    }

    if (x == endMarker) {
      inProgress = false;
      allReceived = true;

      // save the number of bytes that were sent
      dataSentNum = tempBuffer[1];

      decodeHighBytes();
      digitalWrite(LED_BUILTIN, LOW);
    }
  }
}

//============================

void processData() {

  // processes the data that is in dataRecvd[]
  if (allReceived) {
    if (dataRecvCount == 3) {
      for (byte n = 0; n < dataRecvCount; n++) {
        byte x = dataRecvd[n];
        analogWrite(outputPins[n], x);
      }
    } else {
      blinkLED(10);
    }
    allReceived = false;
  }
}

//============================

void decodeHighBytes() {

  //  copies to dataRecvd[] only the data bytes i.e. excluding the marker bytes and the count byte
  //  and converts any bytes of 253 etc into the intended numbers
  //  Note that bytesRecvd is the total of all the bytes including the markers
  dataRecvCount = 0;
  for (byte n = 2; n < bytesRecvd - 1 ; n++) { // 2 skips the start marker and the count byte, -1 omits the end marker
    byte x = tempBuffer[n];
    if (x == specialByte) {
      // debugToPC("FoundSpecialByte");
      n++;
      x = x + tempBuffer[n];
    }
    dataRecvd[dataRecvCount] = x;
    dataRecvCount ++;
  }
}

void blinkLED(byte numBlinks) {
  for (byte n = 0; n < numBlinks; n ++) {
    digitalWrite(13, HIGH);
    delay(30);
    digitalWrite(13, LOW);
    delay(30);
  }
}
