// store pin numbers
int BUTTON = 1;
int ON = A3;
int LJUD = A2;
boolean paired = false;
boolean flying = false;

void setup() {
  pinMode(2, INPUT);
  pinMode(3, INPUT);
  Serial.begin(9600);
}

void loop() {
  Serial.println(digitalRead(2));
  if (digitalRead(2) == 1) {
    sequence();
    flying = true;
  } else if (digitalRead(3) == 1) {
    pair();
  } else if (paired && flying) {
    flying = false;
    analogWrite(LJUD, 100);
    delay(5000);
    analogWrite(LJUD, 0);
  }
}

void pair() {
  analogWrite(LJUD, 255);
  delay(100);
  analogWrite(LJUD, 100); 
  delay(100);
  paired = true;
}

void sequence() {    
  analogWrite(ON, 0);
  analogWrite(LJUD, 150);
  delay(1200);
  analogWrite(LJUD, 100);
  delay(1200);
}
