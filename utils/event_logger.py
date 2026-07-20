class EventLogger:
    """
    Logs only state changes.

    Prevents duplicate events from being
    written every frame.
    """

    def __init__(self):

        self.previous_states = {}

    #########################################

    def has_changed(
        self,
        event,
        value,
    ):

        if event not in self.previous_states:

            self.previous_states[event] = value

            return True

        if self.previous_states[event] != value:

            self.previous_states[event] = value

            return True

        return False

    #########################################

    def reset(self):

        self.previous_states.clear()