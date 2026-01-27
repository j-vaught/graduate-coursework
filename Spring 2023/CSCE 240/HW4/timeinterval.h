// Copyright 2023 jvaught
// header file for TimeInterval class

#ifndef TIMEINTERVAL_H
#define TIMEINTERVAL_H

#include "timeofday.h"

#include <string>

#include <iostream>

class TimeInterval {
  public: TimeInterval();
  TimeInterval(const TimeOfDay & startTime,
    const TimeOfDay & endTime);
  TimeInterval(const TimeOfDay & startTime, int length,
    const std::string & units);

  TimeOfDay GetStartTime() const;
  TimeOfDay GetEndTime() const;

  void SetStartTime(const TimeOfDay & startTime);
  void SetEndTime(const TimeOfDay & endTime);
  void SetEndTime(int length,
    const std::string & units);

  void Print(bool militaryTime = false, bool displaySeconds = false) const;

  private: TimeOfDay start;
  TimeOfDay end;
};

#endif // TIMEINTERVAL_H