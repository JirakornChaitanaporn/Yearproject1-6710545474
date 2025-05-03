import pygame as pg

class PlayerSkill:
    __skill_list = []
    __skill = pg.image.load(r"image\playerSkill.png")
    __skill = pg.transform.scale(__skill, (40, 40))

    def __init__(self, position):
        self.__position = [position[0], position[1]]
        self.__direction = ""

    @staticmethod
    def create_player_skill(player):
        skill_position = [player.get_position()[0], player.get_position()[1] + 30]
        skill_bullet = PlayerSkill(skill_position)

        if player.get_direction() == "left":
            skill_bullet.set_direction("left")
        elif  player.get_direction() == "right":
            skill_bullet.set_direction("right")
        PlayerSkill.add_skill_list(skill_bullet)
    
    @staticmethod
    def move_player_skill(speed = 7):
        for skill in PlayerSkill.get_skill_list():
            position = skill.get_position()
            if skill.get_direction() == "left":
                position[0] -= speed
            elif skill.get_direction() == "right":
                position[0] += speed
            skill.set_position(position)
            if position[0] > 800 or position[0] < 0:
                PlayerSkill.remove_skill_list(skill)

    @classmethod
    def add_skill_list(cls, skill):
        cls.__skill_list.append(skill)
    
    @classmethod
    def remove_skill_list(cls, skill):
        cls.__skill_list.remove(skill)

    @classmethod
    def clear_skill_list(cls):
        cls.__skill_list.clear()

    @classmethod
    def get_skill_list(cls):
        return cls.__skill_list
    
    def get_position(self):
        return self.__position

    def set_position(self, position):
        self.__position = position

    def get_direction(self):
        return self.__direction

    def set_direction(self, direction):
        self.__direction = direction

    @classmethod
    def get_skill(cls):
        return cls.__skill

class EnemiesSkill:
    __skill_list = []
    __skill = pg.image.load(r"image\enemiesSkill.png")
    __skill = pg.transform.scale(__skill, (40, 40))

    def __init__(self, position):
        self.__position = [position[0], position[1]]
        self.__direction = ""

    @staticmethod
    def create_player_skill(enemy):
        skill_position = [enemy.get_position()[0], enemy.get_position()[1] + 30]
        skill_bullet = EnemiesSkill(skill_position)

        if enemy.get_direction() == "left":
            skill_bullet.set_direction("left")
        elif  enemy.get_direction() == "right":
            skill_bullet.set_direction("right")
        EnemiesSkill.add_skill_list(skill_bullet)
    
    @staticmethod
    def move_enemy_skill(speed = 15):
        for skill in EnemiesSkill.get_skill_list():
            position = skill.get_position()
            if skill.get_direction() == "left":
                position[0] -= speed
            elif skill.get_direction() == "right":
                position[0] += speed
            skill.set_position(position)
            if position[0] > 800 or position[0] < 0:
                EnemiesSkill.remove_skill_list(skill)

    @classmethod
    def add_skill_list(cls, skill):
        cls.__skill_list.append(skill)
    
    @classmethod
    def remove_skill_list(cls, skill):
        cls.__skill_list.remove(skill)

    @classmethod
    def clear_skill_list(cls):
        cls.__skill_list.clear()

    @classmethod
    def get_skill_list(cls):
        return cls.__skill_list
    
    def get_position(self):
        return self.__position

    def set_position(self, position):
        self.__position = position

    def get_direction(self):
        return self.__direction

    def set_direction(self, direction):
        self.__direction = direction

    @classmethod
    def get_skill(cls):
        return cls.__skill