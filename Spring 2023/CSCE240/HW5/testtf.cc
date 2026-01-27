// Copyright 2023 bhipp
#include<iostream>
using std::cout;
using std::endl;
#include"truefalsequestion.h"
using csce240_program5::TrueFalseQuestion;

int main() {
  TrueFalseQuestion tf1, tf2("CSCE240 is the best class ever."),
                    tf3("I am eight feet tall", false);
  cout << "Test default constructor / Print(false)" << endl;
  tf1.Print(false);
  cout << "Print(true)" << endl;
  tf1.Print(true);
  cout << "\nTest constructor with one argument / Print(false)" << endl;
  tf2.Print(false);
  cout << "Print(true)" << endl;
  tf2.Print(true);
  cout << "\nTest constructor with two arguments / Print(false)" << endl;
  tf3.Print(false);
  cout << "Print(true)" << endl;
  tf3.Print(true);
  return 0;
}
