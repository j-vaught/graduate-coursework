// Copyright 2023 bhipp
// Initial test driver for the struct / pointers / dynamic memory allocation
// problem on Exam 2.
// Your code should compile and link with this UNEDITED file in order to get
// compilation points.
// You are encouraged to create more rigorous tests.
#include<iostream>
using std::cout;
using std::endl;
#include<cstdlib>
#include<ctime>
#include<iomanip>
using std::setw;
#include"pointerproblemfunctions.h"

int main() {
  // seed the random function with the current time
  srand(time(0));
  SortedDynamicArray sorted1, sorted2;

  // randomly generate sizes for two blocks of sorted integers
  sorted1.size = rand() % 20 + 1;
  sorted1.values = new int[sorted1.size];
  sorted2.size = rand() % 20 + 8;
  sorted2.values = new int[sorted2.size];

  // fill the block of memory sorted1.values points to with a list of distinct
  // "random" distinct integers sorted from smallest to largest
  sorted1.values[0] = rand() % 5;
  for ( int i = 1; i < sorted1.size; ++i ) {
    sorted1.values[i] = sorted1.values[i - 1] + rand() % 10 + 1;
  }

  // fill the block of memory sorted2.values points to with a list of distinct
  // "random" distinct integers sorted from smallest to largest
  sorted2.values[0] = rand() % 8;
  for ( int i = 1; i < sorted2.size; ++i ) {
    sorted2.values[i] = sorted2.values[i - 1] + rand() % 6 + 1;
  }

  // print the two lists
  cout << "Size of sorted1 = " << sorted1.size << "\nValues in sorted1:\n";
  Print(&sorted1);
  cout << "\nSize of sorted2 = " << sorted2.size << "\nValues in sorted2:\n";
  Print(&sorted2);

  // Call the Merge function that merges the two SortedDynamicArrays into the
  // first SortedDynamicArray, whose size and values are updated
  Merge(&sorted1, &sorted2);
  cout << "\nUpdated size of sorted1 = " << sorted1.size
       << "\nUpdated values in sorted1:\n";
  Print(&sorted1);
  return 0;
}

