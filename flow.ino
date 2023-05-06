#include "Bitcraze_PMW3901.h"
#include <math.h>

// Using digital pin 10 for chip select
Bitcraze_PMW3901 flow(10);

void setup() {
  Serial.begin(9600);

  if (!flow.begin()) {
    Serial.println("Initialization of the flow sensor failed");
    while(1) { }
  }
}

int16_t deltaX,deltaY;
int16_t x,y =0;
int16_t xb,yb =0;//previous x and y values
int16_t distance;

void loop() {
  // Get motion count since last call
  flow.readMotionCount(&deltaX, &deltaY);

  x = x+deltaX;
  y = y+deltaY;
  distance = sqrt(pow(x - xb, 2) + pow(y - yb, 2));

  Serial.print(x);        // Send value1 to the serial port
  Serial.print(",");
  Serial.print(y);      // Send value2 to the serial port
  Serial.print(",");
  Serial.print(deltaX);        // Send value1 to the serial port
  Serial.print(",");
  Serial.print(deltaY);      // Send value2 to the serial port
  Serial.print(",");
  Serial.println(distance);      // Send value3 to the serial port
  xb=deltaX;
  yb=deltaY;
  delay(100);
}
