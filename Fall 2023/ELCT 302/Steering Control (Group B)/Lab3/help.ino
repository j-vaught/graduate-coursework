/* mbed Microcontroller Library
 * Copyright (c) 2019 ARM Limited
 * SPDX-License-Identifier: Apache-2.0
 */
/**
*   C Code to automate control to an electric vehicle utilizing a microcontroller.
*   Last Edit:  29 NOV 2023
*   ELCT302: Team 3
*   Subteam Steering:   Dylan Rogers, Ryan McCarvill, Kingkeo Simlamany
*   Subteam Driving:    Jarod Stefurak, Hunter Frady
*  
**/
/*************************************************/
// #includes //
#include "mbed.h"
#include <stdio.h>
#include <stdbool.h>
#include <iterator>
#include <type_traits>
#include <vector>
// end #includes //
/*************************************************/
/*************************************************/
// Defines
#define BLINKING_RATE 50ms // Blinking rate in milliseconds
#define CONTROL_UPDATE_RATE 20ms // Control rate in milliseconds
#define PWM_FREQ 50.0f // PWM output waveform period
#define T1 20ms     // 1KHz sample time
#define K_p 1.0f//0.8928f//0.7//2.0f//.8928f // proportional gain
#define K_i 0.0001473f
#define K_d 0.007f//0.00095f//0.0005f//0.000892f  // Intergal gain
/*************************************************/
// end Defines //
/*************************************************/
// Pinouts //
PwmOut test_pwm(PTC9);
PwmOut RMO(PTA1);
PwmOut LMO(PTA2);
InterruptIn stopButton(PTD4);
InterruptIn startButton(PTA4);
InterruptIn waitButton(PTA12);
AnalogIn battery(PTC1);
// AnalogIn R_Sensor(PTB0);
// AnalogIn L_Sensor(PTB1);
DigitalOut RED_LED(LED1);               // LED on Microcontroller to output Red
DigitalOut GREEN_LED(LED2);             // LED on Microcontroller to output Green
DigitalOut BLUE_LED(LED3);              // LED on Microcontroller to output Blue
// end Pinouts //
/*************************************************/
/*************************************************/
// Initialize Variables //
int isRunning;
float last_smoothed_feedback = 0;
bool batteryState= false;
bool inWait= false;
bool motorState= false;
float err_Previous = 0;
std::vector<float> data(8,0);
// end Initialize Variables //
/*************************************************/
/*************************************************/
// Functions //
/*  LED COLOR FUNCTIONS  */
void LED_OFF(void){RED_LED= 1; GREEN_LED= 1; BLUE_LED= 1;}  // end LED_OFF()
void Purple(void){BLUE_LED= 0; RED_LED= 0; GREEN_LED= 1;}   // end Purple()
void Red(void){RED_LED= 0; GREEN_LED= 1; BLUE_LED= 1;}      // end Red()
void Yellow(void){RED_LED= 0; GREEN_LED= 0; BLUE_LED= 1;}   // end Yellow()
void Green(void){GREEN_LED= 0; RED_LED= 1; BLUE_LED= 1;}    // end Green()
void Cyan(void){BLUE_LED= 0; GREEN_LED= 0; RED_LED= 1;}     // end Cyan()
void Blue(void){BLUE_LED= 0; RED_LED= 1; GREEN_LED= 1;}     // end Blue()
void White(void){BLUE_LED= 0; RED_LED= 0; GREEN_LED= 0;}    // end White()
/*  end LED COLOR FUNCTIONS  */
/*  STEERING FUNCTIONS  */
float radian2DutyCycle(float angle, float maximum_angle, float minimum_angle,
                       float maxium_duty_cycle, float minimum_duty_cycle) {
  float m = (maxium_duty_cycle - minimum_duty_cycle) /
            (maximum_angle - minimum_angle);
  if (angle > maximum_angle) {
    angle = maximum_angle;
  } else if (angle < minimum_angle) {
    angle = minimum_angle;
  } // end elseif
  return m * (angle - minimum_angle) + minimum_duty_cycle;
} // end float radian2DutyCycle

float derivApprox(float dT, float Y_two, float Y_one) {
  return (Y_two - Y_one) / dT;
} // end float derivApprox()

