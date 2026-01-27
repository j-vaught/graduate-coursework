// Copyright 2023 bhipp
// initial tests for the TimeInterval class
#include<iostream>

using std::cout;
using std::endl;

#include"timeinterval.h"
#include"timeofday.h"

int main() {
  TimeInterval interval1;
  if (interval1.GetStartTime().GetHour() == 0 &&
    interval1.GetStartTime().GetMinute() == 0 &&
    interval1.GetStartTime().GetSecond() == 0 &&
    interval1.GetEndTime().GetHour() == 0 &&
    interval1.GetEndTime().GetMinute() == 0 &&
    interval1.GetEndTime().GetSecond() == 0)
    cout << "Passed default constructor test" << endl;
  else
    cout << "Failed default constructor test" << endl;
  interval1.Print();
  cout << endl;

  const TimeOfDay t1(9, 15, 55);
  const TimeOfDay t2(10, 45, 33);
  TimeInterval interval2(t1, t2);
  if (interval2.GetStartTime().GetHour() == 9 &&
    interval2.GetStartTime().GetMinute() == 15 &&
    interval2.GetStartTime().GetSecond() == 55 &&
    interval2.GetEndTime().GetHour() == 10 &&
    interval2.GetEndTime().GetMinute() == 45 &&
    interval2.GetEndTime().GetSecond() == 33)
    cout << "Passed two TimeOfDay argument constructor test" << endl;
  else
    cout << "Failed two TimeOfDay argument constructor test" << endl;
  interval2.Print();
  cout << endl;

  interval2.SetEndTime(t1);
  if (interval2.GetStartTime().GetHour() == 9 &&
    interval2.GetStartTime().GetMinute() == 15 &&
    interval2.GetStartTime().GetSecond() == 55 &&
    interval2.GetEndTime().GetHour() == 9 &&
    interval2.GetEndTime().GetMinute() == 15 &&
    interval2.GetEndTime().GetSecond() == 55)
    cout << "Passed first SetEndTime with TimeOfDay argument test" << endl;
  else
    cout << "Failed first SetEndTime with TimeOfDay argument test" << endl;
  interval2.Print();
  cout << endl;

  interval2.SetEndTime(t2);
  if (interval2.GetStartTime().GetHour() == 9 &&
    interval2.GetStartTime().GetMinute() == 15 &&
    interval2.GetStartTime().GetSecond() == 55 &&
    interval2.GetEndTime().GetHour() == 10 &&
    interval2.GetEndTime().GetMinute() == 45 &&
    interval2.GetEndTime().GetSecond() == 33)
    cout << "Passed first SetEndTime with TimeOfDay argument test" << endl;
  else
    cout << "Failed first SetEndTime with TimeOfDay argument test" << endl;
  interval2.Print();
  cout << endl;

  interval2.SetEndTime(90, "seconds");
  if (interval2.GetStartTime().GetHour() == 9 &&
    interval2.GetStartTime().GetMinute() == 15 &&
    interval2.GetStartTime().GetSecond() == 55 &&
    interval2.GetEndTime().GetHour() == 9 &&
    interval2.GetEndTime().GetMinute() == 17 &&
    interval2.GetEndTime().GetSecond() == 25)
    cout << "Passed SetEndTime(90, \"seconds\") test" << endl;
  else
    cout << "Failed SetEndTime(90, \"seconds\") test" << endl;
  interval2.Print(true, true);
  cout << endl;

  interval2.SetEndTime(165, "minutes");
  if (interval2.GetStartTime().GetHour() == 9 &&
    interval2.GetStartTime().GetMinute() == 15 &&
    interval2.GetStartTime().GetSecond() == 55 &&
    interval2.GetEndTime().GetHour() == 12 &&
    interval2.GetEndTime().GetMinute() == 0 &&
    interval2.GetEndTime().GetSecond() == 55)
    cout << "Passed SetEndTime(165, \"minutes\") test" << endl;
  else
    cout << "Failed SetEndTime(165, \"minutes\") test" << endl;
  interval2.Print(true, true);
  cout << endl;

  interval2.SetEndTime(7, "hours");
  if (interval2.GetStartTime().GetHour() == 9 &&
    interval2.GetStartTime().GetMinute() == 15 &&
    interval2.GetStartTime().GetSecond() == 55 &&
    interval2.GetEndTime().GetHour() == 16 &&
    interval2.GetEndTime().GetMinute() == 15 &&
    interval2.GetEndTime().GetSecond() == 55)
    cout << "Passed SetEndTime(7, \"hours\") test" << endl;
  else
    cout << "Failed SetEndTime(7, \"hours\") test" << endl;
  interval2.Print();
  cout << endl;

  interval2.SetEndTime(-5, "hours");
  if (interval2.GetStartTime().GetHour() == 9 &&
    interval2.GetStartTime().GetMinute() == 15 &&
    interval2.GetStartTime().GetSecond() == 55 &&
    interval2.GetEndTime().GetHour() == 16 &&
    interval2.GetEndTime().GetMinute() == 15 &&
    interval2.GetEndTime().GetSecond() == 55)
    cout << "Passed SetEndTime(-5, \"hours\") test" << endl;
  else
    cout << "Failed SetEndTime(-5, \"hours\") test" << endl;
  interval2.Print();
  cout << endl;

  interval2.SetEndTime(18, "feet");
  if (interval2.GetStartTime().GetHour() == 9 &&
    interval2.GetStartTime().GetMinute() == 15 &&
    interval2.GetStartTime().GetSecond() == 55 &&
    interval2.GetEndTime().GetHour() == 16 &&
    interval2.GetEndTime().GetMinute() == 15 &&
    interval2.GetEndTime().GetSecond() == 55)
    cout << "Passed SetEndTime(18, \"feet\") test" << endl;
  else
    cout << "Failed SetEndTime(18, \"feet\") test" << endl;
  interval2.Print();
  cout << endl;

  TimeInterval interval3(t1, 50, "minutes");
  if (interval3.GetStartTime().GetHour() == 9 &&
    interval3.GetStartTime().GetMinute() == 15 &&
    interval3.GetStartTime().GetSecond() == 55 &&
    interval3.GetEndTime().GetHour() == 10 &&
    interval3.GetEndTime().GetMinute() == 5 &&
    interval3.GetEndTime().GetSecond() == 55)
    cout << "Passed TimeInterval(t1, 50, \"minutes\") test" << endl;
  else
    cout << "Failed TimeInterval(t1, 50, \"minutes\") test" << endl;
  interval3.Print();
  cout << endl;

  TimeInterval interval4(t1, 20, "hours");
  if (interval4.GetStartTime().GetHour() == 9 &&
    interval4.GetStartTime().GetMinute() == 15 &&
    interval4.GetStartTime().GetSecond() == 55 &&
    interval4.GetEndTime().GetHour() == 9 &&
    interval4.GetEndTime().GetMinute() == 15 &&
    interval4.GetEndTime().GetSecond() == 55)
    cout << "Passed TimeInterval(t1, 20, \"hours\") test" << endl;
  else
    cout << "Failed TimeInterval(t1, 20, \"hours\") test" << endl;
  interval4.Print();
  return 0;
}
