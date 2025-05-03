import pygame as pg
from enemies  import enemies
from player import Player
import random
import math
from Bullet import Bullet
from Sound import SoundEffects

class BlackBishop(enemies):
    def __init__(self,player:Player):
        super().__init__(r"image\blackBishopLeft.png", 3, 30.0)
        self.set_enemy(pg.transform.scale(self.get_enemy(), (60, 60)))
        self._picture = r"image\blackBishopLeft.png"
        self.__left_bishop = pg.transform.scale(pg.image.load(self._picture), (60, 60))
        self._picture = r"image\blackBishopRight.png"
        self.__right_bishop = pg.transform.scale(pg.image.load(self._picture), (60, 60))
        self.__last_attack_time = 0
        if self._position[0] < player.get_position()[0]:
            self.set_enemy(self.__right_bishop)
            self._direction = "right"
        elif self._position[0] > player.get_position()[0]:
            self.set_enemy(self.__left_bishop)
            self._direction = "left"

    def movement(self, player: Player):
        speed = random.random()
        if self._position[1] < player.get_position()[1] - 5:
            if random.randint(0,1) == 0:
                self._position[0] -= (speed)
                self._distance_traveled += (speed)
            else:
                self._position[0] += speed
                self._distance_traveled += (speed)
            self._position[1] += speed
            self._distance_traveled += (speed)
        elif self._position[1] > player.get_position()[1] + 5:
            if random.randint(0,1) == 0:
                self._position[0] -= speed
                self._distance_traveled += (speed)
            else:
                self._position[0] += speed
                self._distance_traveled += (speed)
            self._position[1] -= speed
            self._distance_traveled += (speed)

        if self._position[0] < player.get_position()[0]:
            self.set_enemy(self.__right_bishop)
            self._direction = "right"
        elif self._position[0] > player.get_position()[0]:
            self.set_enemy(self.__left_bishop)
            self._direction = "left"
        if self._position[0] < player.get_position()[0] - 200:
            if self._position[1] < player.get_position()[1]:
                self._position[0] += speed
                self._position[1] += speed
            elif self._position[1] > player.get_position()[1]:
                self._position[0] += speed
                self._position[1] -= speed
            self._distance_traveled += math.sqrt(speed**2 + speed**2)
        elif self._position[0] > player.get_position()[0] + 200:
            if self._position[1] < player.get_position()[1]:
                self._position[0] -= speed
                self._position[1] += speed
            elif self._position[1] > player.get_position()[1]:
                self._position[0] -= speed
                self._position[1] -= speed
            self._distance_traveled += math.sqrt(speed**2 + speed**2)

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
                    # self._position[0] += dx * repulsion_strength
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
        if current_time - self.__last_attack_time >= 2000:
            Bullet.create_bullet(self, "enemy")
            self.__last_attack_time = current_time
        Bullet.bullet_movement(2,"enemy")

        for bullet in Bullet.get_enemy_bullet_list():
            if collision(bullet.get_position(), player.get_position()):
                SoundEffects.get_instance().play("enemy_shot")
                player.decrease_health(5)
                self._attack_count += 1
                Bullet.remove_enemy_bullet_list(bullet)

    def get_right_bishop(self):
        return self.__right_bishop
    
    def get_left_bishop(self):
        return self.__left_bishop
