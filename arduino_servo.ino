#include <Servo.h>

Servo servo[2];
int button[] = {7, 6};
int echo = 13;
int trig = 12;
int prevDist = -1;

int angle[2];

int id = 0;
boolean pillsTaken = true;
int startTime;

void setup() {
  Serial.begin(9600);
  servo[0].attach(9);
  servo[1].attach(10);
  
  for(int i = 0; i < 2; i++) {
    pinMode(button[i], INPUT);
    servo[i].write(0);
    angle[i] = 0;
  }

  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);

  digitalWrite(trig, LOW);

  delayMicroseconds(2);
}

void loop() {

  //while(!Serial.available());
  if(Serial.available()) {
    int value = Serial.read() - 48;
  
    int numPills = value <= 3 ? value: value - 4;
    id = value <= 3 ? 0 : 1;
    
    angle[id] += numPills*60;
    
    if(angle[id] > 180) {
      angle[id] = 180;
    }
  
    servo[id].write(angle[id]);
    
    pillsTaken = false;
    startTime = millis();
  }
  
  
  //Serial.println(getDistance());
  if(!pillsTaken && millis() - startTime > 500 && getDistance() > 10) {
    pillsTaken = true;
    
    for(int  i = 0; i < 3; i++) {
      if(getDistance() < 10) {
        pillsTaken = false;
      }
    }
    
    if(pillsTaken) {
      Serial.print(id);
    }
    //pillsTaken = true;
  }
  
  //blue guy
  if(buttonPressed(0)) {
    servo[0].write(0);
    angle[0] = 0;
    //pillsTaken = false;
  }
  
  //black servo
  if(buttonPressed(1)) {
    servo[1].write(0);
    angle[1] = 0;
    //pillsTaken = false;
  }
}

bool buttonPressed(int index) {
  static int previous[] = {0, 0};
  int current = digitalRead(button[index]);
  
  if(previous[index] == 1 && current == 0) {
    previous[index] = current;
    return true;
  }
  
  previous[index] = current;
  return false;
}

int getDistance() {
  int returnTime;
  int distance;
  
  
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);

  returnTime = pulseIn(echo, HIGH);

  //Distance in cm
  return returnTime*0.0343/2;
}
