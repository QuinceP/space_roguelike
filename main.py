import math
import os
import random
import sys
from pprint import pprint

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


def create_room(room):
    # go through the tiles in the rectangle and make them passable
    for x in range(room.x1 - 1, room.x2 + 1):
        for y in range(room.y1 - 1, room.y2 + 1):
            if x == room.x1 - 1 and y == room.y1 - 1:  # top left corner
                tilemap[x][y] = WALLS[0]
            elif x == room.x1 - 1 and y == room.y2:  # bottom left corner
                tilemap[x][y] = WALLS[2]
            elif x == room.x2 and y == room.y1 - 1:  # top right corner
                tilemap[x][y] = WALLS[1]
            elif x == room.x2 and y == room.y2:  # bottom right corner
                tilemap[x][y] = WALLS[3]
            elif x == room.x1 - 1 or x == room.x2:  # horizontal
                tilemap[x][y] = WALLS[4]
            elif y == room.y1 - 1 or y == room.y2:  # vertical
                tilemap[x][y] = WALLS[5]
            else:
                tilemap[x][y] = FLOOR

def scan_for_room(room):
    for x in range(room.x1 - 1, room.x2 + 1):
        for y in range(room.y1 - 1, room.y2 + 1):
            try:
                if tilemap[x][y].z_level != 0:
                    return False
            except IndexError:
                return False

    if room.x1 <= 0 or room.x2 >= MAPWIDTH - 1 or room.y1 <= 0 or room.y2 >= MAPHEIGHT - 1:
        return False

    return True

def pick_wall(room):
    direction = 'west'
    # direction = random.choice(['north', 'east', 'south', 'west'])
    edge = 0
    x = 0
    y = 0
    if direction == 'north':
        x = random.randint(room.x1, room.x2 - 1)
        y = room.y1 - 1

    elif direction == 'east':
        x = room.x2
        y = random.randint(room.y1, room.y2 - 1)

    elif direction == 'south':
        x = random.randint(room.x1, room.x2 - 1)
        y = room.y2

    elif direction == 'west':
        x = room.x1 - 1
        y = random.randint(room.y1, room.y2 - 1)

    if x == room.x1 or y == room.y1:
        edge = 1
    elif x == room.x2 - 1 or y == room.y2 - 1:
        edge = 2

    return x, y, direction, edge


