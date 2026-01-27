// Copyright 2023 bhipp
// prototypes for functions implemented in pointer_problem_functions.cc
// DO NOT MODIFY THE CONTENTS OF THIS FILE!
#ifndef _POINTERPROBLEMFUNCTIONS_H_
#define _POINTERPROBLEMFUNCTIONS_H_

// the SortedDynamic struct will hold a pointer to a block of distinct sorted
// integers, and an integer that specifies the number of integers in the block.
// This structure type is used in pointerproblemdriver.cc and by the Print
// and Merge functions whose prototypes are given below.
struct SortedDynamicArray {
  int size;
  int * values;
};

// the Print function is already implemented in pointerfunctions.cc
void Print(const SortedDynamicArray * const nums);

// You will implement the Merge function, whose prototype is given below, in
// pointerproblemfunctions.cc
// The Merge function takes two pointers to SortedDynamicArray structures.
// The function assumes that the two structures the arguments point to contain
// distinct integers that are sorted in ascending order. These preconditions
// must be met in order for the function to merge the values as expected.
// The function will merge the two sorted lists of values into the structure
// that the first argument points to. That updated structure should be resized
// to exactly fit the merged, sorted list of distinct values.
// For example: If the first argument points to a structure with size 4 and
//              values { 3, 8, 15, 22 }, and the second argument points to a
//              structure with size 6 and values { 1, 8, 10, 16, 22, 30}
//              Then after the function call, the first argument should be
//              updated to point to a structure with size 8 and values
//              { 1, 3, 8, 10, 15, 16, 22, 30 }
void Merge(SortedDynamicArray * const, const SortedDynamicArray * const);

#endif  // end _POINTERPROBLEMFUNCTIONS_H_
