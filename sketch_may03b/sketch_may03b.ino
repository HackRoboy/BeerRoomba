#include <Servo.h> 

Servo servo;
int servoPin[2] = {10,11};
int feedbackPin = 9;


void setup() {
  pinMode(feedbackPin, INPUT);
  pinMode(servoPin[0], OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(2, OUTPUT);
  digitalWrite(2,HIGH);
  analogWrite(3, 200);
  Serial.begin(500000);
  servo.attach(servoPin[1]);
  Serial.println("setup");
}

char msg[128];
char buf[64];
String val;
int angle = 15;
int diff;
int direction;
long dutyScale = 1000;
long unitsFC = 360;
long dcMin = 29;
long dcMax = 971;
long q2min = unitsFC / 4;
long q3max = q2min * 3;

int readFeedback(int pin) {
  long tHigh, tLow, tCycle, turns;
  while (1) {
    tHigh = pulseIn(pin, HIGH);
    tLow = pulseIn(pin, LOW);
    tCycle = tHigh + tLow;
    if (tLow == 0) 
      continue;
    if ((tCycle > 1000) && (tCycle < 1200))
      break;
  }
  long dc = (dutyScale * tHigh) / tCycle;
  long theta = (unitsFC - 1) - ((dc - dcMin) * unitsFC) / (dcMax - dcMin + 1);
  if (theta < 0) {
    sprintf(msg, "error: tHigh=%ld tLow=%ld tCycle=%ld dc=%ld theta=%ld", tHigh, tLow, tCycle, dc, theta);
    Serial.println(msg);
  }
  return theta;
}

int i=0;
int rot_angle =0;

void loop() { 
  int currentAngle = readFeedback(feedbackPin);
  diff = (currentAngle - angle + 180) % 360 - 180;
  diff = diff < -180 ? diff + 360 : diff;
  
  if (Serial.available()) {
    Serial.println("read");
    byte count = Serial.readBytesUntil('\n', buf, 64);
    if(count>0){
      Serial.println((int)buf[0]);
      if(buf[0]==48)
      {
        Serial.write(&(buf[2]));
        buf[count] = '\0';
        val = String(&(buf[2]));
        angle = val.toInt();
        angle = angle % 360;
        sprintf(msg, "rot0: %d\n", angle);
        Serial.write(msg);
      }
      if(buf[0]==49)
      {
        Serial.write(&(buf[2]));
        buf[count] = '\0';
        val = String(&(buf[2]));
        rot_angle = val.toInt();
        sprintf(msg, "rot1: %d\n", rot_angle);
        Serial.write(msg);
      }
      if(buf[0]==50)
        digitalWrite(2,HIGH);
      if(buf[0]==51)
        digitalWrite(2,LOW);
    }
  }

//  static bool dir = false;
//  static bool dir2 = false;
//  if(!dir)
//    angle+=10;
//  else 
//    angle-=10;
//  if(angle>345){
//    dir = !dir;
//    angle = 345;
//  }
//  if(angle<15){
//    dir = !dir;
//    angle = 15;
//  }
//  if(i%10==0){
//    if(!dir2)
//      rot_angle++;
//    else
//      rot_angle--;
//    if(rot_angle>180){
//      rot_angle = 180;
//      dir2 = !dir2;
//    }
//    if(rot_angle<0){
//      rot_angle = 0;
//      dir2 = !dir2;
//    }
//    servo.write(rot_angle%180);
//  }
  

  if (abs(diff) < 2) {
    direction = 0;
  } else {
    if (diff > 0 && currentAngle<angle) {
      direction = -1;
    }else if(diff > 0 && currentAngle>angle){
      direction = 1;
    }else if (diff < 0  && currentAngle>angle) {
      direction = 1;
    }else if (diff < 0  && currentAngle<angle) {
      direction = -1;
    }
  }
  
  i++;
  if(i%1000==0){
    sprintf(msg, "diff: %d, currentAngle: %d\n", diff, currentAngle);
    Serial.write(msg);
  }
  // direction
  int speed = 20;
  if (abs(diff) < 5) {
    direction = 0;
  } else if (abs(diff) < 20) {
    speed = 0;
  } else {
    speed = 15;
  }

  if (direction == 1) {
    analogWrite(servoPin[0], 181 - speed);
    delay(20);
  } else if (direction == -1) {
    analogWrite(servoPin[0], 195 + speed);
    delay(20);
  } else {
    analogWrite(servoPin[0], 190);
  }

//  servo.write(0);      // Turn SG90 servo Left to 45 degrees
//  delay(1000);          // Wait 1 second
//  servo.write(180);      // Turn SG90 servo back to 90 degrees (center position)
//  delay(1000);
}