def create_corridor(wall_x, wall_y, direction, edge, corridor_length):
    if direction == 'north':
        if wall_y - corridor_length > 0:
            for i in range(wall_x - 1, wall_x + 2):
                for j in range(wall_y - corridor_length, wall_y + 1):
                    if i == wall_x:
                        if j == wall_y:
                            tilemap[i][j] = DOOR
                        else:
                            tilemap[i][j] = FLOOR
                    else:
                        if j == wall_y:
                            if i == wall_x + 1:
                                if edge == 2:
                                    tilemap[i][j] = WALLS[4]
                                else:
                                    tilemap[i][j] = WALLS[2]
                            elif i == wall_x - 1:
                                if edge == 1:
                                    tilemap[i][j] = WALLS[4]
                                else:
                                    tilemap[i][j] = WALLS[3]
                        else:
                            tilemap[i][j] = WALLS[4]
    elif direction == 'east':
        if wall_x + corridor_length < MAPWIDTH:
            for i in range(wall_x, wall_x + corridor_length):
                for j in range(wall_y - 1, wall_y + 2):
                    if j == wall_y:
                        if i == wall_x:
                            tilemap[i][j] = DOOR
                        else:
                            tilemap[i][j] = FLOOR
                    else:
                        if i == wall_x:
                            if j == wall_y + 1:
                                if edge == 2:
                                    tilemap[i][j] = WALLS[5]
                                else:
                                    tilemap[i][j] = WALLS[0]
                            elif j == wall_y - 1:
                                if edge == 1:
                                    tilemap[i][j] = WALLS[5]
                                else:
                                    tilemap[i][j] = WALLS[2]
                        else:
                            tilemap[i][j] = WALLS[5]
    elif direction == 'south':
        if wall_y + corridor_length < MAPHEIGHT:
            for i in range(wall_x - 1, wall_x + 2):
                for j in range(wall_y, wall_y + corridor_length):
                    if i == wall_x:
                        if j == wall_y:
                            tilemap[i][j] = DOOR
                        else:
                            tilemap[i][j] = FLOOR
                    else:
                        if j == wall_y:
                            if i == wall_x + 1:
                                if edge == 2:
                                    tilemap[i][j] = WALLS[4]
                                else:
                                    tilemap[i][j] = WALLS[0]
                            elif i == wall_x - 1:
                                if edge == 1:
                                    tilemap[i][j] = WALLS[4]
                                else:
                                    tilemap[i][j] = WALLS[1]
                        else:
                            tilemap[i][j] = WALLS[4]
    elif direction == 'west':
        if wall_x - corridor_length > 0:
            for i in range(wall_x - corridor_length, wall_x + 1):
                for j in range(wall_y - 1, wall_y + 2):
                    if j == wall_y:
                        if i == wall_x:
                            tilemap[i][j] = DOOR
                        else:
                            tilemap[i][j] = FLOOR
                    else:
                        if i == wall_x:
                            if j == wall_y + 1:
                                if edge == 2:
                                    tilemap[i][j] = WALLS[5]
                                else:
                                    tilemap[i][j] = WALLS[1]
                            elif j == wall_y - 1:
                                if edge == 1:
                                    tilemap[i][j] = WALLS[5]
                                else:
                                    tilemap[i][j] = WALLS[3]
                        else:
                            tilemap[i][j] = WALLS[5]


def scan_for_corridor(wall_x, wall_y, direction):
    corridor_length = random.randint(3, 10)
    if direction == 'north':
        if wall_y - corridor_length > 0:
            for i in range(wall_x - 1, wall_x + 2):
                for j in range(wall_y - corridor_length, wall_y):
                    if tilemap[i][j].z_level != 0:
                        pprint(tilemap[i][j])
                        return 0
    elif direction == 'east':
        if wall_x + corridor_length < MAPWIDTH:
            for i in range(wall_x + 1, wall_x + corridor_length):
                for j in range(wall_y - 1, wall_y + 2):
                    if tilemap[i][j].z_level != 0:
                        pprint(tilemap[i][j])
                        return 0
    elif direction == 'south':
        if wall_y + corridor_length < MAPHEIGHT:
            for i in range(wall_x - 1, wall_x + 2):
                for j in range(wall_y + 1, wall_y + corridor_length):
                    if tilemap[i][j].z_level != 0:
                        pprint(tilemap[i][j].z_level)
                        return 0
    elif direction == 'west':
        if wall_x - corridor_length > 0:
            for i in range(wall_x - corridor_length, wall_x):
                for j in range(wall_y - 1, wall_y + 2):
                    if tilemap[i][j].z_level != 0:
                        pprint(tilemap[i][j])
                        return 0

    return corridor_length


def generate_door(room_x, room_y, room_height, room_width):
    wall_x = random.choice([room_x - 1, room_x + room_width - 1])
    wall_y = random.choice([room_y - 1, room_y + room_height - 1])
    if ((wall_x == room_x and wall_y == room_y) or (
                    wall_x == room_x + room_width - 1 and wall_y == room_y + room_height - 1)):
        return generate_door(room_x, room_y, room_height, room_width)
    else:
        return [wall_x, wall_y]


