// Copyright 2023 bhipp
// test constructor with default arguments
#include<iostream>
using std::cout;
using std::endl;
#include"multiplechoicequestion.h"
using csce240_program5::MultipleChoiceQuestion;

int main() {
  string threeanswers[3] = { "one", "two", "three" };
  bool threetfs[3] = { false, false, true };
  MultipleChoiceQuestion mc1("One, two, or three?", 3, threeanswers, threetfs);
  cout << "original / Print(false):" << endl;
  mc1.Print(false);
  cout << "original / Print(true):" << endl;
  mc1.Print(true);

  MultipleChoiceQuestion mc2(mc1);
  cout << "\ncopy / Print(false):" << endl;
  mc2.Print(false);
  cout << "copy / Print(true):" << endl;
  mc2.Print(true);

  string tenanswers[10] = { "1", "2", "3", "4", "5", "6", "7", "8", "9", "10" };
  bool tentfs[10] = { false, true };
  // note: if the SetAnswerChoices function is implemented correctly, mc2 should
  //       be modified, but mc1 (the original object that was copied) should
  //       remain unchanged
  mc2.SetAnswerChoices(10, tenanswers, tentfs);
  cout << "\nmodified copy / Print(false):" << endl;
  mc2.Print(false);
  cout << "modified copy / Print(true):" << endl;
  mc2.Print(true);
  cout << "\noriginal / Print(false):" << endl;
  mc1.Print(false);
  cout << "original / Print(true):" << endl;
  mc1.Print(true);

  MultipleChoiceQuestion mc3;
  mc2 = mc3 = mc1;
  cout << "\ncopy using assignment / Print(true):" << endl;
  mc3.Print(true);
  mc3.SetAnswerChoices(4, tenanswers, tentfs);
  cout << "\nmodified assignment / Print(true):" << endl;
  mc3.Print(true);
  cout << "original / Print(true):" << endl;
  mc1.Print(true);
  
  return 0;
}
