import pygame as pg
from enemies import enemies
import random
from player import Player
import math

class BlackHorse(enemies):
    def __init__(self):
        super().__init__(r"image\blackKnight.png", 3, 10.0)
        self.set_enemy(pg.transform.scale(self.get_enemy(), (60, 60)))
        self.__last_attack_time = 0

    def movement(self, player: Player):
        speed = random.random() + 0.3
        if self._position[0] < player.get_position()[0] - 69:
            self._position[0] += speed
            self._distance_traveled += speed
        elif self._position[0] > player.get_position()[0] + 69:
            self._position[0] -= speed
            self._distance_traveled += speed
        if self._position[1] < player.get_position()[1] - 69:
            self._position[1] += speed
            self._distance_traveled += speed
        elif self._position[1] > player.get_position()[1] + 69:
            self._position[1] -= speed
            self._distance_traveled += speed

        # Repel other enemies
        for other in enemies.get_enemies_list():
            if other != self and hasattr(other, '_position'):
                dx = self._position[0] - other._position[0]
                dy = self._position[1] - other._position[1]
                distance = math.sqrt(dx ** 2 + dy ** 2)

                if distance < 50 and distance > 0:
                    dx /= distance
                    dy /= distance

                    repulsion_strength = 1
                    self._position[0] += dx * repulsion_strength
                    self._position[1] += dy * repulsion_strength
        self.enemy_in_bound()

    def __get_distance(self, pos1, pos2):
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def attack(self, player: Player):
        current_time = pg.time.get_ticks()
        if current_time - self.__last_attack_time >= 250:
            if self.__get_distance(player.get_position(), self._position) <= 75:
                player.decrease_health(1)
                self._attack_count += 1
                self.__last_attack_time = current_time
