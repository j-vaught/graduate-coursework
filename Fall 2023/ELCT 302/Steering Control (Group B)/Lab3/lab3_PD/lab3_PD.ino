#include <Servo.h>

Servo myservo;  // create servo object to control a servo

// Constants for servo control
const int servoPin = 3;
const int ledPin = 13;  // Onboard LED pin

// PID controller constants
const double Kp = 20.0;
const double Ki = 0;   // Integral constant, adjust as necessary
const double Kd = -5;

// Variables for PID controller
double positionError = 0;
double lastPositionError = 0;
double integral = 0;
double derivative = 0;
double correction = 0;

// Sensor pins
const int sensorLeft = A1;
const int sensorRight = A2;

// Sensor value storage for derivative calculation
int lastSensorValueLeft = 0;
int lastSensorValueRight = 0;

// Turn detection variables
double rateOfChange = 0;
const double turnThreshold = 20;  // Threshold for detecting a turn, adjust based on testing

void setup() {
  myservo.attach(servoPin);  // attaches the servo on servoPin to the servo object

  pinMode(sensorLeft, INPUT);
  pinMode(sensorRight, INPUT);
  pinMode(ledPin, OUTPUT);  // Set the LED pin as an output
  Serial.begin(9600);
}

void loop() {
  int sensorValueLeft = analogRead(sensorLeft);
  int sensorValueRight = analogRead(sensorRight);

  positionError = sensorValueLeft - sensorValueRight;

  // PID control algorithm
  derivative = (sensorValueLeft - lastSensorValueLeft) - (sensorValueRight - lastSensorValueRight);
  correction = Kp * positionError + Ki * integral + Kd * derivative;

  // Apply the correction to the servo
  long servoValue = 1500 + correction/50;
  servoValue = constrain(servoValue, 1000, 2000);
  myservo.writeMicroseconds(servoValue);

  // Debug output
  Serial.print("Left Sensor: ");
  Serial.print(sensorValueLeft);
  Serial.print(", Right Sensor: ");
  Serial.print(sensorValueRight);
  Serial.print(", Servo Output: ");
  Serial.println(servoValue);

  // Update last values for next loop iteration
  lastPositionError = positionError;
  lastSensorValueLeft = sensorValueLeft;
  lastSensorValueRight = sensorValueRight;

  delay(5); // Delay in milliseconds, adjust as needed
}
