#include <Servo.h>

Servo servopinky;
Servo servoring;
Servo servomiddle;
Servo servoindex;
Servo servothumb;
Servo servowrist;


void setup() { 
  Serial.begin(115200);

  servopinky.attach(2);   // finger 1
  servoring.attach(3);    // finger 2
  servomiddle.attach(4);  // finger 3
  servoindex.attach(5);   // finger 4
  servothumb.attach(6);   // finger 5
  servowrist.attach(7);   // wrist

  Serial.println("Commands ready. Example commands: 1r, 2m, 3mid.");
}

void loop() {

  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.length() == 0) return;

    // parses just the finger
    char fingerChar = input.charAt(0);

    if (fingerChar < '0' || fingerChar > '5') {
      Serial.println("Invalid finger. Use 0–5.");
      return;
    }

    // converts the char to int
    int finger = fingerChar - '0'; 

    // gets everything after the number
    String command = input.substring(1); 

    int angle = -1;
    if (command.equals("m"))       angle = 180;
    else if (command.equals("r"))  angle = 0;
    else if (command.equals("mid")) angle = 90;
    else {
      Serial.println("Invalid command. Use m, r, or mid");
      return;
    }

    // moves the correct servo
    moveFinger(finger, angle);

    Serial.print("Finger ");
    Serial.print(finger);
    Serial.print(" → ");
    Serial.println(angle);
  }
}

// helper to actually move finger
void moveFinger(int finger, int angle) {
  switch (finger) {
    case 1: servopinky.write(angle); break;
    case 2: servoring.write(angle); break;
    case 3: servomiddle.write(angle); break;
    case 4: servoindex.write(angle); break;
    case 5: servothumb.write(angle); break;
    case 0: servowrist.write(angle); break;
  }
}
