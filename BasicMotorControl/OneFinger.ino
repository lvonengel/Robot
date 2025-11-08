#include <Servo.h>

Servo servoindex;

void setup() { 
  // starts baud rate and initiates servo to PWM GPIO
  Serial.begin(115200);
  servoindex.attach(7);
} 

void loop() {
  
  // handles user input in serial monitor
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    // handles input for a specifict turn angle
    if (input.startsWith("turn")) {
      int angle = input.substring(7).toInt();
      
      if (angle >= 0 && angle <= 180) {
        servoindex.write(angle);
        Serial.print("Turning to ");
        Serial.println(angle);
      } else {
        Serial.println("Please enter a value between 0 and 180.");
      }
    } 
    // handles finger to be fully at rest
    else if (input.equalsIgnoreCase("r")) {
      alltorest();
      Serial.println("Moved to rest at 0");
    } 
    // handles finger to be at 90 degrees (middle)
    else if (input.equalsIgnoreCase("mid")) {
      alltomiddle();
      Serial.println("Moved to middle at 90");
    } 
    // handles finger to be fully bent (max)
    else if (input.equalsIgnoreCase("m")) {
      alltomax();
      Serial.println("Moved to max at 180");
    }
    else {
      Serial.println("Unknown command. Commands: turn x, r, mid, or m");
    }
  }
}

// Motion helper functions
void alltomiddle() {
  servoindex.write(90);
}
void alltorest() { 
  servoindex.write(0);
}
void alltomax(){
  servoindex.write(180);
}
