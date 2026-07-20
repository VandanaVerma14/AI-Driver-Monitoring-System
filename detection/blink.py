class BlinkCounter:
    """
    Detects and counts eye blinks using the
    Eye Aspect Ratio (EAR).

    A blink is counted only when:
    1. EAR stays below the threshold for a
       minimum number of consecutive frames.
    2. The eye opens again.

    This prevents multiple counts for a
    single blink.
    """

    def __init__(
        self,
        ear_threshold: float = 0.21,
        consecutive_frames: int = 3,
    ):

        # EAR threshold below which eye is considered closed
        self.EAR_THRESHOLD = ear_threshold

        # Minimum consecutive frames for a valid blink
        self.MIN_CONSEC_FRAMES = consecutive_frames

        # Counts how many consecutive frames
        # the eyes remain closed
        self.frame_counter = 0

        # Total blink count
        self.blink_count = 0

    def update(self, ear: float):
        """
        Update blink detection for the current frame.

        Parameters
        ----------
        ear : float
            Eye Aspect Ratio of the current frame.

        Returns
        -------
        bool
            True if a blink is detected,
            otherwise False.
        """

        blink_detected = False

        # Eye Closed
        if ear < self.EAR_THRESHOLD:

            self.frame_counter += 1

        # Eye Open
        else:

            # If eye was closed long enough,
            # count it as one blink.
            if self.frame_counter >= self.MIN_CONSEC_FRAMES:

                self.blink_count += 1
                blink_detected = True

            # Reset frame counter
            self.frame_counter = 0

        return blink_detected

    def get_total_blinks(self):
        """
        Returns total blink count.
        """

        return self.blink_count

    def reset(self):
        """
        Reset all counters.
        """

        self.frame_counter = 0
        self.blink_count = 0