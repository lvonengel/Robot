#include <Servo.h>

Servo servopinky;
Servo servoring;
Servo servomiddle;
Servo servoindex;
Servo servothumb;
// Servo servowrist;


void setup() {
  // match Python baudrate
  Serial.begin(9600);

  servopinky.attach(2);
  servoring.attach(3);
  servomiddle.attach(4);
  servoindex.attach(5);
  servothumb.attach(6);
  // servoWrist.attach(7)

    Serial.println("Hand tracking ready. Waiting for binary finger states")
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    // "000000" to "111111"
    if (input.length() != 6) {
      Serial.println("Invalid input length. Expected 6 binary digits.");
      return;
    }

    // get each finger
    // Order: Wrist, Index, Middle, Ring, Thumb, Pinky
    bool wrist = (input.charAt(0) == '1');
    bool index = (input.charAt(1) == '1');
    bool middle = (input.charAt(2) == '1');
    bool ring = (input.charAt(3) == '1');
    bool thumb = (input.charAt(4) == '1');
    bool pinky = (input.charAt(5) == '1');

    // moves servos based on finger states
    // closed = 180 (which is finger down), open (which is finger up) = 0
    servoindex.write(index ? 180 : 0);
    servomiddle.write(middle ? 180 : 0);
    servoring.write(ring ? 180 : 0);
    servothumb.write(thumb ? 180 : 0);
    servopinky.write(pinky ? 180 : 0);

    // degbugging
    // Serial.print(" I:");
    // Serial.print(index);
    // Serial.print(" M:");
    // Serial.print(middle);
    // Serial.print(" R:");
    // Serial.print(ring);
    // Serial.print(" T:");
    // Serial.print(thumb);
    // Serial.print(" P:");
    // Serial.println(pinky);
  }
}