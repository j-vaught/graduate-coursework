// Copyright 2023 Jacob Christopher Vaught
// Copyright 2023 Madelyn Leire Hines
// Project 5: Rotating an image utilizing C code and the Intel Quartus Platorm with a Altera DE2-115 Board

#include "sys/alt_stdio.h"
#include "alt_types.h"
#include <math.h>
#include <string.h>
#include <altera_up_avalon_video_pixel_buffer_dma.h>
#include "system.h"
#include <sys/alt_alarm.h>
#include "myfile.h"
#include "myfile.c" //comment out if reference error to "myimage" is present

const int ROWS = 240;
const int COLS = 320;
const float PI = 3.14159265358979323846f;
const int HALF_ROWS = 120;
const int HALF_COLS = 160;
float theta, thetaCOS, thetaSIN, original_row, original_col;
int shifted_row, shifted_col;
alt_up_pixel_buffer_dma_dev * pixel_buffer;

void frame_function(float COS, float SIN, int rotated_pixel_values[ROWS][COLS]) {
  // Loop through original image and store pixel values in 2D array after rotation
  for (int i = 0; i < ROWS; i++) {
    for (int j = 0; j < COLS; j++) {
      shifted_row = i - HALF_ROWS;
      shifted_col = j - HALF_COLS;
      original_row = roundf((shifted_row * COS - shifted_col * SIN) + HALF_ROWS);
      original_col = roundf((shifted_row * SIN + shifted_col * COS) + HALF_COLS);
      if (original_row < 0 || original_row >= ROWS || original_col < 0 || original_col >= COLS) {
        rotated_pixel_values[i][j] = 0; // black pixel
      } else {
        int base_index = (original_row * COLS * 3) + (original_col * 3);
        rotated_pixel_values[i][j] = (myimage[base_index + 2]) + (myimage[base_index + 1] << 8) + (myimage[base_index] << 16);
      }
    }
  }
}

// Clear pixel buffer

int draw_screen(int( * rotated_pixel_values)[COLS]) {
  alt_up_pixel_buffer_dma_clear_screen(pixel_buffer, 0);
  // Loop through 2D array and draw rotated image onto screen
  for (int i = 0; i < ROWS; i++) {
    for (int j = 0; j < COLS; j++) {
      alt_up_pixel_buffer_dma_draw(pixel_buffer, rotated_pixel_values[i][j], j, i);
    }
  }
}

int main() {
  alt_putstr("Project 5 Jacob Vaught & Madelyn Hines\n");

  pixel_buffer = alt_up_pixel_buffer_dma_open_dev("/dev/dma_buffer");
  if (!pixel_buffer) {
    printf("Error opening pixel buffer\n");
  }

  alt_up_pixel_buffer_dma_clear_screen(pixel_buffer, 0);
  // Pre calculated Values for COS(0, -90, -180, -270\degrees): [1, 0, -1, 0]
  // Pre calculated Values for SIN(0, -90, -180, -270\degrees): [0, -1, 0, 1]
  int degrees_0_array[ROWS][COLS];
  int degrees_90_array[ROWS][COLS];
  int degrees_180_array[ROWS][COLS];
  int degrees_270_array[ROWS][COLS];

  // Call frame_function and pass rotated_pixel_values array as parameter
  printf("Starting Screen Array Calculation For 0 Degrees.\n");
  frame_function(1.0f, 0.0f, degrees_0_array);
  draw_screen(degrees_0_array);
  printf("Starting Screen Array Calculation For 90 Degrees.\n");
  frame_function(0.0f, -1.0f, degrees_90_array);
  draw_screen(degrees_90_array);
  printf("Starting Screen Array Calculation For 180 Degrees.\n");
  frame_function(-1.0f, 0.0f, degrees_180_array);
  draw_screen(degrees_180_array);
  printf("Starting Screen Array Calculation For 270 Degrees.\n");
  frame_function(0.0f, 1.0f, degrees_270_array);
  draw_screen(degrees_270_array);
  printf("Screen Array Calculations Complete!\n Screen Draw Function Commencing:\n");
  int ticks_per_second = alt_ticks_per_second();
  printf("TPS: %d\n", ticks_per_second);

  while (1) {
    unsigned long long fps_sum = 0;
    // This is the code to use if you do not use the default values of 0, 90, 180, 270 degrees
    /*for (int t = 0; t > -360; t -= 90) {
    theta = t * PI / 180.0;
    float COS=cosf(theta);
    float SIN=sinf(theta);
    frame_function();
    */
    int ticks_start = alt_nticks(); // Begin measuring time
    draw_screen(degrees_0_array); // Function to measure speed of
    int ticks_end = alt_nticks(); // End measuring Time
    int ticks_delta = ticks_end - ticks_start;
    float time_delta = (float) ticks_delta / (float) ticks_per_second;
    printf("Total duration for 0 degrees: %d ticks\n", ticks_delta);
    fps_sum += ticks_delta;

    ticks_start = alt_nticks(); // Begin measuring time
    draw_screen(degrees_90_array); // Function to measure speed of
    ticks_end = alt_nticks(); // End measuring Time
    ticks_delta = ticks_end - ticks_start;
    time_delta = (float) ticks_delta / (float) ticks_per_second;
    printf("Total duration for 90 degrees: %d ticks\n", ticks_delta);
    fps_sum += ticks_delta;

    ticks_start = alt_nticks(); // Begin measuring time
    draw_screen(degrees_180_array); // Function to measure speed of
    ticks_end = alt_nticks(); // End measuring Time
    ticks_delta = ticks_end - ticks_start;
    time_delta = (float) ticks_delta / (float) ticks_per_second;
    printf("Total duration for 180 degrees: %d ticks\n", ticks_delta);
    fps_sum += ticks_delta;

    ticks_start = alt_nticks(); // Begin measuring time
    draw_screen(degrees_270_array); // Function to measure speed of
    ticks_end = alt_nticks(); // End measuring Time
    ticks_delta = ticks_end - ticks_start;
    time_delta = (float) ticks_delta / (float) ticks_per_second;
    printf("Total duration for 270 degrees: %d ticks\n", ticks_delta);
    fps_sum += ticks_delta;

    unsigned long long fps_avg = 4.0f / ((unsigned long long) fps_sum / (unsigned long long) ticks_per_second); // FPS is #of frames/Time Delta, where Time Delta=ticks/ticks per second
    //printf("FPS average: %llu \n", fps_avg);
    printf("Tick over previous 4 frames: %d ticks\n\n", (fps_sum / 4));
  }

  return 0;
}
