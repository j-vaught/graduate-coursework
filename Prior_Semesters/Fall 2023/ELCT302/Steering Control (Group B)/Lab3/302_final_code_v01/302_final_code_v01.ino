// Initialization of the button pins
const int greenButtonPin = 11; // Green button connected to digital pin 2
const int yellowButtonPin = 12; // Yellow button connected to digital pin 3
const int redButtonPin = 8; // Red button connected to digital pin 4

const int servoPin = 5;


double Kp = 22.2, Ki = 0.0, Kd = -2.0;//change from 20 to 21[if car is juttery aroudn corners, increase KD and decrease KP]
//try 30, 0.001, -2.6 for higher speed.s(22.2)

//55 speed= Kp = 15.0, Ki = 0.0001, Kd = -1.3;

double positionError = 0, lastPositionError = 0, integral = 0, derivative = 0, correction = 0;
const int sensorLeft = A3, sensorRight = A2;
const int center=80; //if car isnt centered correctly. Added this
int lastSensorValueLeft = 0, lastSensorValueRight = 0;
const double turnThreshold = 175;
const int zeroPos = 1450; // Slightly right turning at 1500

bool isHandlingHardTurn = false; // New flag

unsigned long turnDetectionStartTime = 0;
unsigned long lastTurnTime = 0;
const unsigned long turnDetectionDelay = 200; // Delay after turn detection in milliseconds

int red = 3;
int yellow = 7;
int green = 4;

const int motorSpeed1=55;//low speed
const int motorSpeed2=58;//low speed

const int motorPinA = 9;
const int motorPinB = 10;
const int bumperPin = 6; // Button pin

unsigned long lastServoUpdate = 0;
const int servoUpdateInterval = 20000; // 20 ms interval for servo update
int servoPulseWidth = zeroPos; // Initial pulse width in microseconds

bool inSteeringMode = false;
bool inWaitingMode = false;
bool inDrivingMode = false;

int sensorValueLeft =0;
int sensorValueRight=0;

