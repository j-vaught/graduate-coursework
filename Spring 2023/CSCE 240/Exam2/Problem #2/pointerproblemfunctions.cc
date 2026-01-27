// Copyright 2023 jvaught
// Merge function implemented by jvaught
// Print function implemented by bhipp
#include"pointerproblemfunctions.h"
#include<iostream>

using std::cout;
using std::endl;
#include<iomanip>
using std::setw;

// implement the Merge function (described in pointerproblemfunctions.h) here
#include <algorithm>

void Merge(SortedDynamicArray *
  const arr1,
    const SortedDynamicArray *
      const arr2) {
  // allocate memory for the merged array
  int * merged = new int[arr1 -> size + arr2 -> size];

  // merge the two arrays into the merged array
  int i = 0, j = 0, k = 0;
  while (i < arr1 -> size && j < arr2 -> size) {
    if (arr1 -> values[i] < arr2 -> values[j]) {
      merged[k++] = arr1 -> values[i++];
    } else if (arr2 -> values[j] < arr1 -> values[i]) {
      merged[k++] = arr2 -> values[j++];
    } else { // elements are equal, add one and advance both indices
      merged[k++] = arr1 -> values[i++];
      j++;
    }
  }

  // copy any remaining elements from arr1 or arr2 into the merged array
  while (i < arr1 -> size) {
    merged[k++] = arr1 -> values[i++];
  }
  while (j < arr2 -> size) {
    merged[k++] = arr2 -> values[j++];
  }

  // resize arr1 and copy merged array into it
  arr1 -> size = k;
  delete[] arr1 -> values;
  arr1 -> values = new int[k];
  std::copy(merged, merged + k, arr1 -> values);

  // free memory allocated for the merged array
  delete[] merged;
}

// do not modify the implementation of the Print function
void Print(const SortedDynamicArray * nums) {
  for (int i = 0; i < nums -> size; ++i)
    cout << setw(4) << nums -> values[i];
  cout << endl;
}


