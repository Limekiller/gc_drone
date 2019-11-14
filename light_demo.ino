// This file shows an example of communicating from Python to Arduino over USB
// Build an LED circuit powered from the 7 pin to see this work. Run Arduino program and then Python program.

void setup() {
  Serial.begin(9600);
  pinMode(7, OUTPUT);
  pinMode(6, OUTPUT);
}

void loop() {
  if(Serial.available() > 0) {
    char volt = Serial.read();
    
    // Literally just read data from serial monitor and check if it's 0 or 1.
    // The trick is sending bytes from Python rather than strings. See the companion .py script for more
    if (volt == 0) {
      digitalWrite(6, LOW);
      digitalWrite(7, LOW);
    } else if (volt == 1) {
      digitalWrite(6, LOW);
      digitalWrite(7, HIGH);
    } else if (volt == 2) {
      digitalWrite(6, HIGH);
      digitalWrite(7, LOW);
    } else {
      digitalWrite(6, HIGH);
      digitalWrite(7, HIGH);
    }
  }
}