void steeringControl() {
    static AnalogIn R_Sensor(PTB0);
    static AnalogIn L_Sensor(PTB1);

    float current_feedback = L_Sensor.read() - R_Sensor.read();
    float alpha = 0.1; // Smoothing factor
    float smoothed_feedback = alpha * current_feedback + (1 - alpha) * last_smoothed_feedback;

    float err = 0 - smoothed_feedback;
    float err_Change = derivApprox(0.001, err, err_Previous);

    float Control_Action = K_p * err + K_d * err_Change;
    float Duty_Cycle = radian2DutyCycle(Control_Action, 0.75, -0.75, 0.098, 0.048);

    if (abs(test_pwm.read() - Duty_Cycle) > 0.005)
        test_pwm.write(Duty_Cycle);

    err_Previous = err;
    last_smoothed_feedback = smoothed_feedback;
}

/*  end STEERING FUNCTIONS  */
/*  INTERRUPT FUNCTIONS  */
// Read a voltage from the battery through a voltage divider
void batteryRead(void){
  if ((battery.read()*3.3)<2.0){
    batteryState= false;
    Purple();
  } // end if "Battery Low"
  if ((battery.read()*3.3)>2.0){
    batteryState= true;
  } // end if "Battery not low"
} // end void batteryRead
void setWait(void){
    inWait= true;
    RMO.write(0.0f);
    LMO.write(0.0f);
    Yellow();
    motorState= false;
} // end setWait()
void setStart(void){
    RMO.write(0.5f);
    LMO.write(0.5f);
    Green();
    motorState= true;
} // end setStart()
void setStop(void){
    RMO.write(0.0f);
    LMO.write(0.0f);
    Red();
    inWait= false;
    motorState= false;
} // end setStop()
/*  END INTERRUPT FUNCTIONS  */
// end Functions //
/*************************************************/
/*************************************************/
/* MAIN */
int main() {
// Set the period of the PWM Waveforms
  test_pwm.period(1 / PWM_FREQ);
  RMO.period_us(40);
  LMO.period_us(40);
// Setup an event queue to handle event requests for the ISR
  // and issue the callback in the control thread.
  EventQueue control_event_queue;
  // Setup a control thread to update the PWM signals
  Thread control_thread(osPriorityNormal);
  // Start the event on a loop ready to receive event calls from
  // the event queue
  control_thread.start(
      callback(&control_event_queue, &EventQueue::dispatch_forever));
  // Setup ticker to issue update requests
  Ticker control_ticker;
  // Attach update function to issue an event on the control thread
  // at a specified rate.
  control_ticker.attach(control_event_queue.event(&steeringControl),
                     CONTROL_UPDATE_RATE);
  // Read Button Inputs
  waitButton.rise(&setWait);
  LED_OFF();
// While loop for when the controller is in an `on` state
  while (true) {
    batteryRead(); // Read Battery to determine if enough voltage
    // while("Battery has enough voltage"
    while (batteryState== true){
    //steeringControl();
      if (waitButton){
        setWait(); // end if "Enter Wait state"
        startButton.rise(&setStart);
        stopButton.rise(&setStop);
      } // end if(inWait== true)
      else {
          inWait= false;
      } // end else(inWait==false)
    while(inWait== true){
        // Start Drive Motors
        if(startButton && inWait== true){
            setStart();} // end if("Start Button Pressed")
        // Return to Wait state
        if(waitButton){
            setWait();} // end if("Wait Button Pressed")
        // Stop Drive Motors
        else if(stopButton){
            setStop();
            break; // break while(inWait)
        } // end else if("Start Button Pressed")  
    } // end while(inWait==true)
    break; // break while("Battery has enough voltage")  
  /*  PRINT  */
  /*
  printf("\e[1;1H\e[2J");
  printf("Actual Value:\t%2.2f\n", test_pwm.read());
  printf("Left Value:\t%2.2f\n", L_Sensor.read());
  printf("Right Value:\t%2.2f\n", R_Sensor.read());
  printf("Feedback:\t%2.2f\n", data[0]);
  printf("Error:\t%2.2f\n", data[1]);
  printf("Previous Error:\t%2.2f\n", data[2]);
  printf("Error Change:\t%2.2f\n", data[3]);
  printf("Control Action:\t%2.2f\n", data[4]);
  printf("Duty Cycle:\t%2.2f\n", data[5]);
  printf("Duty Cycle:\t%2.2f\n", data[6]);
  printf("isRunning\t%2.2f\n", data[7]);
  */
  /*  end PRINT  */
    } // end while("Battery has enough voltage")
  } // end while(true)
} // end int main()
// End of Line