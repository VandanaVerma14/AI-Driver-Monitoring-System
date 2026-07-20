import math


# MediaPipe Face Mesh mouth landmark indices
UPPER_LIP = 13
LOWER_LIP = 14

LEFT_MOUTH = 78
RIGHT_MOUTH = 308


class MouthDetector:
    """
    Calculates Mouth Aspect Ratio (MAR) to detect yawning.
    """

    def __init__(self):
        pass

    def _distance(self, p1, p2):
        """
        Calculate Euclidean distance between two landmarks.
        """

        return math.sqrt(
            (p1.x - p2.x) ** 2 +
            (p1.y - p2.y) ** 2
        )

    def calculate_mar(self, face_landmarks):
        """
        Calculate Mouth Aspect Ratio (MAR).

        MAR = Vertical Mouth Distance / Horizontal Mouth Distance
        """

        landmarks = face_landmarks.landmark

        upper = landmarks[UPPER_LIP]
        lower = landmarks[LOWER_LIP]

        left = landmarks[LEFT_MOUTH]
        right = landmarks[RIGHT_MOUTH]

        vertical = self._distance(upper, lower)
        horizontal = self._distance(left, right)

        if horizontal == 0:
            return 0

        mar = vertical / horizontal

        return round(mar, 3)

    def is_yawning(self, mar, threshold=0.65):
        """
        Returns True if MAR exceeds threshold.
        """

        return mar > threshold