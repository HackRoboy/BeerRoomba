#include <Servo.h> 

Servo myservo;
int servoPin = 9;
int feedbackPin = 8;


void setup() {
  pinMode(feedbackPin, INPUT);
  pinMode(servoPin, OUTPUT);
  pinMode(3, OUTPUT);
  analogWrite(3, 200);
  Serial.begin(115200);
  //myservo.attach(servoPin);
  Serial.println("setup");
}

char msg[128];
char buf[64];
String val;
int angle;
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

void loop() { 
  int currentAngle = readFeedback(feedbackPin);
  diff = (currentAngle - angle + 180) % 360 - 180;
  diff = diff < -180 ? diff + 360 : diff;
  
  if (Serial.available()) {
    Serial.println("read");
    byte count = Serial.readBytesUntil('\n', buf, 64);
    buf[count] = '\0';
    Serial.println("read done");
    Serial.write(buf);
    val = String(buf);
    angle = val.toInt();
    sprintf(msg, "val: %d\n", angle);
    Serial.write(msg);
    angle = angle % 360;

    diff = (currentAngle - angle + 180) % 360 - 180;
    diff = diff < -180 ? diff + 360 : diff;

    if (abs(diff) < 2) {
      direction = 0;
    } else {
      if (diff > 0) {
        direction = 1;
      } else if (diff < 0) {
        direction = -1;
      }
    }
    sprintf(msg, "diff: %d, currentAngle: %d\n", diff, currentAngle);
    Serial.write(msg);

  }

  // direction
  int speed = 10;
  if (abs(diff) < 5) {
    direction = 0;
  } else if (abs(diff) < 20) {
    speed = 0;
  } else {
    speed = 5;
  }

  if (direction == 1) {
    analogWrite(servoPin, 181 - speed);
    delay(20);
  } else if (direction == -1) {
    analogWrite(servoPin, 195 + speed);
    delay(20);
  } else {
    analogWrite(servoPin, 190);
  }

 
}
