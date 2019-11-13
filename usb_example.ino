// This file shows an example of communicating from Python to Arduino over USB
// Build an LED circuit powered from the 7 pin to see this work. Run Arduino program and then Python program.

void setup() {
  Serial.begin(9600);
  pinMode(7, OUTPUT);
}

void loop() {
  if(Serial.available() > 0) {
    char data = Serial.read();
    int volt = data;

    // Literally just read data from serial monitor and check if it's 0 or 1.
    // The trick is sending bytes from Python rather than strings. See the companion .py script for more
    if (volt == 0) {
      digitalWrite(7, LOW);
    } else {
      digitalWrite(7, HIGH);
    }
  }
}
