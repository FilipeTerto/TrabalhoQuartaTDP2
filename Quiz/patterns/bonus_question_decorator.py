from model.questions import Question

class BonusQuestion:
    """
    Decorator para marcar uma pergunta como bônus.
    Pode adicionar estrela ao texto e multiplicador de pontuação.
    """
    def __init__(self, question: Question):
        self._question = question
        self.is_bonus = True

    @property
    def id(self):
        return self._question.id

    @property
    def text(self):
        return f"{self._question.text} ⭐"  # adiciona estrela ao texto

    @property
    def alternatives(self):
        return self._question.alternatives

    @property
    def correct_answer_id(self):
        return self._question.correct_answer_id

    def score_multiplier(self):
        return 2  # dobra a pontuação para perguntas bônus
