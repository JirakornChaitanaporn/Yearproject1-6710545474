import pygame as pg
from player import Player
from random import random
import time
from Bullet import Bullet

class enemies:
    __enemies_list = []
    _spawn_position = []

    def __init__(self, picture, speed, health):
        self._direction = ""
        self._picture = picture
        self._enemy = pg.image.load(self._picture)
        self._enemy = pg.transform.scale(self._enemy, (100, 100))
        self._position = [(int(random() * (600 - 300 + 1))), (int(random() * (600 - 20 + 1)))]
        self._speed = speed
        self._health = health
        self._distance_traveled = 0
        enemies._spawn_position.append(tuple(self._position))
        self._attack_count = 0
        self.__start_timer = time.time()
        self.__end_timer = 0
        self._time_survived = 0

    def enemy_in_bound(self):
        if self._position[0] > 780.0:
            self._position = [775, self._position[1]]
        elif self._position[0] < 0.0:
            self._position = [3, self._position[1]]
        if self._position[1] > 580.0:
            self._position = [self._position[0], 575]
        elif self._position[1] < 0.0:
            self._position = [self._position[0], 3]

    def print_health(self, screen, font):
        health_text = font.render(str(self._health), True, (255, 255, 255))
        screen.blit(health_text, (self._position[0] + 5, self._position[1] - 10.0))

    def get_attack_count(self):
        return self._attack_count

    def get_attacked(self, decrease_health):
        self._health -= decrease_health
        if self._health <= 0:
            self.__end_timer = time.time()
            self._time_survived = self.__start_timer - self.__end_timer
            enemies.__enemies_list.remove(self)
            Player.change_coin(5)

    @classmethod
    def add_enemies(cls, enemy):
        cls.__enemies_list.append(enemy)

    @classmethod
    def get_enemies_list(cls):
        return cls.__enemies_list
    
    @classmethod
    def clear_enemies(cls):
        cls.__enemies_list.clear()

    @classmethod
    def delete_enemies(cls, enemy):
        cls.__enemies_list.remove(enemy)

    def set_end_timer(self, stopped_time):
        self.__end_timer = stopped_time

    def get_position(self):
        return self._position

    def change_position(self, position:list):
        self._position[0] += position[0]
        self._position[1] += position[1]

    def set_position(self, position):
        self._position = position

    def get_enemy(self):
        return self._enemy

    def set_enemy(self, enemy):
        self._enemy = enemy

    def get_picture(self):
        return self._picture

    def get_direction(self):
        return self._direction