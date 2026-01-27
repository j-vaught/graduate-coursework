// Copyright 2023 jvaught
// shortanswerquestion class
// Completed: 9:26 PM 4/11/2023

#include "shortanswerquestion.h"
#include <iostream>

ShortAnswerQuestion::ShortAnswerQuestion(std::string question,
                                         std::string answer)
    : Question(question), answer_(answer) {}

std::string ShortAnswerQuestion::GetAnswer() const { return answer_; }

void ShortAnswerQuestion::SetAnswer(std::string answer) { answer_ = answer; }

void ShortAnswerQuestion::Print(bool print_answer) const {
  std::cout << "Question: " << GetQuestion() << std::endl;
  if (print_answer) {
    std::cout << "Correct Answer: " << GetAnswer() << std::endl;
  }
}
