import pygame
from paths import AUDIO_PATH


class AudioManager:
    def __init__(self, volume=0.5):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(volume)
