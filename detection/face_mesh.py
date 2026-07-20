import cv2
import mediapipe as mp


class FaceMeshDetector:
    """
    Detects facial landmarks using MediaPipe Face Mesh.
    """

    def __init__(
        self,
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ):

        self.mp_face_mesh = mp.solutions.face_mesh

        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=static_image_mode,
            max_num_faces=max_num_faces,
            refine_landmarks=refine_landmarks,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

        self.mp_drawing = mp.solutions.drawing_utils

        self.drawing_spec = self.mp_drawing.DrawingSpec(
            thickness=1,
            circle_radius=1,
        )

        # Store the latest detection results
        self.results = None

    def detect_landmarks(self, frame):
        """
        Detect facial landmarks and store the result.
        """

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.results = self.face_mesh.process(rgb_frame)

        return self.results

    def get_face_landmarks(self):
        """
        Returns the first detected face landmarks.
        """

        if self.results and self.results.multi_face_landmarks:
            return self.results.multi_face_landmarks[0]

        return None

    def face_detected(self):
        """
        Returns True if a face is detected.
        """

        return (
            self.results is not None
            and self.results.multi_face_landmarks is not None
        )

    def draw_landmarks(self, frame):
        """
        Draw the detected face mesh.
        """

        if self.results and self.results.multi_face_landmarks:

            for face_landmarks in self.results.multi_face_landmarks:

                self.mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.drawing_spec,
                )

        return frame

    def close(self):
        """
        Release MediaPipe resources.
        """
        self.face_mesh.close()