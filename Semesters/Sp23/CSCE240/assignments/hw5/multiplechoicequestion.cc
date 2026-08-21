// Copyright 2023 jvaught
// multiplechoicequestion class
// Completed: 9:29 PM 4/11/2023

#include "multiplechoicequestion.h"
#include <iostream>

MultipleChoiceQuestion::MultipleChoiceQuestion(std::string question,
                                               int num_choices,
                                               std::string *answer_choices,
                                               bool *correct_answers)
    : Question(question), num_choices_(num_choices) {
  answer_choices_ = new std::string[num_choices_];
  correct_answers_ = new bool[num_choices_];

  for (int i = 0; i < num_choices_; i++) {
    if (answer_choices != nullptr) {
      answer_choices_[i] = answer_choices[i];
    } else {
      answer_choices_[i] = "";
    }

    if (correct_answers != nullptr) {
      correct_answers_[i] = correct_answers[i];
    } else {
      correct_answers_[i] = true;
    }
  }
}

MultipleChoiceQuestion::MultipleChoiceQuestion(
    const MultipleChoiceQuestion &other)
    : Question(other.GetQuestion()), num_choices_(other.num_choices_) {
  answer_choices_ = new std::string[num_choices_];
  correct_answers_ = new bool[num_choices_];

  for (int i = 0; i < num_choices_; i++) {
    answer_choices_[i] = other.answer_choices_[i];
    correct_answers_[i] = other.correct_answers_[i];
  }
}

MultipleChoiceQuestion &
MultipleChoiceQuestion::operator=(const MultipleChoiceQuestion &other) {
  if (this != &other) {
    SetQuestion(other.GetQuestion());
    num_choices_ = other.num_choices_;
    delete[] answer_choices_;
    delete[] correct_answers_;
    answer_choices_ = new std::string[num_choices_];
    correct_answers_ = new bool[num_choices_];
    for (int i = 0; i < num_choices_; i++) {
      answer_choices_[i] = other.answer_choices_[i];
      correct_answers_[i] = other.correct_answers_[i];
    }
  }
  return *this;
}

MultipleChoiceQuestion::~MultipleChoiceQuestion() {
  delete[] answer_choices_;
  delete[] correct_answers_;
}

void MultipleChoiceQuestion::SetAnswerChoices(int num_choices,
                                              std::string *answer_choices,
                                              bool *correct_answers) {
  num_choices_ = num delete[] answer_choices_;
  delete[] correct_answers_;
  answer_choices_ = new std::string[num_choices_];
  correct_answers_ = new bool[num_choices_];

  for (int i = 0; i < num_choices_; i++) {
    if (answer_choices != nullptr) {
      answer_choices_[i] = answer_choices[i];
    } else {
      answer_choices_[i] = "";
    }

    if (correct_answers != nullptr) {
      correct_answers_[i] = correct_answers[i];
    } else {
      correct_answers_[i] = true;
    }
  }
}

void MultipleChoiceQuestion::Print(bool print_answer) const {
  std::cout << "Question: " << GetQuestion() << std::endl;
  std::cout << "Answer Choices:" << std::endl;
  for (int i = 0; i < num_choices_; i++) {
    std::cout << answer_choices_[i];
    if (print_answer) {
      std::cout << (correct_answers_[i] ? " - correct" : " - incorrect");
    }
    std::cout << std::endl;
  }
}
