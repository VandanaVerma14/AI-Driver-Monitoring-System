from collections import deque


class ValueSmoother:
    """
    Smooths noisy values using a moving average.

    This is useful for:
    - Head Pose (Yaw, Pitch, Roll)
    - EAR
    - MAR
    - Safety Score (optional)

    Parameters
    ----------
    window_size : int
        Number of previous values used for averaging.
    """

    def __init__(self, window_size: int = 10):

        self.window_size = window_size

        self.values = deque(maxlen=window_size)

    def update(self, value: float):
        """
        Add a new value.

        Parameters
        ----------
        value : float

        Returns
        -------
        float
            Smoothed value.
        """

        self.values.append(value)

        return self.get_average()

    def get_average(self):
        """
        Returns the moving average.
        """

        if len(self.values) == 0:
            return 0.0

        return sum(self.values) / len(self.values)

    def reset(self):
        """
        Clear all stored values.
        """

        self.values.clear()

    def size(self):
        """
        Number of stored values.
        """

        return len(self.values)