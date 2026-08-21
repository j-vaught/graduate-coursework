// Copyright 2023 jvaught
// time of day header file
#ifndef TIMEOFDAY_H
#define TIMEOFDAY_H

class TimeOfDay {
  private: int hour;
  int minute;
  int second;

  public: TimeOfDay(int h = 0, int m = 0, int s = 0);

  void SetHour(int h);
  void SetMinute(int m);
  void SetSecond(int s);

  int GetHour() const;
  int GetMinute() const;
  int GetSecond() const;

  void Print(bool militaryTime = false, bool showSeconds = false) const;
};

#endif // TIMEOFDAY_H