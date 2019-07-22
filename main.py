import pygame
import random
from copy import deepcopy

def draw_text(surf, text, size, x, y):
    COLOR = (100,100,200)
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, COLOR)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE=(0,0,255)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 10
TITLE = "Tilemap Demo"
BGCOLOR = DARKGREY

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

import pygame as pg

class Cube(pg.sprite.Sprite):
    def __init__(self, game, x, y,dirx=0,diry=0):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.dirx=dirx
        self.diry=diry
        self.last_moved=0

    def collide_with_walls(self):
        for wall in self.game.walls:
            if wall.x == self.x + self.dirx and wall.y == self.y + self.diry:
                return True
        return False

    def update(self):

        for indexbruh,cube in enumerate(self.game.player):
            if self.game.player[0].x + self.game.player[0].dirx==cube.x and self.game.player[0].y + self.game.player[0].diry==cube.y :
                if indexbruh!=0:
                    self.game.playing=False


        if not self.game.player[0].collide_with_walls() :
            self.x += self.dirx
            self.y += self.diry
            if self.y>GRIDHEIGHT:
                self.y=0
            elif self.y<0:
                self.y=GRIDHEIGHT
            if self.x>GRIDWIDTH:
                self.x=0
            elif self.x<0:
                self.x=GRIDWIDTH
            self.last_moved=pg.time.get_ticks()
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
# KidsCanCode - Game Development with Pygame video series
# Tile-based game - Part 2
# Collisions and Tilemaps
# Video link: https://youtu.be/ajR4BZBKTr4
import pygame as pg
import sys
from os import path


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.turns=[]
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.highscore=0
        self.fruitwithd=32
        self.nowalls=[]
        self.player=[]


    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                else:
                    if tile == 'P':
                        self.player=[Cube(self,col,row)]
                        self.player[0].dirx=1
                        self.player[0].diry=0
                        for i in range(25):
                            self.player.append(Cube(self,self.player[len(self.player)-1].x-self.player[len(self.player)-1].dirx,self.player[len(self.player)-1].y-self.player[len(self.player)-1].diry,self.player[len(self.player)-1].dirx,self.player[len(self.player)-1].diry))

                    self.nowalls.append((col,row))
        posforfruit=random.choice(self.nowalls)
        self.fruitx=posforfruit[0]
        self.fruity=posforfruit[1]
        self.player[0].image.fill(BLUE)



    def run(self):


        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            print(FPS)
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop

        for pos_in_list,cube in enumerate(self.player):
            for med_list in self.turns:
                if med_list[0][0]==cube.x and med_list[0][1]==cube.y:
                    self.player[pos_in_list].dirx=med_list[1][0]
                    self.player[pos_in_list].diry=med_list[1][1]
                    if pos_in_list==len(self.player)-1:
                        self.turns.remove(med_list)

        if self.player[0].x==self.fruitx and self.player[0].y==self.fruity:
            self.player.append(Cube(self,self.player[len(self.player)-1].x-self.player[len(self.player)-1].dirx,self.player[len(self.player)-1].y-self.player[len(self.player)-1].diry,self.player[len(self.player)-1].dirx,self.player[len(self.player)-1].diry))
            score=len(self.player)-1
            if score-(score//2*2)==0:
                global FPS
                FPS+=1
            posforfruit=random.choice(self.nowalls)
            self.fruitx=posforfruit[0]
            self.fruity=posforfruit[1]

        for i in range(len(self.player)-1,-1,-1):
            self.player[i].update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        draw_text(self.screen,"Yyour score is {} while your high score is {} ".format(len(self.player)-1,FPS),40,WIDTH//2,30)
        pg.draw.rect(self.screen,RED,(self.fruitx*32,self.fruity*32, self.fruitwithd, self.fruitwithd))
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                elif event.key == pg.K_LEFT and self.player[0].dirx!=1:

                        self.player[0].dirx=-1
                        self.player[0].diry=0
                        if not self.player[0].collide_with_walls()   :
                            self.turns.append([[self.player[0].x,self.player[0].y],[self.player[0].dirx, self.player[0].diry]])

                elif event.key == pg.K_RIGHT and self.player[0].dirx!=-1:

                        self.player[0].dirx=1
                        self.player[0].diry=0
                        if not self.player[0].collide_with_walls()   :
                            self.turns.append([[self.player[0].x,self.player[0].y],[self.player[0].dirx, self.player[0].diry]])

                elif event.key == pg.K_UP and self.player[0].diry!=1 and self.player[0].diry!=-1:

                        self.player[0].diry=-1
                        self.player[0].dirx=0
                        if not self.player[0].collide_with_walls()   :
                            self.turns.append([[self.player[0].x,self.player[0].y],[self.player[0].dirx, self.player[0].diry]])

                elif event.key == pg.K_DOWN and self.player[0].diry!=-1:

                        self.player[0].diry=1
                        self.player[0].dirx=0
                        if not self.player[0].collide_with_walls()   :
                            self.turns.append([[self.player[0].x,self.player[0].y],[self.player[0].dirx, self.player[0].diry]])



    def show_start_screen(self):
        while True:
            self.screen.fill(BLACK)
            draw_text(self.screen,"hello,welcome to THE SNAKE GAME",60,WIDTH//2,250)
            draw_text(self.screen,"You know how to play, GOOD LUCK",60,WIDTH//2,HEIGHT//2+100)
            pygame.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                elif event.type == pg.KEYDOWN:
                        return None

    def show_go_screen(self):
         if len(self.player)>self.highscore:
                self.highscore=len(self.player)

         while True:
            self.screen.fill(BLACK)
            draw_text(self.screen,"looks like you failed!!!",60,WIDTH//2,250)
            draw_text(self.screen,"Yyour score was {} while your high score is {} ".format(len(self.player),self.highscore),60,WIDTH//2,HEIGHT//2+100)
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                elif event.type == pg.KEYDOWN:
                        pg.init()
                        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
                        self.turns=[]
                        pg.display.set_caption(TITLE)
                        self.clock = pg.time.Clock()
                        self.load_data()
                        self.highscore=0
                        self.fruitwithd=32
                        self.nowalls=[]
                        return None
pygame.mixer.init()
snd_dir = path.join(path.dirname(__file__), 'snd')
pygame.mixer.music.load(path.join(snd_dir, 'country rap.wav'))
pygame.mixer.music.play(loops=-1)
# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
