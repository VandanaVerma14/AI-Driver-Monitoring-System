class SafetyScore:

    def __init__(self):
        self.score = 100

    def calculate(
        self,
        eye_closure,
        distraction,
        ear,
        mar,
        microsleep,
    ):

        score = 100

        #################################
        # Eye Closure %s
        #################################

        if eye_closure > 40:
            score -= 40

        elif eye_closure > 30:
            score -= 25

        elif eye_closure > 20:
            score -= 10

        #################################
        # Distraction %
        #################################

        if distraction > 40:
            score -= 30

        elif distraction > 25:
            score -= 20

        elif distraction > 10:
            score -= 10

        #################################
        # Current Eye State
        #################################

        if ear < 0.18:
            score -= 15

        #################################
        # Current Mouth State
        #################################

        if mar > 0.65:
            score -= 10

        #################################
        # Microsleep
        #################################

        if microsleep:
           score -= 50

        score = max(0, min(100, score))

        self.score = score

        return score

    def get_status(self):

        if self.score >= 90:
            return "Excellent"

        elif self.score >= 75:
            return "Good"

        elif self.score >= 60:
            return "Alert"

        elif self.score >= 40:
            return "Fatigued"

        else:
            return "Danger"