def generate_tilemap():
    global tilemap
    tilemap = [[numpy.random.choice(BACKGROUND, p=BACKGROUND_WEIGHTS) for height in range(MAPHEIGHT)] for width in
               range(MAPWIDTH)]

    starting_room_width = 5
    starting_room_height = 5
    starting_room_x = math.floor(MAPWIDTH / 2) - starting_room_width + math.floor(starting_room_width / 2)
    starting_room_y = math.floor(MAPHEIGHT / 2) - starting_room_height + math.floor(starting_room_height / 2)

    starting_room = Rect(starting_room_x, starting_room_y, starting_room_width, starting_room_height)
    create_room(starting_room)
    wall_x, wall_y, direction, edge = pick_wall(starting_room)

    available_cooridor_length = scan_for_corridor(wall_x, wall_y, direction)
    if available_cooridor_length != 0:
        create_corridor(wall_x, wall_y, direction, edge, available_cooridor_length)
    else:
        print("blocked!")

    if direction == 'north':
        new_room = Rect(wall_x, wall_y - 2 * (available_cooridor_length) - 1, available_cooridor_length, available_cooridor_length)
        print(scan_for_room(new_room))
        if scan_for_room(new_room):
            create_room(new_room)
            tilemap[wall_x][wall_y - available_cooridor_length - 1] = DOOR
    elif direction == 'east':
        y = random.randint(0, 3)
        new_room = Rect(wall_x + available_cooridor_length + 1, wall_y - y, random.randint(4, 10), random.randint(4, 10))
        print(scan_for_room(new_room))
        if scan_for_room(new_room):
            create_room(new_room)
            tilemap[wall_x + available_cooridor_length][wall_y] = DOOR
    elif direction == 'south':
        x = random.randint(0, 3)
        new_room = Rect(wall_x - x, wall_y + available_cooridor_length + 1, random.randint(4, 10), random.randint(4, 10))
        print(scan_for_room(new_room))
        if scan_for_room(new_room):
            create_room(new_room)
            tilemap[wall_x][wall_y + available_cooridor_length] = DOOR
    elif direction == 'west':
        y = random.randint(0, 3)
        new_room = Rect(wall_x - 2 * available_cooridor_length - 1, wall_y - y, random.randint(4, 10), random.randint(4, 10))
        print(scan_for_room(new_room))
        if scan_for_room(new_room):
            create_room(new_room)
            tilemap[wall_x - available_cooridor_length - 1][wall_y] = DOOR

    return tilemap


# class Player:
#     health = 100
#
#     def __init__(self):


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

tilemap = generate_tilemap()

while True:
    clock.tick(12)

    keys = pygame.key.get_pressed()
    if (keys[K_RIGHT]) and PLAYER.x < MAPWIDTH - 1:
        PLAYER.facing_right = True
        try:
            passable = tilemap[PLAYER.x + 1][PLAYER.y].is_passable
        except IndexError:
            passable = False

        if passable:
            PLAYER.move(1, 0)
    if (keys[K_LEFT]) and PLAYER.x > 0:
        PLAYER.facing_right = False
        try:
            passable = tilemap[PLAYER.x - 1][PLAYER.y].is_passable
        except IndexError:
            passable = False

        if passable:
            PLAYER.move(-1, 0)

    if (keys[K_UP]) and PLAYER.y > 0:

        try:
            passable = tilemap[PLAYER.x][PLAYER.y - 1].is_passable
        except IndexError:
            passable = False
        if passable:
            PLAYER.move(0, -1)
    if (keys[K_DOWN]) and PLAYER.y < MAPHEIGHT - 1:
        try:
            passable = tilemap[PLAYER.x][PLAYER.y + 1].is_passable
        except IndexError:
            passable = False

        try:
            is_door = (tilemap[PLAYER.x][PLAYER.y + 1] == DOOR)
        except IndexError:
            is_door = False

        if is_door:
            tilemap[PLAYER.x][PLAYER.y + 1] = OPEN_DOOR

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
    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            DISPLAYSURF.blit(tilemap[column][row].sprite, (column * TILESIZE, row * TILESIZE))

    PLAYER.update()

    pygame.display.update()
