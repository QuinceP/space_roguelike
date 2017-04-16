import math
import os
import random
import sys
from pprint import pprint
from generator import dMap
import numpy
import pygame
from pygame.locals import *


def load_image(name):
    """ Load image and return image object"""
    fullname = os.path.join('', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    return image


class Sprite(pygame.sprite.Sprite):
    def __init__(self, images, x, y):
        super(Sprite, self).__init__()
        self.x = x
        self.y = y
        self.counter = 0
        self.imageArray = []
        for i in range(0, len(images)):
            self.imageArray.append(load_image(images[i]))

        self.index = 0
        self.image = self.imageArray[self.index]
        self.facing_right = -1

    def update(self):
        self.counter += 1

        if self.counter == 5:
            self.index += 1
            self.counter = 0

        if self.index >= len(self.imageArray):
            self.index = 0

        self.image = self.imageArray[self.index]
        self.flip()
        DISPLAYSURF.blit(self.image, (self.x * TILESIZE, self.y * TILESIZE))

    def flip(self):
        self.image = pygame.transform.flip(self.image, self.facing_right, False)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h


class Tile():
    def __init__(self, name, sprite, z_level, is_passable):
        self.name = name
        self.sprite = pygame.image.load(sprite)
        self.z_level = z_level
        self.is_passable = is_passable

    def __repr__(self):
        return "<Tile name:%s sprite:%s z_level:%s is_passable:%s>" % (
            self.name, self.sprite, self.z_level, self.is_passable)


FLOOR = Tile('floor', 'oryx_16bit_scifi_world_01.png', 1, True)
GRASS = Tile('grass', 'grass0.png', 1, True)
WATER = Tile('water', 'water0.png', 1, False)
DOOR = Tile('door', 'oryx_16bit_scifi_world_481.png', 1, True)
OPEN_DOOR = Tile('open_door', 'oryx_16bit_scifi_world_1106.png', 1, True)
WALLS = [
    Tile('wall_top_left', 'oryx_16bit_scifi_world_14.png', 1, False),
    Tile('wall_top_right', 'oryx_16bit_scifi_world_15.png', 1, False),
    Tile('wall_bottom_left', 'oryx_16bit_scifi_world_16.png', 1, False),
    Tile('wall_bottom_right', 'oryx_16bit_scifi_world_17.png', 1, False),
    Tile('wall_vertical', 'oryx_16bit_scifi_world_12.png', 1, False),
    Tile('wall_horizontal', 'oryx_16bit_scifi_world_09.png', 1, False)
]
BACKGROUND = [
    Tile('empty_space', 'oryx_16bit_scifi_world_965.png', 0, False),
    Tile('double_stars', 'oryx_16bit_scifi_world_966.png', 0, False),
    Tile('single_star', 'oryx_16bit_scifi_world_967.png', 0, False),
    Tile('big_star', 'oryx_16bit_scifi_world_968.png', 0, False)
]
BACKGROUND_WEIGHTS = [0.85, 0.05, 0.08, 0.02]


def quitGame():
    pygame.quit()
    sys.exit()


# useful game dimensions
TILESIZE = 24
MAPWIDTH = 40
MAPHEIGHT = 40

# constants representing colours
BLACK = (0, 0, 0)
BROWN = (153, 76, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# set up the display
pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH * TILESIZE, MAPHEIGHT * TILESIZE))

# the player image
PLAYER = Sprite(['oryx_16bit_scifi_creatures_01.png', 'oryx_16bit_scifi_creatures_02.png'],
                math.floor((MAPWIDTH / 2) - 1),
                math.floor((MAPHEIGHT / 2) - 1))

clock = pygame.time.Clock()
startx = MAPWIDTH
starty = MAPHEIGHT

themap = dMap()
themap.makeMap(startx, starty, 110, 50, 60)

map = []
for y in range(starty):
    line = []
    for x in range(startx):
        if themap.mapArr[y][x] == 0:
            # line += "."
            line.append(FLOOR)
        if themap.mapArr[y][x] == 1:
            # line += " "
            line.append(numpy.random.choice(BACKGROUND, p=BACKGROUND_WEIGHTS))
        if themap.mapArr[y][x] == 2:
            # line += "#"
            line.append(WALLS[5])
        if themap.mapArr[y][x] == 3 or themap.mapArr[y][x] == 4 or themap.mapArr[y][x] == 5:
            # line += "="
            line.append(DOOR)
        if themap.mapArr[y][x] == 6:
            line.append(WALLS[0])
        if themap.mapArr[y][x] == 7:
            line.append(WALLS[2])
        if themap.mapArr[y][x] == 8:
            line.append(WALLS[1])
        if themap.mapArr[y][x] == 9:
            line.append(WALLS[3])
        if themap.mapArr[y][x] == 10:
            line.append(WALLS[5])
        if themap.mapArr[y][x] == 11:
            line.append(WALLS[4])
    map.append(line)

while True:
    clock.tick(12)

    keys = pygame.key.get_pressed()
    if (keys[K_RIGHT]) and PLAYER.x < MAPWIDTH - 1:
        PLAYER.facing_right = True
        try:
            passable = map[PLAYER.x + 1][PLAYER.y].is_passable
        except IndexError:
            passable = False

        if passable:
            PLAYER.move(1, 0)
    if (keys[K_LEFT]) and PLAYER.x > 0:
        PLAYER.facing_right = False
        try:
            passable = map[PLAYER.x - 1][PLAYER.y].is_passable
        except IndexError:
            passable = False

        if passable:
            PLAYER.move(-1, 0)

    if (keys[K_UP]) and PLAYER.y > 0:

        try:
            passable = map[PLAYER.x][PLAYER.y - 1].is_passable
        except IndexError:
            passable = False
        if passable:
            PLAYER.move(0, -1)
    if (keys[K_DOWN]) and PLAYER.y < MAPHEIGHT - 1:
        try:
            passable = map[PLAYER.x][PLAYER.y + 1].is_passable
        except IndexError:
            passable = False

        try:
            is_door = (map[PLAYER.x][PLAYER.y + 1] == DOOR)
        except IndexError:
            is_door = False

        if is_door:
            map[PLAYER.x][PLAYER.y + 1] = OPEN_DOOR

        if passable:
            PLAYER.move(0, 1)

    # get all the user events
    for event in pygame.event.get():
        if event.type == QUIT:
            quitGame()

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quitGame()

    DISPLAYSURF.fill((0, 0, 0))
    for row in range(MAPWIDTH):
        for column in range(MAPHEIGHT):
            DISPLAYSURF.blit(map[column][row].sprite, (column * TILESIZE, row * TILESIZE))

    PLAYER.update()

    pygame.display.update()
