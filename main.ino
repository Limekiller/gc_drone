// digital pins
int ON = 6;

// analog pins
int PAIR = A5;
int LJUD = A4;

boolean paired = false;
boolean flying = false;
boolean propellersOn = false;

void setup() {
  pinMode(ON, OUTPUT);
  pinMode(LJUD, OUTPUT);
  pinMode(PAIR, OUTPUT);
  Serial.begin(9600);
  digitalWrite(ON, HIGH);
}

void loop() {
  //pair();
  if (Serial.available() > 0) {
    int volt = Serial.read();
    if (volt == 1) {
      start();
      flying = true;
    }
    else if (volt == 2) {
      analogWrite(LJUD, 135);
    }
    else if (volt == 3) {
      analogWrite(LJUD, 100);
      delay(2);
    } else {
      stabilize(LJUD);
    }
  }
  //start();  
}

void pair() {
  if (!paired) {
    analogWrite(PAIR, 255);
    delay(1);
    analogWrite(PAIR, 0);
    paired = true;
    delay(100);
    pinMode(PAIR, INPUT);
  }
}

void start() {
  if (!propellersOn) {
    digitalWrite(ON, LOW);
    delay(200);
    //propellersOn = true;
    delay(200);
    digitalWrite(ON, HIGH);
    delay(200);
  }
}

void stabilize(int pin) {
  analogWrite(pin, 127);
  delay(2);
  analogWrite(pin, 128);
  delay(2);
}
