import pygame
import os


class Alarm:

    def __init__(self):

        pygame.mixer.init()

        alarm_path = os.path.join(
            "assets",
            "alarm.wav"
        )

        self.sound = pygame.mixer.Sound(alarm_path)

        self.playing = False

    #########################################

    def start(self):

        if not self.playing:

            self.sound.play(loops=-1)

            self.playing = True

    #########################################

    def stop(self):

        if self.playing:

            self.sound.stop()

            self.playing = False