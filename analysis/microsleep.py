class MicrosleepDetector:
    """
    Detects microsleep using Eye Aspect Ratio (EAR).

    If the eyes remain closed continuously for
    a specified number of frames, a microsleep
    event is triggered.
    """

    def __init__(
        self,
        ear_threshold=0.18,
        consecutive_frames=60,
    ):

        self.EAR_THRESHOLD = ear_threshold

        self.MIN_FRAMES = consecutive_frames

        self.closed_counter = 0

        self.microsleep = False
        self.event_sent = False

    ##########################################
    # Update
    ##########################################

    def update(self, ear):

        if ear < self.EAR_THRESHOLD:

            self.closed_counter += 1

        else:

            self.closed_counter = 0
            self.microsleep = False
            self.event_sent = False

        if self.closed_counter >= self.MIN_FRAMES:

            self.microsleep = True
        else:

            self.microsleep = False

        return self.microsleep

    ##########################################

    def is_microsleep(self):

        return self.microsleep

    def just_started(self):

        if self.microsleep and not self.event_sent:

            self.event_sent = True

            return True

        return False
    ##########################################

    def reset(self):

        self.closed_counter = 0
        self.microsleep = False
        self.event_sent = False