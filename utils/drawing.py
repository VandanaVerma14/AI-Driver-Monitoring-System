import cv2
import mediapipe as mp

# MediaPipe drawing utilities
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


def draw_face_mesh(frame, face_landmarks):
    """
    Draw the complete MediaPipe face mesh.
    """

    mp_drawing.draw_landmarks(
        image=frame,
        landmark_list=face_landmarks,
        connections=mp_face_mesh.FACEMESH_TESSELATION,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style(),
    )

    mp_drawing.draw_landmarks(
        image=frame,
        landmark_list=face_landmarks,
        connections=mp_face_mesh.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style(),
    )


def draw_text(frame, text, position=(20, 30), color=(0, 255, 0), scale=0.7, thickness=2):
    """
    Draw text on the frame.
    """

    cv2.putText(
        frame,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        scale,
        color,
        thickness,
        cv2.LINE_AA,
    )


def draw_circle(frame, x, y, color=(0, 0, 255), radius=2):
    """
    Draw a small circle.
    """

    cv2.circle(
        frame,
        (int(x), int(y)),
        radius,
        color,
        -1,
    )


def draw_line(frame, pt1, pt2, color=(255, 0, 0), thickness=2):
    """
    Draw a line.
    """

    cv2.line(
        frame,
        (int(pt1[0]), int(pt1[1])),
        (int(pt2[0]), int(pt2[1])),
        color,
        thickness,
    )