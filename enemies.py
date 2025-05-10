import pygame as pg
from player import Player
import random
import time

class enemies:
    __enemies_list = []
    __time_survived_list = []
    __attack_count_list = []
    __distance_travelled_list = []

    def __init__(self, picture, speed, health):
        self._direction = ""
        self._picture = picture
        self._enemy = pg.image.load(self._picture)
        self._enemy = pg.transform.scale(self._enemy, (100, 100))
        self._position = [(int(random.random() * (600 - 300 + 1))), (int(random.random() * (600 - 20 + 1)))]
        self._speed = speed
        self._health = health
        self._distance_traveled = 0
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

    def print_health(self, screen, max_health):
        pg.draw.rect(screen, (255,0,0), (self._position[0] - 5, self._position[1] - 15, 70, 10))
        pg.draw.rect(screen, (0,255,0), (self._position[0] - 5, self._position[1] - 15, 70 * (self._health/max_health), 10))


    def get_attack_count(self):
        return self._attack_count

    def get_attacked(self, decrease_health):
        self._health -= decrease_health
        if self._health <= 0:
            enemies.__attack_count_list.append(self._attack_count)
            enemies.__distance_travelled_list.append(round(self._distance_traveled,2))
            self.__end_timer = time.time()
            self._time_survived = self.__end_timer -  self.__start_timer
            enemies.__time_survived_list.append(round(self._time_survived,2))
            enemies.__enemies_list.remove(self)
            Player.change_coin(int(random.random() * 3) + 7)

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

    @classmethod
    def get_survive_time(cls):
        return cls.__time_survived_list
    
    @classmethod
    def get_attack_count_list(cls):
        return cls.__attack_count_list
    
    @classmethod
    def get_distance_travelled_list(cls):
        return cls.__distance_travelled_list
    
    @classmethod
    def set_time_survived(cls, _list):
        cls.__time_survived_list = _list

    @classmethod
    def set_attack_count(cls, _list):
        cls.__attack_count_list = _list

    @classmethod
    def set_distance_travelled(cls, _list):
        cls.__distance_travelled_list = _list

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