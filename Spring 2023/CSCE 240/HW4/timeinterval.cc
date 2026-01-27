// Copyright 2023 jvaught
// C Source file for TimeInterval class

#include "timeinterval.h"

TimeInterval::TimeInterval(): start(0, 0, 0), end(0, 0, 0) {}

TimeInterval::TimeInterval(const TimeOfDay & startTime, const TimeOfDay & endTime): start(startTime), end(endTime) {
  if (endTime.GetHour() < startTime.GetHour() || 
      (endTime.GetHour() == startTime.GetHour() && endTime.GetMinute() < startTime.GetMinute()) ||
      (endTime.GetHour() == startTime.GetHour() && endTime.GetMinute() == startTime.GetMinute() && endTime.GetSecond() < startTime.GetSecond())) {
    end = startTime;
  }
}

TimeInterval::TimeInterval(const TimeOfDay & startTime, int length,
  const std::string & units): start(startTime), end(startTime) {
  SetEndTime(length, units);
}

TimeOfDay TimeInterval::GetStartTime() const {
  return start;
}

TimeOfDay TimeInterval::GetEndTime() const {
  return end;
}

void TimeInterval::SetStartTime(const TimeOfDay & startTime) {
  if (startTime.GetHour() < end.GetHour() ||
      (startTime.GetHour() == end.GetHour() && startTime.GetMinute() < end.GetMinute()) ||
      (startTime.GetHour() == end.GetHour() && startTime.GetMinute() == end.GetMinute() && startTime.GetSecond() <= end.GetSecond())) {
    start = startTime;
  }
}

void TimeInterval::SetEndTime(const TimeOfDay & endTime) {
  if (endTime.GetHour() > start.GetHour() ||
      (endTime.GetHour() == start.GetHour() && endTime.GetMinute() > start.GetMinute()) ||
      (endTime.GetHour() == start.GetHour() && endTime.GetMinute() == start.GetMinute() && endTime.GetSecond() >= start.GetSecond())) {
    end = endTime;
  }
}


void TimeInterval::SetEndTime(int length, const std::string &units) {
if(length<0){return;}
    TimeOfDay newEnd = start;
    int totalSeconds = start.GetHour() * 3600 + start.GetMinute() * 60 + start.GetSecond();

    if (units == "seconds") {
        totalSeconds += length;
    } else if (units == "minutes") {
        totalSeconds += length * 60;
    } else if (units == "hours") {
        totalSeconds += length * 3600;
    } else {
        return;
    }

    // Check if the new end time would still be on the same day
    if (totalSeconds >= 0 && totalSeconds < 86400) {
        int newHour = totalSeconds / 3600;
        int newMinute = (totalSeconds % 3600) / 60;
        int newSecond = totalSeconds % 60;

        newEnd.SetHour(newHour);
        newEnd.SetMinute(newMinute);
        newEnd.SetSecond(newSecond);

        end = newEnd;
    }
}


void TimeInterval::Print(bool militaryTime, bool displaySeconds) const {
  std::cout << "Start time: ";
  start.Print(militaryTime, displaySeconds);
  std::cout << "End time: ";
  end.Print(militaryTime, displaySeconds);
}
