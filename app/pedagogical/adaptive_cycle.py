class AdaptiveLearningCycle:
    def __init__(self):
        self.stage = 1

    def next_stage(self, correct: bool):
        """
        If correct → return CORRECT and do not increment.
        If incorrect → move to next stage.
        """
        if correct:
            return "CORRECT"

        self.stage += 1
        return self.stage