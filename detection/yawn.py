class YawnCounter:
    """
    Detects and counts yawns using the
    Mouth Aspect Ratio (MAR).

    A yawn is counted only when:
    1. MAR stays above the threshold for
       a minimum number of consecutive frames.
    2. The mouth closes again.

    This prevents counting the same yawn
    multiple times.
    """

    def __init__(
        self,
        mar_threshold: float = 0.60,
        consecutive_frames: int = 10,
    ):

        # MAR threshold above which mouth is considered open
        self.MAR_THRESHOLD = mar_threshold

        # Minimum frames for a valid yawn
        self.MIN_CONSEC_FRAMES = consecutive_frames

        # Counts consecutive open-mouth frames
        self.frame_counter = 0

        # Total yawns detected
        self.yawn_count = 0

    def update(self, mar: float):
        """
        Update yawn detection.

        Parameters
        ----------
        mar : float
            Mouth Aspect Ratio.

        Returns
        -------
        bool
            True if a yawn is detected,
            otherwise False.
        """

        yawn_detected = False

        # Mouth Open
        if mar > self.MAR_THRESHOLD:

            self.frame_counter += 1

        # Mouth Closed
        else:

            if self.frame_counter >= self.MIN_CONSEC_FRAMES:

                self.yawn_count += 1
                yawn_detected = True

            self.frame_counter = 0

        return yawn_detected

    def get_total_yawns(self):
        """
        Returns total yawns.
        """

        return self.yawn_count

    def reset(self):
        """
        Reset counters.
        """

        self.frame_counter = 0
        self.yawn_count = 0