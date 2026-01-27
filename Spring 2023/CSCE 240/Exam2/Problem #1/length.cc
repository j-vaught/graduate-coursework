//copyright 2023 jvaught
//Length class that can compare lengths
// Length.cc

#include "length.h"

#include <iostream>

Length::Length(double v,
  const std::string & u) {
  value = (v >= 0) ? v : 0;
  units = validateUnits(u) ? u : "inches";
}

bool Length::validateUnits(const std::string & u) const {
  return u == "inches" || u == "centimeters";
}

void Length::SetUnits(const std::string & u) {
  if (validateUnits(u)) {
    units = u;
  }
}

void Length::SetValue(double v) {
  if (v >= 0) {
    value = v;
  }
}

double Length::GetValue() const {
  return value;
}

std::string Length::GetUnits() const {
  return units;
}

void Length::Convert(const std::string & u) {
  if (validateUnits(u) && u != units) {
    if (u == "centimeters") {
      value = value * 2.54;
    } else {
      value = value / 2.54;
    }
    units = u;
  }
}

Length Length::operator + (const Length & other) const {
  double convertedValue = other.value;
  std::string convertedUnits = other.units;
  if (units != other.units) {
    if (units == "inches") {
      convertedValue /= 2.54;
      convertedUnits = "inches";
    } else {
      convertedValue *= 2.54;
      convertedUnits = "centimeters";
    }
  }

  return Length(value + convertedValue, units);
}

bool Length::operator == (const Length & other) const {
  double convertedValue = other.value;
  std::string convertedUnits = other.units;

  if (units != other.units) {
    if (units == "inches") {
      convertedValue /= 2.54;
      convertedUnits = "inches";
    } else {
      convertedValue *= 2.54;
      convertedUnits = "centimeters";
    }
  }

  return value == convertedValue && units == convertedUnits;
}

bool Length::operator < (const Length & other) const {
  double convertedValue = other.value;
  std::string convertedUnits = other.units;
  if (units != other.units) {
    if (units == "inches") {
      convertedValue /= 2.54;
      convertedUnits = "inches";
    } else {
      convertedValue *= 2.54;
      convertedUnits = "centimeters";
    }
  }

  return value < convertedValue;

}

std::ostream & operator << (std::ostream & os,
  const Length & l) {
  os << l.value << " " << l.units;
  return os;
}
