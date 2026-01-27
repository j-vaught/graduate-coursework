// Copyright 2023 bhipp
// Initial tests for TimeOfDay class
#include<iostream>
using std::cout;
using std::endl;
#include"timeofday.h"

int main() {
  TimeOfDay t1;
  if ( t1.GetHour() != 0 || t1.GetMinute() != 0 || t1.GetSecond() != 0 )
    cout << "Failed default constructor / accessor function test.";
  else
    cout << "Passed default constructor / accessor function test.";
  cout << endl;

  TimeOfDay t2(9);
  if ( t2.GetHour() != 9 || t2.GetMinute() != 0 || t2.GetSecond() != 0 )
    cout << "Failed constructor one good argument / accessor function test.";
  else
    cout << "Passed constructor one good argument / accessor function test.";
  cout << endl;

  TimeOfDay t3(-3);
  if ( t3.GetHour() != 0 || t3.GetMinute() != 0 || t3.GetSecond() != 0 )
    cout << "Failed constructor one bad argument / accessor function test.";
  else
    cout << "Passed constructor one bad argument / accessor function test.";
  cout << endl;

  TimeOfDay t4(17, 30);
  if ( t4.GetHour() != 17 || t4.GetMinute() != 30 || t4.GetSecond() != 0 )
    cout << "Failed constructor two good arguments / accessor function test.";
  else
    cout << "Passed constructor two good arguments / accessor function test.";
  cout << endl;

  TimeOfDay t5(25, 67);
  if ( t5.GetHour() != 0 || t5.GetMinute() != 0 || t5.GetSecond() != 0 )
    cout << "Failed constructor two bad arguments / accessor function test.";
  else
    cout << "Passed constructor two bad arguments / accessor function test.";
  cout << endl;

  TimeOfDay t6(13, 7, 9);
  if ( t6.GetHour() != 13 || t6.GetMinute() != 7 || t6.GetSecond() != 9 )
    cout << "Failed constructor three good arguments / accessor function test.";
  else
    cout << "Passed constructor three good arguments / accessor function test.";
  cout << endl;

  TimeOfDay t7(3, -8, 159);
  if ( t7.GetHour() != 3 || t7.GetMinute() != 0 || t7.GetSecond() != 0 )
    cout << "Failed constructor three good arguments / accessor function test.";
  else
    cout << "Passed constructor three good arguments / accessor function test.";
  cout << endl;

  t1.SetHour(15);
  t1.SetMinute(6);
  t1.SetSecond(58);
  if ( t1.GetHour() != 15 || t1.GetMinute() != 6 || t1.GetSecond() != 58 )
    cout << "Failed good mutator / accessor function test.";
  else
    cout << "Passed good mutator / accessor function test.";
  cout << endl;

  t1.SetHour(27);
  t1.SetMinute(63);
  t1.SetSecond(-4);
  if ( t1.GetHour() != 15 || t1.GetMinute() != 6 || t1.GetSecond() != 58 )
    cout << "Failed bad mutator / accessor function test.";
  else
    cout << "Passed bad mutator / accessor function test.";
  cout << endl;

  t1.Print();
  t2.Print(true);
  t3.Print(true, true);
  t4.Print(false, true);
  t5.Print();
  t6.Print(true, true);
  t7.Print();
  return 0;
}

