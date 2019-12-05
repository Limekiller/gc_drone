// digital pins
int ON = 4;
int FLIP = 12;
int SPEED = 7;
int PAIR = 6;
int POWER = 13;

// analog pins
int LJUD = 3;
int LJRL = 5;
int RJLJ = 9;
int RJUD = 10;

boolean paired = false;
int byteArray[5];
int bytesReceived;

void setup() {
  pinMode(ON, OUTPUT);
  pinMode(LJUD, OUTPUT);
  pinMode(FLIP, OUTPUT);
  pinMode(SPEED, OUTPUT);
  pinMode(LJRL, OUTPUT);
  pinMode(PAIR, INPUT);
  pinMode(POWER, OUTPUT);

  // Write high to the digital buttons, as that should be their default state
  digitalWrite(FLIP, HIGH);
  digitalWrite(SPEED, HIGH);
  digitalWrite(ON, HIGH);
  digitalWrite(POWER, HIGH);
  
  Serial.begin(9600);
  pair();
}

void loop() {

  // Declare an array of length 5 to hold the numbers we get from Python,
  // and a counter so we can tell how many bytes we have received
  int byteArray[5];
  int bytesReceived = 0;

  // Keep trying to receive bytes until we get them all
  while (bytesReceived < 5) {
    if (Serial.available() > 0) {
      int pythonByte = Serial.read();
      byteArray[bytesReceived] = pythonByte;
      bytesReceived++;
    }
  }

  // If the "misc" byte is 15, run the takeoff function and set flying to true
  if (byteArray[4] == 15) {
    start();
  }
  // If the "misc" byte is 16, that's the land command, so we activate the landing button.
  else if (byteArray[4] == 16) {
    analogWrite(RJLJ, byteArray[0]);
    analogWrite(RJUD, byteArray[1]);
    analogWrite(LJUD, byteArray[2]);
    analogWrite(LJRL, byteArray[3]);
    
    digitalWrite(ON, LOW);
    delay(200);
    digitalWrite(ON, HIGH);
    delay(200);
  }
  // If we didn't receive a special command, just write whatever Python gives us
  else {
    analogWrite(RJLJ, byteArray[0]);
    analogWrite(RJUD, byteArray[1]);
    analogWrite(LJUD, byteArray[2]);
    analogWrite(LJRL, byteArray[3]);
  }
  
}

void pair() {
  // This function automatically pairs the transmitter to the drone for us.
  // We write 255 to the analog stick, delay, and then write 0. This is the pairing motion.
  if (!paired) {
    pinMode(PAIR, OUTPUT);
    analogWrite(PAIR, 255);
    
    delay(500);
    
    analogWrite(PAIR, 0);
    paired = true;
    delay(500);
    pinMode(PAIR, INPUT);
  }
}

void start() {
  // Takeoff function. Set the U/D stick all the way up, and then press the takeoff button. delay a small bit and then set the U/D stick back to neutral.
    analogWrite(LJUD, 255);
    digitalWrite(ON, LOW);
    delay(200);
    digitalWrite(ON, HIGH);
    delay(200);
    analogWrite(LJUD, 128);
    
}
