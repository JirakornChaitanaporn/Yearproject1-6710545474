import pygame as pg
import math
import random
from Bullet import Bullet
from skill import PlayerSkill
from Sound import SoundEffects

class Player:
    __coin = 0
    __time_taken_each_wave = []
    __damage_taken_each_wave = []

    def __init__(self, picture, weapon):
        self.__until_skill = 5
        self.__pic = pg.transform.scale(pg.image.load(picture), (60, 60))
        self.__speed = 2
        self.__hitting_effect_left = pg.transform.scale(pg.image.load(r"image\right_hit.png"), (50, 40))
        self.__hitting_effect_right = pg.transform.scale(pg.image.load(r"image\left_hit.png"), (50, 40))
        self.__position = [5.0, 5.0]
        self.__right_queen = pg.image.load(r"image\white_queen_right.png")
        self.__right_queen = pg.transform.scale(self.__right_queen, (60, 60))
        self.__left_queen = pg.image.load(r"image\white_queen_left.png")
        self.__left_queen = pg.transform.scale(self.__left_queen, (60, 60))
        self.__health = 70.0
        self.__max_health = 70.0
        self.__dmg = 3#change to debug(default == 3)
        self.__weapon = weapon
        self.__sword_is_left = 0
        self.__is_attacking = False
        self.__direction = "right"
        self.__position_to_player = 25
        self.__weapon[0][0] = pg.transform.scale(self.__weapon[0][0], (90, 80))
        self.__weapon[0][1] = pg.transform.scale(self.__weapon[0][1], (90, 80))
        self.__weapon[0][2] = pg.transform.scale(self.__weapon[0][2], (90, 80))
        self.__weapon[1][0] = pg.transform.scale(self.__weapon[1][0], (90, 80))
        self.__weapon[1][1] = pg.transform.scale(self.__weapon[1][1], (90, 80))
        self.__weapon[1][2] = pg.transform.scale(self.__weapon[1][2], (90, 80))

        self.__current_weapon = self.__weapon[0][0]
        self.__attack_style = "melee"
        self.__last_attack_time = 0
        self.__attack_cooldown = 300
        self.__sword_state = 0

        self.__key_history = []


    def print_health(self, screen):
        pg.draw.rect(screen, (255,0,0), (self.__position[0] - 5, self.__position[1] - 15, 70, 10))
        pg.draw.rect(screen, (0,255,0), (self.__position[0] - 5, self.__position[1] - 15, 70 * (self.__health/self.__max_health), 10))

    def print_stat(self, screen, font):
        stat_text = font.render(f"Strenght: {self.__dmg}", True, (255, 255, 255))
        screen.blit(stat_text, (500, 20))
        stat_text = font.render(f"Max_health: {self.__max_health}", True, (255, 255, 255))
        screen.blit(stat_text, (500, 50))
        stat_text = font.render(f"Current_health: {self.__health}", True, (255, 255, 255))
        screen.blit(stat_text, (500, 80))
        stat_text = font.render(f"Speed: {self.__speed}", True, (255, 255, 255))
        screen.blit(stat_text, (500, 110))
        stat_text = font.render(f"Weapon: {self.__attack_style}", True, (255, 255, 255))
        screen.blit(stat_text, (500, 140))

    @staticmethod
    def print_coin(screen, font):
        coin = font.render(f"Coins: {Player.__coin}", True, (0, 255, 0))
        screen.blit(coin, (500,180))
    
    def __key_pressed(self, key):
        if key:
            if (key not in self.__key_history):
                self.__key_history.append(key)
                return True
            return False
        else:
            self.__key_history.clear()
            return False

    def player_movement(self, isshop):
        keys = pg.key.get_pressed()
        if not isshop:
            if self.__attack_style == "melee":
                if keys[pg.K_w] and self.__position[1] >= 0:
                    self.__position[1] -= self.__speed
                elif keys[pg.K_s] and self.__position[1] <= 550:
                    self.__position[1] += self.__speed
                elif keys[pg.K_d] and self.__position[0] <= 750:
                    self.__position[0] += self.__speed + 0.5
                elif keys[pg.K_a] and self.__position[0] >= 0:
                    self.__position[0] -= self.__speed + 0.5
            else:
                if keys[pg.K_w] and self.__position[1] >= 0:
                    self.__position[1] -= self.__speed
                    if keys[pg.K_d] and self.__position[0] <= 750:
                        self.__position[0] += self.__speed
                        self.__pic = self.__right_queen
                        self.__direction = "right"
                    elif keys[pg.K_a] and self.__position[0] >= 0:
                        self.__position[0] -= self.__speed
                        self.__pic = self.__left_queen
                        self.__direction = "left"
                elif keys[pg.K_s] and self.__position[1] <= 550:
                    self.__position[1] += self.__speed
                    if keys[pg.K_d] and self.__position[0] <= 750:
                        self.__position[0] += self.__speed
                        self.__pic = self.__right_queen
                        self.__direction = "right"
                    elif keys[pg.K_a] and self.__position[0] >= 0:
                        self.__position[0] -= self.__speed
                        self.__pic = self.__left_queen
                        self.__direction = "left"
                elif keys[pg.K_d] and self.__position[0] <= 750:
                    self.__position[0] += self.__speed
                    self.__pic = self.__right_queen
                    self.__direction = "right"
                elif keys[pg.K_a] and self.__position[0] >= 0:
                    self.__position[0] -= self.__speed
                    self.__pic = self.__left_queen
                    self.__direction = "left"

    def __get_distance(self, pos1, pos2):
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
        
    def player_attack(self, enemies_list:list):
        def collision(bullet_pos: list, player_pos: list) -> bool:
            player_width = 60
            player_height = 60

            if (bullet_pos[0] > player_pos[0] and bullet_pos[0] < player_pos[0] + player_width and
                bullet_pos[1] > player_pos[1] -10 and bullet_pos[1] < player_pos[1] + player_height):
                return True
            return False
        current_time = pg.time.get_ticks()
        if self.__attack_style == "melee":
            if current_time - self.__last_attack_time >= self.__attack_cooldown and self.__key_pressed(pg.key.get_pressed()[pg.K_SPACE]):
                    for enemy in enemies_list:
                        if (self.__get_distance([self.__position[0] + 30 + self.__position_to_player, self.__position[1] + 30], enemy.get_position())) <= 90 and\
                            ((self.__sword_is_left and (self.__position[0]> enemy.get_position()[0]))or \
                             (not self.__sword_is_left and (self.__position[0] < enemy.get_position()[0]))):#correct collision by using swing animation laterrrrr
                            self.__is_attacking = True
                            SoundEffects.get_instance().play("player_shot", 0.1)
                            enemy.get_attacked(self.__dmg)
                            self.__last_attack_time = current_time
        else:
            if current_time - self.__last_attack_time >= self.__attack_cooldown and self.__key_pressed(pg.key.get_pressed()[pg.K_SPACE]):
                if self.__until_skill == 0:
                    SoundEffects.get_instance().play("player_shot", 0.1)
                    PlayerSkill.create_player_skill(self)
                    self.__until_skill = (int(random.random() * 6) + 6)
                else:
                    SoundEffects.get_instance().play("player_shot", 0.1)
                    Bullet.create_bullet(self, "player")
                    self.__until_skill -= 1
                    if self.__pic == self.__right_queen:
                        self.__position[0] -= 0.25
                    else:
                        self.__position[0] += 0.25
                    self.__last_attack_time = current_time
            PlayerSkill.move_player_skill()
            Bullet.bullet_movement(8, "player")

            for bullet in Bullet.get_player_bullet():
                for enemies in enemies_list:
                    if collision(bullet.get_position(), enemies.get_position()):
                        enemies.get_attacked(4)
                        Bullet.remove_player_bullet(bullet)
            for skill in PlayerSkill.get_skill_list():
                for enemies in enemies_list:
                    if collision(skill.get_position(), enemies.get_position()):
                        enemies.set_position([(int(random.random() * 700) + 1), (int(random.random() * 500) + 1)])
                        enemies.get_attacked(10)
                        Bullet.remove_player_bullet(skill)

    def print_skill_status(self, screen,font):
        skill_status = font.render(f"Until skill: {self.__until_skill}", True, (0, 255, 0))
        screen.blit(skill_status, (5,580))
 
    @classmethod
    def change_coin(cls,coin):
        cls.__coin += coin
    @classmethod
    def get_coin(cls):
        return cls.__coin
    @classmethod
    def set_coin(cls, coin):
        cls.__coin = coin 

    @classmethod
    def get_time_taken_each_wave(cls):
        return cls.__time_taken_each_wave
    
    @classmethod
    def add_time_taken_each_wave(cls, time):
        cls.__time_taken_each_wave.append(time)

    @classmethod
    def get_damage_taken(cls):
        return cls.__damage_taken_each_wave.copy()
    
    @classmethod
    def add_damage_taken(cls, damage):
        cls.__damage_taken_each_wave.append(damage)

    @classmethod
    def set_time_taken(cls, _list):
        cls.__time_taken_each_wave = _list

    @classmethod
    def set_damage_taken(cls, _list):
        cls.__damage_taken_each_wave = _list

    def show_weapon(self, screen, enemies):
        mouse_x, mouse_y = pg.mouse.get_pos()
        if self.__is_attacking:
            self.__sword_state += 1
            if self.__sword_state == 5:
                self.__sword_state = 0
                self.__is_attacking = False
            if self.__sword_is_left == 0:
                screen.blit(self.__hitting_effect_left, (self.__position[0] + self.__position_to_player*2 -20, self.__position[1] - 5))
            else:
                screen.blit(self.__hitting_effect_right, (self.__position[0] + self.__position_to_player, self.__position[1] - 5))
        if self.__position[0] > mouse_x:
            self.__sword_is_left = 1
            self.__position_to_player = -50
        elif self.__position[0] <= mouse_x:
            self.__sword_is_left = 0
            self.__position_to_player  = 40
        self.__current_weapon = self.__weapon[self.__sword_is_left][int(self.__sword_state / 2)]
        screen.blit(self.__current_weapon, (self.__position[0] + self.__position_to_player, self.__position[1]))
    
    def get_weapon(self):
        return self.__weapon
        
    def get_damage(self):
        return self.__dmg
    
    def change_dmg(self, dmg):
        self.__dmg += dmg

    def decrease_health(self, decrease_health):
        self.__health -= decrease_health

    def get_health(self):
        return self.__health
    
    def set_health(self, health):
        self.__health = health

    def get_max_health(self):
        return self.__max_health 

    def set_max_health(self, max_health):
        self.__max_health = max_health

    def set_dmg(self, dmg):
        self.__dmg = dmg

    def set_speed(self, speed):
        self.__speed = speed
    
    def get_speed(self):
        return self.__speed

    def get_max_health(self):
        return self.__max_health
    
    def change_max_health(self, health):
        self.__max_health += health

    def get_position(self):
        return self.__position
    
    def set_pos(self,pos):
        self.__position = pos
    
    def get_tuple_position(self):
        return tuple(self.__position)

    def get_pic(self):
        return self.__pic
    
    def set_pic(self, pic):
        self.__pic = pic

    def set_attacking(self, attack):
        self.__attack_style = attack
    
    def get_attacking(self):
        return self.__attack_style
    
    def set_attack_cooldown(self, c):
        self.__attack_cooldown = c

    def get_direction(self):
        return self.__direction
    
    def set_direction(self, direction):
        self.__direction = direction