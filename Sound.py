import pygame as pg

class SoundEffects:
    __instance = None
    __available_sound = True
    __volume = 0.1

    def __init__(self):
        if SoundEffects.__instance is None:
            pg.mixer.init(frequency=44100, channels=2)
            self.__instance = self
            self.__effects = {
                "game_start": pg.mixer.Sound(r"sound\game_start.wav"),
                "game_win": pg.mixer.Sound(r"sound\game_win.wav"),
                "game_loss": pg.mixer.Sound(r"sound\game_loss.wav"),
                "player_shot": pg.mixer.Sound(r"sound\player_shot.wav"),
                "enemy_shot": pg.mixer.Sound(r"sound\enemy_shot.wav")
            }
        else:
            raise Exception("This class is a singleton!")

    @staticmethod
    def get_instance():
        if SoundEffects.__instance is None:
            SoundEffects.__instance = SoundEffects()
        return SoundEffects.__instance    

    def play(self, effect):
        if effect in self.__effects:
            if self.__available_sound:
                sound = self.__effects[effect]
                sound.set_volume(SoundEffects.__volume)  # Set the volume before playing
                sound.play()

    @classmethod
    def get_available_sound(cls):
        return cls.__available_sound
    
    @classmethod
    def set_available_sound(cls, is_sound):
        cls.__available_sound = is_sound

    @classmethod
    def set_volume(cls, volume):
        cls.__volume = volume