// digital pins
int ON = 4;
int FLIP = 12;

// analog pins
int PAIR = A5;
int LJUD = 3;
int RJLJ = 9;
int RJUD = 10;

boolean paired = false;
boolean flying = false;
boolean propellersOn = false;

void setup() {
  pinMode(ON, OUTPUT);
  pinMode(LJUD, OUTPUT);
  pinMode(PAIR, OUTPUT);
  pinMode(FLIP, OUTPUT);
  digitalWrite(FLIP, HIGH);
  Serial.begin(9600);
  digitalWrite(ON, HIGH);
  //analogWrite(LJUD, 255);
}

void loop() {
  //pair();  
  digitalWrite(FLIP, HIGH);
  if (Serial.available() > 0) {
    int str_commands = Serial.read();

    int direction = str_commands % 10;
    float difference = direction * 0.1;
    int velocity = (int) (str_commands / 10) - difference;
    int proper_velocity = ((velocity -10) * 12);
    
    if (direction == 1) {
      start();
      flying = true;
    }
    else if (direction == 2) {
      int magnitude = proper_velocity + 128;
      
      analogWrite(LJUD, magnitude);
      analogWrite(RJLJ, 128);
      analogWrite(RJUD, 128);
    }
    else if (direction == 3) {
      int magnitude =  0 + proper_velocity;
      
      analogWrite(LJUD, 0);
      analogWrite(RJLJ, 128);
      analogWrite(RJUD, 128);
      //delay(4);
    } else if (direction == 4) {
      int magnitude = proper_velocity + 128;

      analogWrite(RJLJ, magnitude); 
      analogWrite(LJUD, 128);
      analogWrite(RJUD, 128);
    } else if (direction == 5) {
      int magnitude =  128 - proper_velocity;

      analogWrite(RJLJ, magnitude);
      analogWrite(LJUD, 128);
      analogWrite(RJUD, 128);
      } else if (direction == 6) {
      int magnitude = proper_velocity + 128;

      analogWrite(RJUD, magnitude);
      analogWrite(RJLJ, 128);
      analogWrite(LJUD, 128);
    } else if (direction == 7) {
      int magnitude = 128 - proper_velocity;

      analogWrite(RJUD, magnitude);
      analogWrite(RJLJ, 128);
      analogWrite(LJUD, 128);
    } else if (direction == 8) {
        digitalWrite(FLIP, LOW);
        delay(200);
    } else {
      stabilize(LJUD, RJLJ, RJUD);
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

void stabilize(int pin, int pin2, int pin3) {
  analogWrite(pin, 128);
  analogWrite(pin2, 128);
  analogWrite(pin3, 128);
//  analogWrite(pin2, 128);
//  delay(75);
//  analogWrite(pin, 127);
//  analogWrite(pin2, 128);
//  delay(2);
}
