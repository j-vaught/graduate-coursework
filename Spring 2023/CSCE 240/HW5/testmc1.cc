// Copyright 2023 bhipp
// test constructor with default arguments
#include<iostream>
using std::cout;
using std::endl;
#include"multiplechoicequestion.h"
using csce240_program5::MultipleChoiceQuestion;

int main() {
  MultipleChoiceQuestion mc1;
  cout << "Test default constructor / Print(false)" << endl;
  mc1.Print(false);
  cout << "Print(true)" << endl;
  mc1.Print(true);

  MultipleChoiceQuestion mc2("What's the answer?");
  cout << "\nTest constructor with one argument / Print(false)" << endl;
  mc2.Print(false);
  cout << "Print(true)" << endl;
  mc2.Print(true);

  string threeanswers[3] = { "one", "two", "three" };
  MultipleChoiceQuestion mc3("One, two, or three?", 3, threeanswers);
  cout << "\nTest constructor with three arguments / Print(false)" << endl;
  mc3.Print(false);
  cout << "Print(true)" << endl;
  mc3.Print(true);

  bool threetfs[3] = { false, false, true };
  MultipleChoiceQuestion mc4("One, two, or three?", 3, threeanswers, threetfs);
  cout << "\nTest constructor with four arguments / Print(false)" << endl;
  mc4.Print(false);
  cout << "Print(true)" << endl;
  mc4.Print(true);
  return 0;
}
