import pygame, sys, math, numpy, random
from numpy.random import choice
from pygame.locals import *


def load_image(name):
    image = pygame.image.load(name).convert_alpha()
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
        '''This method iterates through the elements inside self.images and
        displays the next one each tick. For a slower animation, you may want to
        consider using a timer of some sort so it updates slower.'''
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


FLOOR = Tile('floor', 'oryx_16bit_scifi_world_01.png', 1, True)
GRASS = Tile('grass', 'grass0.png', 1, True)
WATER = Tile('water', 'water0.png', 1, True)
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
            if (x == room.x1 - 1 and y == room.y1 - 1):  # top left corner
                map[x][y] = WALLS[0]
            elif (x == room.x1 - 1 and y == room.y2):  # bottom left corner
                map[x][y] = WALLS[2]
            elif (x == room.x2 and y == room.y1 - 1):  # top right corner
                map[x][y] = WALLS[1]
            elif (x == room.x2 and y == room.y2):  # bottom right corner
                map[x][y] = WALLS[3]
            elif (x == room.x1 - 1 or x == room.x2):  # horizontal
                map[x][y] = WALLS[4]
            elif (y == room.y1 - 1 or y == room.y2):  # vertical
                map[x][y] = WALLS[5]
            else:
                map[x][y] = FLOOR


def pick_wall(room):
    # direction = random.choice(['north', 'east', 'south', 'west'])
    direction = 'east'
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

    return x, y, direction


def scan_for_corridor(wall_x, wall_y, direction):
    corridor_length = random.randint(3, 10)
    if direction == 'north':
        if (wall_y - corridor_length > 0):
            for i in range(wall_y - corridor_length, wall_y + 1):
                map[wall_x][i] = FLOOR
    elif direction == 'east':
        if (wall_x + corridor_length < MAPWIDTH):
            for i in range(wall_x, wall_x + corridor_length):
                map[i][wall_y] = FLOOR
    elif direction == 'south':
        if (wall_y + corridor_length < MAPHEIGHT):
            for i in range(wall_y, wall_y + corridor_length):
                map[wall_x][i] = FLOOR
    elif direction == 'west':
        if (wall_x - corridor_length > 0):
            for i in range(wall_x - corridor_length, wall_x + 1):
                map[i][wall_y] = FLOOR

    return True


def generate_door(room_x, room_y, room_height, room_width):
    wall_x = random.choice([room_x - 1, room_x + room_width - 1])
    wall_y = random.choice([room_y - 1, room_y + room_height - 1])
    if ((wall_x == room_x and wall_y == room_y) or (
                    wall_x == room_x + room_width - 1 and wall_y == room_y + room_height - 1)):
        return generate_door(room_x, room_y, room_height, room_width)
    else:
        return [wall_x, wall_y]


def generate_tilemap():
    global map
    map = [[numpy.random.choice(BACKGROUND, p=BACKGROUND_WEIGHTS) for height in range(MAPHEIGHT)] for width in
           range(MAPWIDTH)]

    starting_room_width = 5
    starting_room_height = 5
    starting_room_x = math.floor(MAPWIDTH / 2) - starting_room_width + math.floor(starting_room_width / 2)
    starting_room_y = math.floor(MAPHEIGHT / 2) - starting_room_height + math.floor(starting_room_height / 2)

    starting_room = Rect(starting_room_x, starting_room_y, starting_room_width, starting_room_height)
    create_room(starting_room)
    wall_x, wall_y, direction = pick_wall(starting_room)
    scan_for_corridor(wall_x, wall_y, direction)

    return map


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

map = generate_tilemap()

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

        if passable:
            PLAYER.move(0, 1)

    # get all the user events
    for event in pygame.event.get():
        if event.type == QUIT:
            quitGame()

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quitGame()

    for row in range(MAPHEIGHT):
        for column in range(MAPWIDTH):
            DISPLAYSURF.blit(map[column][row].sprite, (column * TILESIZE, row * TILESIZE))

    PLAYER.update()

    pygame.display.update()
