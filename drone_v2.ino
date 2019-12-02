// digital pins
int ON = 4;
int FLIP = 12;
int SPEED = 7;

// analog pins
int LJUD = 3;
int RJLJ = 9;
int RJUD = 10;


boolean paired = false;
boolean flying = false;
boolean propellersOn = false;
int byteArray[4];
int bytesReceived;

void setup() {
  pinMode(ON, OUTPUT);
  pinMode(LJUD, OUTPUT);
  pinMode(FLIP, OUTPUT);
  pinMode(SPEED, OUTPUT);

  // Write high to the digital buttons, as that should be their default state
  digitalWrite(FLIP, HIGH);
  digitalWrite(SPEED, HIGH);
  digitalWrite(ON, HIGH);
  
  Serial.begin(9600);
}

void loop() {

  // Declare an array of length 4 to hold the numbers we get from Python,
  // and a counter so we can tell how many bytes we have received
  int byteArray[4];
  int bytesReceived = 0;

  // Keep trying to receive bytes until we get them all
  while (bytesReceived < 4) {
    if (Serial.available() > 0) {
      int pythonByte = Serial.read();
      byteArray[bytesReceived] = pythonByte;
      bytesReceived++;
    }
  }

  // If the "misc" byte is 15, run the takeoff function and set flying to true
  if (byteArray[3] == 15) {
    start();
    flying = true;
  } else if (byteArray[3] == 16) {
    stabilize(LJUD, RJLJ, RJUD);
  // If we didn't receive a special command, just write whatever Python gives us
  } else {
    analogWrite(RJLJ, byteArray[0]);
    analogWrite(RJUD, byteArray[1]);
    analogWrite(LJUD, byteArray[2]);
  }
  
}

void pair() {
  // Pair function. If not already paired, set the U/D stick all the way up and then all the way down, with some delays between
  // Also, set the paired variable
  if (!paired) {
    analogWrite(LJUD, 255);
    delay(500);
    analogWrite(LJUD, 0);
    paired = true;
    delay(500);
  }
}

void start() {
  // Takeoff function. Set the U/D stick all the way up, and then press the takeoff button. delay a small bit and then set the U/D stick back to neutral.
  if (!propellersOn) {
    analogWrite(LJUD, 255);
    digitalWrite(ON, LOW);
    delay(200);
    digitalWrite(ON, HIGH);
    delay(200);
    analogWrite(LJUD, 128);
  }
}

// To stabilize, we simply set all the stick voltages to be in the middle.
void stabilize(int pin, int pin2, int pin3) {
  analogWrite(pin, 128);
  analogWrite(pin2, 128);
  analogWrite(pin3, 128);
}
