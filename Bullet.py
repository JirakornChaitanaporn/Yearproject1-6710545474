import pygame as pg
from block import Block

class Bullet:
    __bullet = pg.image.load(r"image\bishop_bullet.png")
    __bullet = pg.transform.scale(__bullet, (80, 5))
    __player_bullet_pic = pg.image.load(r"image\player_bullet.png")
    __player_bullet_pic = pg.transform.scale(__player_bullet_pic, (60, 20))
    __enemy_bullet_list = []
    __player_bullet = []
    
    @staticmethod
    def create_bullet(character, type):
        bullet_position = [character.get_position()[0], character.get_position()[1] + 30]
        new_bullet = Bullet(bullet_position)

        if character.get_direction() == "left":
            new_bullet.set_direction("left")
        elif  character.get_direction() == "right":
            new_bullet.set_direction("right")
        if type == "enemy":
            Bullet.add_enemy_bullet_list(new_bullet)
        elif type == "player":
            Bullet.add_player_bullet(new_bullet) 
    
    @staticmethod
    def bullet_movement(speed, type):
        if type == "enemy":
            for bullet in Bullet.get_enemy_bullet_list():
                position = bullet.get_position()
                if bullet.get_direction() == "left":
                    position[0] -= speed
                elif bullet.get_direction() == "right":
                    position[0] += speed
                bullet.set_position(position)
                if position[0] > 800 or position[0] < 0:
                    Bullet.remove_enemy_bullet_list(bullet)
        elif type == "player":
            for bullet in Bullet.get_player_bullet():
                position = bullet.get_position()
                if bullet.get_direction() == "left":
                    position[0] -= speed
                elif bullet.get_direction() == "right":
                    position[0] += speed
                bullet.set_position(position)
                if position[0] > 800 or position[0] < 0:
                    Bullet.remove_enemy_bullet_list(bullet)

    def __init__(self, position):
        self.__position = [position[0], position[1]]
        self.__direction = ""

    @classmethod
    def bullet_remove_block(cls):
        def collision(bullet_pos: list, block_pos: list) -> bool:
            player_width = 60
            player_height = 60

            if (bullet_pos[0] > block_pos[0] and bullet_pos[0] < block_pos[0] + player_width and
                bullet_pos[1] > block_pos[1] -10 and bullet_pos[1] < block_pos[1] + player_height):
                return True
            return False
        for bullet in cls.get_enemy_bullet_list():
            for block in Block.get_block_list():
                if collision(bullet.get_position(), block.get_position()):
                    cls.remove_enemy_bullet_list(bullet)

        for bullet in cls.get_player_bullet():
            for block in Block.get_block_list():
                if collision(bullet.get_position(), block.get_position()):
                    cls.remove_player_bullet(bullet)

    def get_position(self):
        return self.__position

    def set_position(self, position):
        self.__position = position

    def get_direction(self):
        return self.__direction

    def set_direction(self, direction):
        self.__direction = direction

    @classmethod
    def get_player_bullet_pic(cls):
        return cls.__player_bullet_pic

    @classmethod
    def get_enemy_bullet_list(cls):
        return cls.__enemy_bullet_list
    
    @classmethod
    def clear_enemy_bullet_list(cls):
        cls.__enemy_bullet_list.clear()

    @classmethod
    def add_enemy_bullet_list(cls, bullet):
        cls.__enemy_bullet_list.append(bullet)

    @classmethod
    def remove_enemy_bullet_list(cls, bullet):
        if bullet in cls.__enemy_bullet_list:
            cls.__enemy_bullet_list.remove(bullet)

    @classmethod
    def get_bullet(cls):
        return cls.__bullet
    
    def get_is_hitted_player(self):
        return self.__is_hitted_player

    def set_is_hitted_player(self, value):
        self.__is_hitted_player = value

    @classmethod
    def get_player_bullet(cls):
        return cls.__player_bullet

    @classmethod
    def clear_player_bullet(cls):
        cls.__player_bullet = []

    @classmethod
    def add_player_bullet(cls, bullet):
        cls.__player_bullet.append(bullet)

    @classmethod
    def remove_player_bullet(cls, bullet):
        if bullet in cls.__player_bullet:
            cls.__player_bullet.remove(bullet)

    def __repr__(self):
        return "bullet"