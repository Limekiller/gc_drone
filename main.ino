// digital pins
int ON = 4;
int FLIP = 12;
int SPEED = 7;

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
  pinMode(SPEED, OUTPUT);

  // Write high to the digital buttons, as that should be their default state
  digitalWrite(FLIP, HIGH);
  digitalWrite(SPEED, HIGH);
  digitalWrite(ON, HIGH);
  
  Serial.begin(9600);
}

void loop() {
  // If there are serial commands available,
  if (Serial.available() > 0) {
    // Read those commands
    int str_commands = Serial.read();

    // If you've read the leap.py file, you'd know we send our commands as velocity concatenated with direction, such as 152 --
    // Velocity 15 (5) and direction 2 (up). Arduino has no way to split up integers so we use math.
    
    // Get the ones place (direction) by taking the number mod 10
    int direction = str_commands % 10;

    // Get the first two digits by dividing by 10 and then subtracting what's left in the 0.1s place.
    float difference = direction * 0.1;
    int velocity = (int) (str_commands / 10) - difference;

    // Get the ACTUAL voltage level we want by subtracting 10 and multiplying by 12 (remember, max is 20, and 20*12 is 240. Not quite 255 but pretty close).
    int proper_velocity = ((velocity -10) * 12);

    // Determine what to do based on direction
    // For each of these, if we're moving in a positive direction, we take 128 (the half-way point) and add the velocity voltage to it to get our speed.
    // If we're moving in a negative direction, we take 128 - our velocity. Then we always set the other two axes to be in the middle, so we only move one axis at a time.
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
        digitalWrite(SPEED, LOW);
        delay(200);
        digitalWrite(FLIP, HIGH);
        digitalWrite(SPEED, HIGH);
    } else {
      stabilize(LJUD, RJLJ, RJUD);
    }
  }
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

// To take off, we write low and then high to the take off button, with delays
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

// To stabilize, we simply set all the stick voltages to be in the middle.
void stabilize(int pin, int pin2, int pin3) {
  analogWrite(pin, 128);
  analogWrite(pin2, 128);
  analogWrite(pin3, 128);
}
