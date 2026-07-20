from collections import deque


class FatigueAnalyzer:

    def __init__(self, window_size=300):

        self.window_size = window_size

        self.eye_history = deque(maxlen=window_size)
        self.distraction_history = deque(maxlen=window_size)

    ############################################
    # Update Statistics
    ############################################

    def update(
        self,
        ear,
        distracted,
    ):

        # Eye Closed?
        if ear < 0.21:
            self.eye_history.append(1)
        else:
            self.eye_history.append(0)

        # Distracted?
        if distracted:
            self.distraction_history.append(1)
        else:
            self.distraction_history.append(0)
        
    ############################################
    # Eye Closure %
    ############################################

    def get_eye_closure(self):

        if len(self.eye_history) == 0:
            return 0.0

        return (
            sum(self.eye_history)
            / len(self.eye_history)
        ) * 100

    ############################################
    # Distraction %
    ############################################

    def get_distraction(self):

        if len(self.distraction_history) == 0:
            return 0.0

        return (
            sum(self.distraction_history)
            / len(self.distraction_history)
        ) * 100

    ############################################
    # Reset
    ############################################

    def reset(self):

        self.eye_history.clear()
        self.distraction_history.clear()