// Copyright 2023 CSCE240
#include<iostream>
using std::cout;
using std::endl;
#include"shortanswerquestion.h"
using csce240_program5::ShortAnswerQuestion;

int main() {
  ShortAnswerQuestion sa1, sa2("What's the meaning of life?"),
    sa3("What do you do if you're happy and you know it?", "Clap your hands");
  cout << "Test default constructor / Print(false)" << endl;
  sa1.Print(false);
  cout << "Print(true)" << endl;
  sa1.Print(true);
  cout << "\nTest constructor with one argument / Print(false)" << endl;
  sa2.Print(false);
  cout << "Print(true)" << endl;
  sa2.Print(true);
  cout << "\nTest constructor with two arguments / Print(false)" << endl;
  sa3.Print(false);
  cout << "Print(true)" << endl;
  sa3.Print(true);
  return 0;
}
