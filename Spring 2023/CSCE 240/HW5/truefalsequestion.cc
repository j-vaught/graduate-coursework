// Copyright 2023 jvaught
// trueFalsequestion class
// Completed: 9:24 PM 4/11/2023

#include "truefalsequestion.h"
#include <iostream>

TrueFalseQuestion::TrueFalseQuestion(std::string question, bool answer)
    : Question(question), answer_(answer) {}

bool TrueFalseQuestion::GetAnswer() const { return answer_; }

void TrueFalseQuestion::SetAnswer(bool answer) { answer_ = answer; }

void TrueFalseQuestion::Print(bool print_answer) const {
  std::cout << "Question: " << GetQuestion() << std::endl;
  if (print_answer) {
    std::cout << "Correct Answer: " << (answer_ ? "true" : "false")
              << std::endl;
  }
}
