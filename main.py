import pygame as pg
from config import Config
from player import Player
from blackHorse import BlackHorse
from blackBishop import BlackBishop
from enemies import enemies,Bullet
from block import Block
from boss import Boss
from skill import PlayerSkill, EnemiesSkill
from Sound import SoundEffects
from random import random

class RunGame:
    def __init__(self):
        pg.init()
        self.__is_run = True
        self.__is_menu = True
        self.__isphase1 = False
        self.__is_created_enemies = False
        self.__isphase2 = False
        self.__isphase3 = False
        self.__is_queen = False
        self.__is_in_shop = False
        self.__is_win = False
        self.__is_gameover = False
        self.__key_history = []
        self.__isendless = False
        self.__menu = pg.transform.scale(pg.image.load(r"image\menu.png"), (800, 600))
        self.__shop_background = pg.transform.scale(pg.image.load(r"image\shop.png"), (800, 600))
        self.__background1 = pg.transform.scale(pg.image.load(r"image\bg1.png"), (800, 600))
        self.__background2 = pg.transform.scale(pg.image.load(r"image\bg2.png"), (800, 600))
        self.__background3 = pg.transform.scale(pg.image.load(r"image\bg3.png"), (800, 600))
        self.__player = Player(
            r"image\whiteRook.png", 
            [[pg.image.load(r"image\sword(right_up).png"), pg.image.load(r"image\sword(right_down).png")], 
             [pg.image.load(r"image\sword(left_up).png"), pg.image.load(r"image\sword(left_down).png")]]
        )
        self.__guideline  = pg.transform.scale(pg.image.load(r"image\GuideBook.png"), (800, 600))
        self.__white_queen = pg.transform.scale(pg.image.load(r"image\white_queen_right.png"), (50, 50))
        self.__backgrounds = [self.__menu, self.__background1, self.__background2, self.__background3]
        self.__screen = pg.display.set_mode((Config.get('WIN_SIZE_W'), Config.get('WIN_SIZE_H')))
        pg.display.set_caption("Rogue-like Chess")

    def menu(self):
        Welcome = pg.font.Font(None, 48).render("Welcome to Rogue-like chess", True, (255,255,255))
        play_text = pg.font.Font(None, 36).render("Press E to play", True, (255, 215, 0))
        guide_prompt = pg.font.Font(None, 24).render("Hold h to read guide book", True, (200, 200, 200))
        sound_disable = pg.font.Font(None, 32).render("Press K to disable sound", True, (65,105,255))
        self.__screen.blit(guide_prompt, (285, 375))
        self.__screen.blit(play_text, (295, 250))
        self.__screen.blit(Welcome, (160, 100))
        self.__screen.blit(sound_disable, (255, 450))
        if pg.key.get_pressed()[pg.K_h]:
            self.__screen.blit(self.__guideline, (0,0))
        if self.__key_pressed(pg.K_e):
            self.reset()

    
    def __key_pressed(self, key):
        keys = pg.key.get_pressed()
        if keys[key]:
            if key not in self.__key_history:
                self.__key_history.append(key)
                return True
            return False
        else:
            if key in self.__key_history:
                self.__key_history.remove(key)
            return False

    def shopping_phase(self):
        self.__is_in_shop = True
        if self.__key_pressed(pg.K_1) and Player.get_coin() >= 10:
            Player.change_coin(-10)
            self.__player.change_dmg(2)
        if self.__key_pressed(pg.K_2) and Player.get_coin() >= 30 and not self.__is_queen:
            Player.change_coin(-30)
            self.__player.set_max_health(150.0)
            self.__player.set_speed(5)
            self.__player.set_dmg(15)
            self.__player.set_pic(self.__white_queen)
            self.__player.set_attacking("gun")
            self.__player.set_attack_cooldown(250)
            self.__is_queen = True
        if pg.key.get_pressed()[pg.K_3] and Player.get_coin() >= 5 and self.__player.get_health() < self.__player.get_max_health():
            Player.change_coin(-5)
            self.__player.set_health(self.__player.get_max_health())
        if self.__key_pressed(pg.K_4) and Player.get_coin() >= 15:
            Player.change_coin(-15)
            self.__player.change_max_health(30)

    def reset(self):
        self.__is_win = False
        self.__is_gameover = False
        self.__is_menu = False
        self.__isphase1 = True
        enemies.clear_enemies()
        self.__is_created_enemies = False
        Bullet.clear_enemy_bullet_list()
        Bullet.clear_player_bullet()
        PlayerSkill.clear_skill_list()
        EnemiesSkill.clear_skill_list()
        SoundEffects.get_instance().play("game_start")
        self.__player.set_coin(0)
        self.__player.__init__(r"image\whiteRook.png",
            [[pg.image.load(r"image\sword(right_up).png"), pg.image.load(r"image\sword(right_down).png")], 
             [pg.image.load(r"image\sword(left_up).png"), pg.image.load(r"image\sword(left_down).png")]])

    def __create_enemies(self, n, class_name):
        temporary = None
        for i in range(n):
            temporary = class_name()
            enemies.add_enemies(temporary)

    def phase1(self):
        if not self.__is_created_enemies:
            self.__create_enemies(5, lambda: BlackHorse())
            self.__is_created_enemies = True
        self.__player.player_movement(self.__is_in_shop)
        self.__player.player_attack(enemies.get_enemies_list())
        if Player.get_coin() == 30:
            Player.set_coin(29)
        for enemy in enemies.get_enemies_list():
            enemy.movement(self.__player)
            enemy.attack(self.__player)
        if len(enemies.get_enemies_list()) == 0 and self.__is_created_enemies:
            self.shopping_phase()
            if pg.key.get_pressed()[pg.K_x]:
                self.__player.set_speed(2.5)
                self.__is_in_shop = False
                self.__is_created_enemies = False
                self.__is_in_shop = False
                self.__isphase1 = False
                self.__isphase2 = True

    def phase2(self):
        if not self.__is_created_enemies:
            self.__create_enemies(9, lambda: BlackBishop(self.__player))
            self.__is_created_enemies = True
        self.__player.player_movement(self.__is_in_shop)
        self.__player.player_attack(enemies.get_enemies_list())
        for enemy in enemies.get_enemies_list():
            enemy.movement(self.__player)
            enemy.attack(self.__player)
        if len(enemies.get_enemies_list()) == 0 and self.__is_created_enemies:
            Bullet.clear_enemy_bullet_list()
            Bullet.clear_player_bullet()
            self.shopping_phase()
            if pg.key.get_pressed()[pg.K_x]:
                self.__is_in_shop = False
                self.__is_created_enemies = False
                self.__is_in_shop = False
                self.__isphase2 = False
                self.__isphase3 = True

    def boss_phase(self):
        if not self.__is_created_enemies:
            self.__create_enemies(3, lambda: Boss(self.__player))
            self.__is_created_enemies = True

        if len(Block.get_block_list()) < 4:
            temp = Block()
            Block.add_block_list(temp)

        for enemy in enemies.get_enemies_list():
            enemy.movement(self.__player)
            enemy.attack(self.__player)

        Bullet.bullet_remove_block()
        self.__player.player_movement(self.__is_in_shop)
        self.__player.player_attack(enemies.get_enemies_list())
        if len(enemies.get_enemies_list()) == 0 and self.__is_created_enemies:
            Bullet.clear_enemy_bullet_list()
            Bullet.clear_player_bullet()
            self.__is_gameover = True

    def endlessmode(self):
        pass

    def gameover(self):
        self.__isphase3 = False
        self.__is_win = True
        

    def game_event(self):
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                self.__is_run = False
        if self.__isphase1:
            self.phase1()
        elif self.__isphase2:
            self.phase2()
        elif self.__isphase3:
            self.boss_phase()
        elif self.__isendless:
            self.endlessmode()
        if self.__is_gameover:
            self.gameover()
        if self.__key_pressed(pg.K_q):
            if SoundEffects.get_available_sound():
                SoundEffects.set_available_sound(False)
            else:
                SoundEffects.set_available_sound(True)
        
            
        if self.__player.get_health() <= 0:#when loss
            loss_text = pg.font.Font(None, 36).render("Game Over", True, (0, 0, 0))
            self.__screen.blit(loss_text, (200,200))
            loss_text = pg.font.Font(None, 36).render("Skill Issue", True, (0, 0, 0))
            self.__screen.blit(loss_text, (200,300))
            loss_text = pg.font.Font(None, 36).render("press 'r' to restart", True, (0, 0, 0))
            self.__screen.blit(loss_text, (200,400))
            self.__isphase1 = False
            self.__isphase2 = False
            self.__isphase3 = False
            SoundEffects.get_instance().play("game_loss")
            if pg.key.get_pressed()[pg.K_r]:
                self.reset()
        elif self.__is_win:
            win_text = pg.font.Font(None, 36).render("Game Over", True, (0, 0, 0))
            self.__screen.blit(win_text, (200,200))
            win_text = pg.font.Font(None, 36).render("You win", True, (0, 0, 0))
            self.__screen.blit(win_text, (200,350))
            win_text = pg.font.Font(None, 36).render("press 'r' to restart", True, (0, 0, 0))
            self.__screen.blit(win_text, (200,550))
            self.__isphase1 = False
            self.__isphase2 = False
            self.__isphase3 = False
            SoundEffects.get_instance().play("game_win")
            if pg.key.get_pressed()[pg.K_r]:
                self.reset()

    def draw_game(self):
        back_layer = pg.Surface([800,600], pg.SRCALPHA, 32)
        back_layer = back_layer.convert_alpha()
        self.__screen.blit(back_layer, (0,0))
        if self.__isphase1 or self.__isphase2:
            self.__screen.blit(self.__backgrounds[1], (-self.__player.get_position()[0],0))
            self.__screen.blit(self.__backgrounds[2], (-self.__player.get_position()[0] + 800, 0))
            for enemy in enemies.get_enemies_list():
                if self.__isphase1:
                    radius = 69
                    circle_surf = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
                    pg.draw.circle(
                        circle_surf,
                        (200, 0, 0, 128),
                        (radius, radius),
                        radius
                    )
                    enemy_x, enemy_y = enemy.get_position()
                    self.__screen.blit(
                        circle_surf,
                        (enemy_x + 30 - radius, enemy_y + 30 - radius)
                    )
                    enemy.print_health(self.__screen, 10)
                else:
                    enemy.print_health(self.__screen, 30)
                self.__screen.blit(enemy.get_enemy(), enemy.get_position())
        elif self.__isphase3:
            self.__screen.blit(self.__backgrounds[3], (0,0))
            for enemy in enemies.get_enemies_list():
                self.__screen.blit(enemy.get_enemy(), enemy.get_position())
                enemy.print_health(self.__screen, 120)
            for block in Block.get_block_list():
                self.__screen.blit(Block.get_block(), block.get_position())
        elif self.__is_menu:
            self.__screen.blit(self.__menu, (0, 0))
            self.menu()
        if not self.__is_menu:
            self.__screen.blit(self.__player.get_pic(), self.__player.get_tuple_position())
            self.__player.print_health(self.__screen)
        if (self.__player.get_attacking() == "melee") and enemies.get_enemies_list():
            self.__player.show_weapon(self.__screen, enemies.get_enemies_list()[0])
        for bullet in Bullet.get_enemy_bullet_list():
            self.__screen.blit(Bullet.get_bullet(), tuple(bullet.get_position()))
        for bullet in Bullet.get_player_bullet():
            self.__screen.blit(Bullet.get_player_bullet_pic(), tuple(bullet.get_position()))
        for skill in PlayerSkill.get_skill_list():
            self.__screen.blit(PlayerSkill.get_skill(), tuple(skill.get_position()))
        for skill in EnemiesSkill.get_skill_list():
            self.__screen.blit(EnemiesSkill.get_skill(), tuple(skill.get_position()))
        if self.__is_in_shop:
            self.__screen.blit(self.__shop_background,(0,0))
            self.__player.print_stat(self.__screen, pg.font.Font(None, 42))
        if self.__is_in_shop: 
            self.__player.print_coin(self.__screen, pg.font.Font(None, 36))

        #sound
        sound_status = pg.font.Font(None, 28).render(f"Sound is playing: {SoundEffects.get_available_sound()}", True,\
                                    (0,255,0))
        self.__screen.blit(sound_status,\
                           sound_status.get_rect(bottomright=(800 - 10, 600 - 10)))


    def run_game(self):
        while self.__is_run:
            self.game_event()
            self.draw_game()
            pg.display.update()

if __name__ == '__main__':
    g1 = RunGame()
    g1.run_game()
