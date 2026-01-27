// Copyright 2023 bhipp
// Some initial tests for the ==, <, +, and << operators for the Length class
// You should add more!
#include<iostream>
using std::cout;
using std::endl;
using std::cin;
#include<fstream>
using std::ofstream;
using std::ifstream;
#include"length.h"

int main() {
  cout << "Make sure that student-lengthpartb.txt and correct-lengthpartb.txt"
       << "are closed. Press enter to continue the test." << endl;
  cin.get();
  Length l2inches(2);
  const Length l2inchescm(5.08, "centimeters");
  ofstream outfile("student-lengthpartb.txt");
  outfile << (l2inches == l2inchescm ? "Passed " : "Failed ") << l2inches
          << " == " << l2inchescm << " test" << endl;
  outfile << (l2inchescm < l2inches ? "Failed " : "Passed ") << l2inches
          << " < " << l2inchescm << " test" << endl;
  Length correctsum(4, "inches");
  outfile << (l2inches + l2inchescm == correctsum ? "Passed " : "Failed ")
          << l2inches + l2inchescm << " == " << correctsum
          << " test" << endl;
  outfile << (l2inchescm + l2inches == correctsum ? "Passed " : "Failed ")
          << l2inchescm  + l2inches << " == " << correctsum
          << " test" << endl;
  outfile.close();

  ifstream correctfile("correct-lengthpartb.txt"),
           studentfile("student-lengthpartb.txt");
  char correct = correctfile.get(), student = studentfile.get();
  bool ok = true;
  while ( correctfile.good() && ok ) {
    ok = correct == student;
    cout << student;
    correct = correctfile.get();
    student = studentfile.get();
  }
  if ( ok ) {
    cout << "Match!" << endl;
  } else {
    cout << "\nMismatched output. Open student-lengthpartb.txt and "
         << "correct-lengthpartb.txt to compare your output to the expected"
         << "output" << endl;
  }
  return 0;
}
