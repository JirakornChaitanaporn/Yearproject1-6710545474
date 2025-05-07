import pygame as pg
from enemies import enemies
import random
from player import Player
import math
from Bullet import Bullet
from skill import EnemiesSkill
from Sound import SoundEffects

class Boss(enemies):
    def __init__(self, player:Player):
        super().__init__(r"image\blackKingLeft.png",2.5, 80)
        self.set_enemy(pg.transform.scale(self.get_enemy(), (60, 60)))
        self._picture = r"image\blackKingLeft.png"
        self.__left_king = pg.transform.scale(pg.image.load(self._picture), (60, 60))
        self._picture = r"image\blackKingRight.png"
        self.__right_king = pg.transform.scale(pg.image.load(self._picture), (60, 60))
        self.__last_attack_time = 0
        if self._position[0] < player.get_position()[0]:
            self.set_enemy(self.__right_king)
            self._direction = "right"
        elif self._position[0] > player.get_position()[0]:
            self.set_enemy(self.__left_king)
            self._direction = "left"

    def movement(self, player: Player):
        if self._position[0] < player.get_position()[0]:
            self.set_enemy(self.__right_king)
            self._direction = "right"
        elif self._position[0] > player.get_position()[0]:
            self.set_enemy(self.__left_king)
            self._direction = "left"
        speed = random.random() + 0.1
        if self._position[0] < player.get_position()[0] - 250:
            self._position[0] += speed
            self._distance_traveled += speed
        elif self._position[0] > player.get_position()[0] + 250:
            self._position[0] -= speed
            self._distance_traveled += speed
        if self._position[1] < player.get_position()[1]:
            self._position[1] += speed
            self._distance_traveled += speed
        elif self._position[1] > player.get_position()[1]:
            self._position[1] -= speed
            self._distance_traveled += speed
            
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

    def attack(self, player: Player):
        def collision(bullet_pos: list, player_pos: list) -> bool:
    # Define the dimensions of the player (e.g., 60x60 as per your original logic)
            player_width = 60
            player_height = 60

            # Check for overlap between the bullet and the player
            if (bullet_pos[0] > player_pos[0] and bullet_pos[0] < player_pos[0] + player_width and
                bullet_pos[1] > player_pos[1] -10 and bullet_pos[1] < player_pos[1] + player_height):
                return True
            return False


        current_time = pg.time.get_ticks()
        if current_time - self.__last_attack_time >= 850:
            if (int(random.random() * 20) + 1) == 1:
                EnemiesSkill.create_player_skill(self)
                SoundEffects.get_instance().play("enemy_shot", 0.05)
            else:
                if self._direction == "right":
                    self._position[0] -= 0.25
                else:
                    self._position[0] += 0.25
                SoundEffects.get_instance().play("enemy_shot", 0.05)
                Bullet.create_bullet(self, "enemy")
                self.__last_attack_time = current_time
        EnemiesSkill.move_enemy_skill()
        Bullet.bullet_movement(4, "enemy")

        for bullet in Bullet.get_enemy_bullet_list():
            if collision(bullet.get_position(), player.get_position()):
                player.decrease_health(1.5)
                self._attack_count += 1
                Bullet.remove_enemy_bullet_list(bullet)

        for skill in EnemiesSkill.get_skill_list():
            if collision(skill.get_position(), player.get_position()):
                SoundEffects.get_instance().play("enemy_shot", 0.1)
                player.decrease_health(2.1)
                self._attack_count += 1
                EnemiesSkill.remove_skill_list(skill)
