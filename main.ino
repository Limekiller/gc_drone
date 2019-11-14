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
}

void loop() {
  pair();
  start();  
  stabilize(LJUD);
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
    analogWrite(LJUD, 135);
    digitalWrite(ON, LOW);
    propellersOn = true;
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
