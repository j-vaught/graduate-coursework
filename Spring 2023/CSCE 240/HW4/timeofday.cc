// Copyright 2023 jvaught
// time of day C source file

#include <iostream>

#include "timeofday.h"

TimeOfDay::TimeOfDay(int h, int m, int s) {
  SetHour(h);
  SetMinute(m);
  SetSecond(s);
}

void TimeOfDay::SetHour(int h) {
  if (h >= 0 && h < 24) {
    hour = h;
  } else if(hour >= 0 && hour < 24){
    hour = hour;
  } else{
   hour=0;
  }
}

void TimeOfDay::SetMinute(int m) {
  if (m >= 0 && m < 60) {
    minute = m;
  } else if(minute >= 0 && minute < 60){
    minute = minute;
  } else{
    minute=0;
  }
}

void TimeOfDay::SetSecond(int s) {
  if (s >= 0 && s < 60) {
    second = s;
  } else if(second >= 0 && second < 60){
    second = second;
  } else{
    second=0;
  }
}

int TimeOfDay::GetHour() const {
  return hour;
}

int TimeOfDay::GetMinute() const {
  return minute;
}

int TimeOfDay::GetSecond() const {
  return second;
}

void TimeOfDay::Print(bool militaryTime, bool showSeconds) const {
  int displayHour = hour;
  std::string am_pm;

  if (!militaryTime) {
    if (hour < 12) {
      am_pm = "a.m.";
      if (hour == 0) {
        displayHour = 12;
      }
    } else {
      am_pm = "p.m.";
      if (hour > 12) {
        displayHour -= 12;
      }
    }
  }

  std::cout << (displayHour < 10 ? "0" : "") << displayHour << ":" <<
    (minute < 10 ? "0" : "") << minute;

  if (showSeconds) {
    std::cout << ":" << (second < 10 ? "0" : "") << second;
  }

  if (!militaryTime) {
    std::cout << " " << am_pm;
  }

  std::cout << std::endl;
}
