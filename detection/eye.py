import cv2
import numpy as np
from scipy.spatial import distance


class EyeDetector:
    """
    Handles eye landmark extraction, Eye Aspect Ratio (EAR)
    calculation, and eye visualization.
    """

    # MediaPipe Face Mesh landmark indices
    LEFT_EYE = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE = [362, 385, 387, 263, 373, 380]

    def __init__(self):
        pass

    def get_eye_points(
        self,
        face_landmarks,
        frame_width: int,
        frame_height: int
    ):
        """
        Convert normalized MediaPipe eye landmarks
        into pixel coordinates.

        Returns:
            left_eye (list): List of (x, y) points
            right_eye (list): List of (x, y) points
        """

        left_eye = []
        right_eye = []

        for idx in self.LEFT_EYE:
            landmark = face_landmarks.landmark[idx]
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            left_eye.append((x, y))

        for idx in self.RIGHT_EYE:
            landmark = face_landmarks.landmark[idx]
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            right_eye.append((x, y))

        return left_eye, right_eye

    def calculate_ear(self, eye_points):
        """
        Calculate Eye Aspect Ratio (EAR).

        Formula:
                  ||P2-P6|| + ||P3-P5||
        EAR = ----------------------------
                    2 * ||P1-P4||

        Returns:
            float : Eye Aspect Ratio
        """

        A = distance.euclidean(eye_points[1], eye_points[5])
        B = distance.euclidean(eye_points[2], eye_points[4])
        C = distance.euclidean(eye_points[0], eye_points[3])

        if C <= 0:
            return 0.0

        ear = (A + B) / (2.0 * C)

        return round(ear, 3)

    def get_average_ear(
        self,
        face_landmarks,
        frame_width: int,
        frame_height: int
    ):
        """
        Calculates EAR for both eyes and returns
        the average value.

        Returns:
            average_ear
            left_eye
            right_eye
        """

        left_eye, right_eye = self.get_eye_points(
            face_landmarks,
            frame_width,
            frame_height,
        )

        left_ear = self.calculate_ear(left_eye)
        right_ear = self.calculate_ear(right_eye)

        average_ear = round((left_ear + right_ear) / 2, 3)

        return average_ear, left_eye, right_eye

    def draw_eye_landmarks(self, frame, left_eye, right_eye):
        """
        Draw eye landmarks and eye boundary
        on the frame.
        """

        # Draw left eye
        for point in left_eye:
            cv2.circle(frame, point, 2, (0, 255, 0), -1)

        cv2.polylines(
            frame,
            [np.array(left_eye)],
            True,
            (0, 255, 0),
            1
        )

        # Draw right eye
        for point in right_eye:
            cv2.circle(frame, point, 2, (0, 255, 0), -1)

        cv2.polylines(
            frame,
            [np.array(right_eye)],
            True,
            (0, 255, 0),
            1
        )

        return frame