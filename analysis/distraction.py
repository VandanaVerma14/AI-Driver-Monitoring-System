class DistractionDetector:
    """
    Detects driver distraction using head pose angles.
    """

    def __init__(
        self,
        yaw_threshold: float = 30.0,
        pitch_down_threshold: float = 30.0,
        pitch_up_threshold: float = -20.0,
    ):

        # Looking Left / Right
        self.YAW_THRESHOLD = yaw_threshold

        # Looking Down
        self.PITCH_DOWN_THRESHOLD = pitch_down_threshold

        # Looking Up
        self.PITCH_UP_THRESHOLD = pitch_up_threshold

        self.direction = "Forward"
        self.distracted = False

    def update(self, yaw: float, pitch: float):

        self.direction = "Forward"
        self.distracted = False

        ####################################
        # Looking Left
        ####################################

        if yaw > self.YAW_THRESHOLD:

            self.direction = "Looking Left"
            self.distracted = True

        ####################################
        # Looking Right
        ####################################

        elif yaw < -self.YAW_THRESHOLD:

            self.direction = "Looking Right"
            self.distracted = True

        ####################################
        # Looking Down
        ####################################

        elif pitch > self.PITCH_DOWN_THRESHOLD:

            self.direction = "Looking Down"
            self.distracted = True

        ####################################
        # Looking Up
        ####################################

        elif pitch < self.PITCH_UP_THRESHOLD:

            self.direction = "Looking Up"
            self.distracted = True

        return self.direction, self.distracted

    def get_direction(self):
        return self.direction

    def is_distracted(self):
        return self.distracted

    def reset(self):

        self.direction = "Forward"
        self.distracted = False