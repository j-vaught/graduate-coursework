//Copyright 2023 jvaught
//Length class header file that can compare lengths

// Length.h

#ifndef LENGTH_H
#define LENGTH_H

#include <string>

class Length {
  private: double value;
  std::string units;
  bool validateUnits(const std::string & u) const;
  
  public: Length(double v = 0,
    const std::string & u = "inches");
  void SetUnits(const std::string & u);
  void SetValue(double v);
  double GetValue() const;
  std::string GetUnits() const;
  void Convert(const std::string & u);
  Length operator + (const Length & other) const;
  bool operator == (const Length & other) const;
  bool operator < (const Length & other) const;
  friend std::ostream & operator << (std::ostream & os,
    const Length & l);
};
#endif // LENGTH_H