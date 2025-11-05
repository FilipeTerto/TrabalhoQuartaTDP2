from abc import ABC, abstractmethod
from model.questions import Question 

class QuestionFactory(ABC):
    @abstractmethod
    def create_question(self, text, alternatives, correct_answer_id):
        pass


class MultipleChoiceFactory(QuestionFactory):
    def create_question(self, text, alternatives, correct_answer_id):
        return Question(
            text=text,
            alternatives=alternatives,
            correct_answer_id=correct_answer_id
        )


class TrueFalseFactory(QuestionFactory):
    def create_question(self, text, alternatives=None, correct_answer_id=None):
        alternatives = [
            {"id": 1, "text": "Verdadeiro"},
            {"id": 2, "text": "Falso"}
        ]
        return Question(
            text=text,
            alternatives=alternatives,
            correct_answer_id=correct_answer_id
        )