void setup() {
  // Initialize the button pins as inputs
  pinMode(greenButtonPin, INPUT);
  pinMode(yellowButtonPin, INPUT);
  pinMode(redButtonPin, INPUT);

  pinMode(sensorLeft, INPUT); // Set sensor left as input
  pinMode(sensorRight, INPUT); // Set sensor right as input
  //Serial.begin(9600);
  pinMode(red, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(yellow, OUTPUT);
  pinMode(motorPinA, OUTPUT); // Set motor pin A as output
  pinMode(motorPinB, OUTPUT); // Set motor pin B as output
  pinMode(bumperPin, INPUT_PULLUP); // Initialize button pin as input with pull-up[NEED TO CHANGE TO NOT BE PULL_UP]
  digitalWrite(motorPinA, HIGH); // Initialize motor pin A
  digitalWrite(motorPinB, HIGH); // Initialize motor pin B

  TCCR1A = 0b11110010; // Timer/Counter Control Registers setup
  TCCR1B = 0b00010001;
  ICR1 = 320; // Input Capture Register
  TCNT1 = 0x0000; // Timer/Counter1 Register
  OCR1A = 0; // Turn off motor A
  OCR1B = 0; // Turn off motor B

  pinMode(servoPin, OUTPUT); // Set servo pin as output
}

void loop() {
  checkButtonPress();
  handleIRCommands();
  if (inSteeringMode || inWaitingMode) {
    readAndProcessSensors();
    updateServoPosition();

    if (inSteeringMode) {
      adjustMotorSpeedsBasedOnPID(); // Adjust motor speeds based on PID correction
      detectAndHandleTurn();
    }
    // Serial.print(servoPulseWidth);
    // Serial.print(", ");
    // Serial.print(sensorValueLeft);
    // Serial.print(", ");
    // Serial.println(sensorValueRight);
  }
}

void adjustMotorSpeedsBasedOnPID() {
  if (isHandlingHardTurn) { // Only adjust if in the middle of a hard turn
    // Adjust motor speeds based on correction
    if (correction / 50 > 150) {
      OCR1A = motorSpeed1 - 15; // Slow down left motor for right turn
      OCR1B = motorSpeed2;      // Keep right motor speed constant
        digitalWrite(yellow, HIGH);
    } else if (correction / 50 < -150) {
      OCR1A = motorSpeed1;      // Keep left motor speed constant
      OCR1B = motorSpeed2 - 15;  // Slow down right motor for left turn
        digitalWrite(yellow, HIGH);
    } else {
      OCR1A = motorSpeed1;      // Keep both motors at original speed for straight line
      OCR1B = motorSpeed2;
        digitalWrite(yellow, LOW);
    }
  }
}

void detectAndHandleTurn() {
  //Kd=-1.9;Kp=24;//LOOK AT THIS BEFORE UPLOADING<---------------------------------------------------------------------------
  bool isTurnDetected = abs(center + sensorValueLeft - sensorValueRight) > turnThreshold;

  if (isTurnDetected) {
    lastTurnTime = millis();
    if (turnDetectionStartTime == 0) {
      turnDetectionStartTime = millis();
    }

    if (millis() - turnDetectionStartTime > 30) {
      handleTurnDetection();
      isHandlingHardTurn = true; // Set flag when handling hard turn
    }
  } else {
    if (turnDetectionStartTime != 0 && millis() - lastTurnTime > turnDetectionDelay) {
      digitalWrite(red, LOW);
      OCR1A = motorSpeed1 + 15;
      OCR1B = motorSpeed2 + 15;
      turnDetectionStartTime = 0;
      //Kd=3;Kp=10;
      isHandlingHardTurn = false; // Reset flag when turn is over
    }
  }
}


void handleTurnDetection() {
  // Turn on Red LED to indicate a turn
  digitalWrite(red, HIGH);
    OCR1A = motorSpeed1; // Set motor speed left
  OCR1B = motorSpeed2; // Set motor speed right
  // Additional logic for turn handling can be added here
}

void checkButtonPress() {
  if (digitalRead(bumperPin) == HIGH) { // Check if button is pressed
    handleRedButton();
  }
}

void handleIRCommands() {
    // Check if the red button is pressed
  if (digitalRead(redButtonPin) == HIGH) {
    handleRedButton();
  }
  // Check if the green button is pressed
  if (digitalRead(greenButtonPin) == HIGH) {
    handleGreenButton();
  }
  // Check if the yellow button is pressed
  if (digitalRead(yellowButtonPin) == HIGH) {
    handleYellowButton();
  }

}

void readAndProcessSensors() {
  sensorValueLeft = analogRead(sensorLeft);
  sensorValueRight = analogRead(sensorRight);

  if (sensorValueLeft <= 20 && sensorValueRight <= 20) {
    handleRedButton();  // Activate stop mode if both sensors read 0
  } else {
    calculatePID(sensorValueLeft, sensorValueRight);
    updateLastSensorValues(sensorValueLeft, sensorValueRight);
  }
}

void calculatePID(int sensorValueLeft, int sensorValueRight) {
  positionError = center + sensorValueLeft - sensorValueRight; // Calculate position error + what the code should aim for
  integral += positionError;  // Accumulate the integral (sum of errors)
  derivative = (sensorValueLeft - lastSensorValueLeft) - (sensorValueRight - lastSensorValueRight);  // Compute the derivative (rate of change of error)
  correction = Kp * positionError + Ki * integral + Kd * derivative;  // Calculate the PID correction
}




void updateServoPosition() {
  servoPulseWidth = zeroPos + correction / 50;
  servoPulseWidth = constrain(servoPulseWidth, 1000, 2000);
  if (micros() - lastServoUpdate >= servoUpdateInterval) {
    lastServoUpdate = micros();
    digitalWrite(servoPin, HIGH);
    delayMicroseconds(servoPulseWidth);
    digitalWrite(servoPin, LOW);
  }
}


void handleRedButton() {
  inSteeringMode = false;
  inWaitingMode = false;
  inDrivingMode = false;
  OCR1A = 0; // Turn off motors
  OCR1B = 0;
  setLEDStates(true, false, false);
}

void handleYellowButton() {
  inSteeringMode = false;
  inWaitingMode = true;
  inDrivingMode = false;
  setLEDStates(false, false, true);
}

void handleGreenButton() {
  inSteeringMode = true;
  inWaitingMode = false;
  OCR1A = motorSpeed1; // Set motor speed left
  OCR1B = motorSpeed2; // Set motor speed right
  integral = 0; // Reset integral component
  setLEDStates(false, true, false);
}

void updateLastSensorValues(int sensorValueLeft, int sensorValueRight) {
  lastPositionError = positionError;
  lastSensorValueLeft = sensorValueLeft;
  lastSensorValueRight = sensorValueRight;
}

void setLEDStates(bool redState, bool greenState, bool yellowState) {
  digitalWrite(red, redState);
  digitalWrite(green, greenState);
  digitalWrite(yellow, yellowState);
}
