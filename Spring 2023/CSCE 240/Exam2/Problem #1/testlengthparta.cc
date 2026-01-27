// Copyright 2023 bhipp
// Initial tests (add more) for the Length class constructor, accessor
// functions, mutator functions, and Convert function
#include<iostream>
using std::cout;
using std::endl;
#include"length.h"

int main() {
  Length ldefault;
  if ( ldefault.GetValue() == 0 && ldefault.GetUnits() == "inches" ) {
    cout << "Passed default constructor / accessor test" << endl;
  } else {
    cout << "Failed default constructor / accessor test" << endl;
  }
  Length l3inches(3.5);
  if ( l3inches.GetValue() == 3.5 && l3inches.GetUnits() == "inches" ) {
    cout << "Passed 1 good argument constructor / accessor test" << endl;
  } else {
    cout << "Failed 1 good argument constructor / accessor test" << endl;
  }
  Length l5centimeters(5, "centimeters");
  if ( l5centimeters.GetValue() == 5 &&
       l5centimeters.GetUnits() == "centimeters" ) {
    cout << "Passed 2 good argument constructor / accessor test" << endl;
  } else {
    cout << "Failed 2 good argument constructor / accessor test" << endl;
  }
  Length l1badarg(-7);
  if ( l1badarg.GetValue() == 0 && l1badarg.GetUnits() == "inches" ) {
    cout << "Passed 1 bad argument constructor / accessor test" << endl;
  } else {
    cout << "Failed 1 bad argument constructor / accessor test" << endl;
  }
  Length l1good1badarg(14, "degrees");
  if ( l1good1badarg.GetValue() == 14 &&
       l1good1badarg.GetUnits() == "inches" ) {
    cout << "Passed 1 good 1 bad argument constructor / accessor test" << endl;
  } else {
    cout << "Failed 1 good 1 bad argument constructor / accessor test" << endl;
  }
  l1good1badarg.SetValue(-8);
  if ( l1good1badarg.GetValue() == 14 &&
       l1good1badarg.GetUnits() == "inches" ) {
    cout << "Passed SetValue bad argument / accessor test" << endl;
  } else {
    cout << "Failed SetValue bad argument / accessor test" << endl;
  }
  l1good1badarg.SetValue(1.5);
  if ( l1good1badarg.GetValue() == 1.5 &&
       l1good1badarg.GetUnits() == "inches" ) {
    cout << "Passed SetValue good argument / accessor test" << endl;
  } else {
    cout << "Failed SetValue good argument / accessor test" << endl;
  }
  l1good1badarg.SetUnits("acres");
  if ( l1good1badarg.GetValue() == 1.5 &&
       l1good1badarg.GetUnits() == "inches" ) {
    cout << "Passed SetUnits bad argument / accessor test" << endl;
  } else {
    cout << "Failed SetUnits bad argument / accessor test" << endl;
  }
  l1good1badarg.SetUnits("centimeters");
  if ( l1good1badarg.GetValue() == 1.5 &&
       l1good1badarg.GetUnits() == "centimeters" ) {
    cout << "Passed SetUnits good argument / accessor test" << endl;
  } else {
    cout << "Failed SetUnits good argument / accessor test" << endl;
  }
  Length l2inches(2);
  l2inches.Convert("centimeters");
  if ( l2inches.GetValue() == 5.08 &&
       l2inches.GetUnits() == "centimeters" ) {
    cout << "Passed Convert inches to centimeters test" << endl;
  } else {
    cout << "Failed Convert inches to centimeters test" << endl;
  }
  Length l10inches(25.4, "centimeters");
  l10inches.Convert("inches");
  if ( l10inches.GetValue() == 10 &&
       l10inches.GetUnits() == "inches" ) {
    cout << "Passed Convert centimeters to inches test" << endl;
  } else {
    cout << "Failed Convert centimeters to inches test" << endl;
  }
  Length l4cm(4, "centimeters");
  l4cm.Convert("centimeters");
  if ( l4cm.GetValue() == 4 &&
       l4cm.GetUnits() == "centimeters" ) {
    cout << "Passed Convert centimeters to centimeters test" << endl;
  } else {
    cout << "Failed Convert centimeters to centimeters test" << endl;
  }
  l4cm.Convert("saywhat");
  if ( l4cm.GetValue() == 4 &&
       l4cm.GetUnits() == "centimeters" ) {
    cout << "Passed Convert invalid argument test" << endl;
  } else {
    cout << "Failed Convert invalid argument test" << endl;
  }
  return 0;
}
