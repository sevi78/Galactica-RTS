import os

import pygame

pygame.mixer.pre_init(frequency=44100, size=-16, channels=8, buffer=512, devicename=None, allowedchanges=5)
pygame.mixer.init()


class Sounds:
    def __init__(self):
        """
        use channels for:
        0 = music
        1 = spaceship
        2 = cargoloader
        3 = spacehunter
        4 = click (ui stuff)
        5 =
        6 =
        7 = Ui
        """
        dirpath = os.path.dirname(os.path.realpath(__file__))
        soundpath = os.path.split(dirpath)[0].split("source")[0] + "sounds" + os.sep

        self.click = pygame.mixer.Sound(soundpath + "mixkit-interface-device-click-2577.wav")
        self.hum1 = pygame.mixer.Sound(soundpath + "mixkit-underwater-transmitter-hum-2135.wav")
        self.hum2 = pygame.mixer.Sound(soundpath + "mixkit-electricity-reactor-buzz-904.wav")
        self.hum3 = pygame.mixer.Sound(soundpath + "mixkit-fridge-motor-hum-1865.wav")
        self.electricity = pygame.mixer.Sound(soundpath + "mixkit-static-electric-crackles-1455.wav")
        self.electricity2 = pygame.mixer.Sound(soundpath + "mixkit-low-electricity-humming-2132.wav")
        self.starting = pygame.mixer.Sound(soundpath + "mixkit-night-vision-starting-2476.wav")
        self.bleep = pygame.mixer.Sound(soundpath + "mixkit-high-tech-notification-bleep-2519.wav")
        self.bleep2 = pygame.mixer.Sound(soundpath + "mixkit-high-tech-bleep-2521.wav")
        self.confirm = pygame.mixer.Sound(soundpath + "mixkit-high-tech-bleep-confirmation-2520.wav")
        self.alarm = pygame.mixer.Sound(soundpath + "mixkit-classic-short-alarm-993.wav")
        self.success_ = pygame.mixer.Sound(soundpath + "mixkit-game-success-alert-2039.wav")
        self.success = pygame.mixer.Sound(soundpath + "mixkit-sci-fi-reject-notification-896.wav")
        self.intro_drama = pygame.mixer.Sound(soundpath + "mixkit-cinematic-drama-riser-632.mp3")
        self.happy = pygame.mixer.Sound(soundpath + "mixkit-tile-game-reveal-960.wav")
        self.happy_ = pygame.mixer.Sound(soundpath + "mixkit-happy-crowd-cheer-975.wav")
        self.happy__ = pygame.mixer.Sound(soundpath + "mixkit-fairy-spell-swish-1497.wav")
        self.collect_success = pygame.mixer.Sound(soundpath + "mixkit-bonus-earned-in-video-game-2058.wav")
        self.collect_fail = pygame.mixer.Sound(soundpath + "mixkit-creature-cry-of-hurt-2208.wav")
        self.destroy_building = pygame.mixer.Sound(soundpath + "mixkit-game-blood-pop-slide-2363.wav")
        self.unload_ship = pygame.mixer.Sound(soundpath + "mixkit-coins-handling-1939.wav")
        self.rank_up = pygame.mixer.Sound(soundpath + "mixkit-casino-bling-achievement-2067.wav")
        self.rank_down = pygame.mixer.Sound(soundpath + "mixkit-player-losing-or-failing-2042.wav")

    def get_sound(self, sound):
        return getattr(self, sound)

    def play_sound(self, sound, **kwargs):
        channel = kwargs.get("channel", 7)
        if type(sound) == str:
            sound = self.get_sound(sound)

        loops = kwargs.get("loops", 0)
        maxtime = kwargs.get("maxtime", 0)
        fade_ms = kwargs.get("fade_ms", 0)

        pygame.mixer.Channel(channel).play(sound, loops=loops, maxtime=maxtime, fade_ms=fade_ms)
        pygame.mixer.Channel(channel).set_volume(1.0)
        # print (pygame.mixer.Channel(channel).get_volume(),pygame.mixer.Channel(channel).get_sound() )

    def stop_sound(self, channel, **kwargs):
        pygame.mixer.Channel(channel).stop()


sounds = Sounds()
