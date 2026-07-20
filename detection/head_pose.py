import cv2
import numpy as np


class HeadPoseEstimator:
    """
    Estimates the head pose (Yaw, Pitch, Roll)
    using MediaPipe facial landmarks and OpenCV solvePnP.
    """

    def __init__(self):

        # Landmark indices used for pose estimation
        self.landmark_ids = {
        "nose_tip": 1,
        "chin": 199,
        "left_eye_outer": 33,
        "right_eye_outer": 263,
        "left_mouth": 61,
        "right_mouth": 291,
        }

    def estimate_pose(self, face_landmarks, frame_width, frame_height):
        """
        Estimate head pose angles.

        Returns
        -------
        pitch, yaw, roll
        """

        image_points = []
        model_points = []

        # -------------------------
        # 2D Image Points
        # -------------------------

        for key in self.landmark_ids:

            idx = self.landmark_ids[key]

            landmark = face_landmarks.landmark[idx]

            x = landmark.x * frame_width
            y = landmark.y * frame_height

            image_points.append((x, y))

        image_points = np.array(image_points, dtype=np.float64)

        # -------------------------
        # Approximate 3D Face Model
        # -------------------------

        model_points = np.array([
        (0.0,   0.0,    0.0),      # Nose Tip
        (0.0, -75.0,  -15.0),      # Chin
        (-45.0, 35.0, -30.0),      # Left Eye Outer
        (45.0, 35.0, -30.0),       # Right Eye Outer
        (-30.0,-35.0, -30.0),      # Left Mouth
        (30.0,-35.0, -30.0),       # Right Mouth
        ], dtype=np.float64)

        # -------------------------
        # Camera Matrix
        # -------------------------

        focal_length = frame_width

        camera_matrix = np.array([
            [focal_length, 0, frame_width / 2],
            [0, focal_length, frame_height / 2],
            [0, 0, 1]
        ], dtype=np.float64)

        dist_coeffs = np.zeros((4, 1))

        # -------------------------
        # Solve PnP
        # -------------------------

        success, rotation_vector, translation_vector = cv2.solvePnP(
            model_points,
            image_points,
            camera_matrix,
            dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE
        )

        if not success:
            return 0.0, 0.0, 0.0

        # -------------------------
        # Rotation Matrix
        # -------------------------

        rotation_matrix, _ = cv2.Rodrigues(rotation_vector)

        # -------------------------
        # Extract Euler Angles
        # -------------------------

        sy = np.sqrt(
        rotation_matrix[0, 0] * rotation_matrix[0, 0]
        + rotation_matrix[1, 0] * rotation_matrix[1, 0]
    )

        singular = sy < 1e-6

        if not singular:
            x = np.arctan2(
            rotation_matrix[2, 1],
            rotation_matrix[2, 2]
            )

            y = np.arctan2(
            -rotation_matrix[2, 0],
            sy
            )

            z = np.arctan2(
            rotation_matrix[1, 0],
            rotation_matrix[0, 0]
            )

        else:

            x = np.arctan2(
            -rotation_matrix[1, 2],
            rotation_matrix[1, 1]
            )

            y = np.arctan2(
            -rotation_matrix[2, 0],
            sy
            )

        z = 0

        pitch = np.degrees(x)
        yaw = np.degrees(y)
        roll = np.degrees(z)

        # -------------------------
        # Normalize Angles
        # -------------------------

        if pitch > 90:
            pitch -= 180
        elif pitch < -90:
            pitch += 180

        if yaw > 90:
            yaw -= 180
        elif yaw < -90:
            yaw += 180

        if roll > 90:
            roll -= 180
        elif roll < -90:
            roll += 180

        return pitch, yaw, roll
       

        print(f"Raw Euler -> Pitch: {pitch:.2f}, Yaw: {yaw:.2f}, Roll: {roll:.2f}")
        return pitch, yaw, roll