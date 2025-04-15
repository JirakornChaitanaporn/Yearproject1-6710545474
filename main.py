import pygame as pg
from config import Config
from player import Player
from blackHorse import BlackHorse
from blackBishop import BlackBishop
from enemies import enemies,Bullet
from block import Block
from boss import Boss
from skill import PlayerSkill, EnemiesSkill

class RunGame:
    def __init__(self):
        pg.init()
        self.__is_run = True
        self.__is_menu = True
        self.__isphase1 = True
        self.__is_created_enemies = False
        self.__isphase2 = True
        self.__isphase3 = True
        self.__is_queen = False
        self.__is_in_shop = False
        self.__is_gameover = False
        self.__key_history = []
        self.__isendless = False
        self.__menu = pg.transform.scale(pg.image.load("menu.png"), (800, 600))
        self.__shop_background = pg.transform.scale(pg.image.load("shop.png"), (800, 600))
        self.__background1 = pg.transform.scale(pg.image.load("bg1.png"), (800, 600))
        self.__background2 = pg.transform.scale(pg.image.load("bg2.png"), (800, 600))
        self.__background3 = pg.transform.scale(pg.image.load("bg3.png"), (800, 600))
        self.__player = Player(
            "whiteRook.png", 
            [[pg.image.load("sword(right_up).png"), pg.image.load("sword(right_down).png")], 
             [pg.image.load("sword(left_up).png"), pg.image.load("sword(left_down).png")]]
        )
        self.__white_queen = pg.transform.scale(pg.image.load("white_queen_right.png"), (50, 50))
        self.__backgrounds = [self.__menu, self.__background1, self.__background2, self.__background3]
        self.__screen = pg.display.set_mode((Config.get('WIN_SIZE_W'), Config.get('WIN_SIZE_H')))
        pg.display.set_caption("Rogue-like Chess")
        pg.display.set_icon(pg.image.load("coolBishop.png"))

    def menu(self):
        pass
    
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
        if self.__key_pressed(pg.K_2) and Player.get_coin() >= 30:
            if not self.__is_queen:
                Player.change_coin(-30)
                self.__player.set_max_health(250.0)
                self.__player.set_speed(5)
                self.__player.set_dmg(15)
                self.__player.set_pic(self.__white_queen)
                self.__player.set_attacking("gun")
                self.__player.set_attack_cooldown(100)
                self.__is_queen = True
        if pg.key.get_pressed()[pg.K_3] and Player.get_coin() >= 5 and self.__player.get_health() < self.__player.get_max_health():
            Player.change_coin(-5)
            self.__player.set_health(self.__player.get_max_health())
        if self.__key_pressed(pg.K_4) and Player.get_coin() >= 15:
            Player.change_coin(-15)
            self.__player.change_max_health(30)

    def reset(self):
        self.__isphase1 = True
        enemies.clear_enemies()
        self.__is_created_enemies = False
        self.__player.set_coin(0)
        self.__player.__init__("whiteRook.png",
            [[pg.image.load("sword(right_up).png"), pg.image.load("sword(right_down).png")], 
             [pg.image.load("sword(left_up).png"), pg.image.load("sword(left_down).png")]])

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
            self.__create_enemies(6, lambda: BlackBishop(self.__player))
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
            self.__create_enemies(2, lambda: Boss(self.__player))
            self.__is_created_enemies = True
        for enemy in enemies.get_enemies_list():
            enemy.movement(self.__player)
            enemy.attack(self.__player)

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
        self.__isendless = False
        

    def game_event(self):
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                self.__is_run = False
        # if self.__is_menu:
        #     self.menu()
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
            
        if self.__player.get_health() <= 0:#when loss
            loss_text = pg.font.Font(None, 36).render("Game Over", True, (0, 0, 0))
            self.__screen.blit(loss_text, (200,200))
            loss_text = pg.font.Font(None, 36).render("Skill Issue", True, (0, 0, 0))
            self.__screen.blit(loss_text, (200,300))
            loss_text = pg.font.Font(None, 36).render("press space to restart", True, (0, 0, 0))
            self.__screen.blit(loss_text, (200,400))
            self.__isphase1 = False
            self.__isphase2 = False
            self.__isphase3 = False
            if pg.key.get_pressed()[pg.K_SPACE]:
                self.reset()

    def draw_game(self):
        if self.__isphase1 or self.__isphase2:
            self.__screen.blit(self.__backgrounds[1], (-self.__player.get_position()[0],0))
            self.__screen.blit(self.__backgrounds[2], (-self.__player.get_position()[0] + 800, 0))
            for enemy in enemies.get_enemies_list():
                self.__screen.blit(enemy.get_enemy(), enemy.get_position())
                enemy.print_health(self.__screen, pg.font.Font(None, 36))
        elif self.__isphase3:
            self.__screen.blit(self.__backgrounds[3], (0,0))
            for enemy in enemies.get_enemies_list():
                self.__screen.blit(enemy.get_enemy(), enemy.get_position())
                enemy.print_health(self.__screen, pg.font.Font(None, 36))
        # elif self.__is_menu:
            # self.__screen.blit(self.__menu_pic, (0, 0))
        self.__screen.blit(self.__player.get_pic(), self.__player.get_tuple_position())#draw player
        # pg.draw.rect(self.__screen, 
        #              (255,255,255), 
        #              (self.__player.get_position()[0], self.__player.get_position()[1], 60, 60))
        self.__player.print_health(self.__screen, pg.font.Font(None, 36))
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
        self.__player.print_coin(self.__screen, pg.font.Font(None, 36))


    def run_game(self):
        while self.__is_run:
            self.game_event()
            self.draw_game()
            pg.display.update()

if __name__ == '__main__':
    g1 = RunGame()
    g1.run_game()
