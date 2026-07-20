import cv2
from config import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT
from utils.logger import logger


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(CAMERA_INDEX)

        if not self.cap.isOpened():
            logger.error("Unable to open webcam")
            raise Exception("Unable to open webcam")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

        logger.info("Camera initialized successfully")

    def get_frame(self):
        success, frame = self.cap.read()

        if not success:
            logger.warning("Failed to read frame")
            return None

        return frame

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
        logger.info("Camera released")