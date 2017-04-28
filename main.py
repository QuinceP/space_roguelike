from tkinter import *

import numpy
from pygame.locals import *

from generator import dMap
from messages import Message as messages_Message
from messages import MessageHandler
from systems import *
from theme import *


# TODO: Abstraction and cleanup

class Tile():
    def __init__(self, name, sprite, z_level, is_passable):
        self.name = name
        self.sprite = pygame.image.load(sprite)
        self.sprite = pygame.transform.scale(self.sprite, (64, 64))
        self.z_level = z_level
        self.is_passable = is_passable

    def __repr__(self):
        return "<Tile name:%s sprite:%s z_level:%s is_passable:%s>" % (
            self.name, self.sprite, self.z_level, self.is_passable)


world = esper.World

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


TILESIZE = 64
MAPWIDTH = 60
MAPHEIGHT = 30

pygame.init()
DISPLAYSURF = pygame.display.set_mode((1536, 768 + 150))

message_handler = MessageHandler()

clock = pygame.time.Clock()
startx = MAPWIDTH
starty = MAPHEIGHT

themap = dMap()
themap.makeMap(startx, starty, 100, 45, 101)

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
            line.append(WALLS[1])
        if themap.mapArr[y][x] == 8:
            line.append(WALLS[2])
        if themap.mapArr[y][x] == 9:
            line.append(WALLS[3])
        if themap.mapArr[y][x] == 10:
            line.append(WALLS[4])
        if themap.mapArr[y][x] == 11:
            line.append(WALLS[5])
    map.append(line)

world = esper.World()

ai_system = AISystem(map, MAPWIDTH, MAPHEIGHT)
camera_system = CameraSystem(map, TILESIZE, DISPLAYSURF)
movement_system = MovementSystem()
sprite_system = SpriteSystem(DISPLAYSURF, TILESIZE)

world.add_processor(ai_system, priority=2)
world.add_processor(camera_system, priority=1)
world.add_processor(movement_system, priority=0)
world.add_processor(sprite_system, priority=0)

room_found = False
while not room_found:
    room_index = random.randint(1, len(themap.roomList) - 1)
    starting_room = themap.roomList[room_index]
    try:
        x_pos = random.randint(starting_room[2] + 1, starting_room[2] + starting_room[1] - 1)
        y_pos = random.randint(starting_room[3] + 1, starting_room[3] + starting_room[0] - 1)
    except ValueError:
        continue

    PLAYER = world.create_entity(Sprite(['oryx_16bit_scifi_creatures_01.png', 'oryx_16bit_scifi_creatures_02.png']),
                                 Position(x_pos, y_pos),
                                 Velocity(),
                                 Fighter(health=100, max_health=100))
    camera = world.create_entity(Position(x_pos - 1, y_pos - 1),
                                 Velocity(),
                                 Camera(24, 12, PLAYER))

    if map[y_pos][x_pos] == FLOOR:
        room_found = True

room_found = False
while not room_found:
    room_index = random.randint(1, len(themap.roomList) - 1)
    starting_room = themap.roomList[room_index]
    try:
        x_pos = random.randint(starting_room[2] + 1, starting_room[2] + starting_room[1] - 1)
        y_pos = random.randint(starting_room[3] + 1, starting_room[3] + starting_room[0] - 1)
    except ValueError:
        continue

    MONSTER = world.create_entity(Sprite(['oryx_16bit_scifi_creatures_553.png', 'oryx_16bit_scifi_creatures_554.png']),
                                  Position(x_pos, y_pos),
                                  Velocity(),
                                  Fighter(health=100, max_health=100))
    if map[y_pos][x_pos] == FLOOR:
        room_found = True

message_handler.messages.append(messages_Message('Welcome to <Game Name>.', 'warning'))

while True:
    clock.tick(10)

    player_x = world.component_for_entity(PLAYER, Position).x
    player_y = world.component_for_entity(PLAYER, Position).y
    player_velocity = world.component_for_entity(PLAYER, Velocity)
    player_sprite = world.component_for_entity(PLAYER, Sprite)
    player_fighter = world.component_for_entity(PLAYER, Fighter)

    world.component_for_entity(camera, Position).x = player_x
    world.component_for_entity(camera, Position).y = player_y

    camera_x = world.component_for_entity(camera, Position).x
    camera_y = world.component_for_entity(camera, Position).y
    camera_velocity = world.component_for_entity(camera, Velocity)

    for event in pygame.event.get():
        if event.type == QUIT:
            quitGame()

        elif event.type == KEYDOWN:
            string = ('You pressed ' + pygame.key.name(event.key))
            message_handler.messages.append(messages_Message(string, 'default'))
            if event.key == K_ESCAPE:
                quitGame()
            elif event.key == pygame.K_RIGHT and player_x < MAPWIDTH - 1:
                player_sprite.facing_right = True
                try:
                    passable = map[player_y][player_x + 1].is_passable
                except IndexError:
                    passable = False
                if passable:
                    player_velocity.dx = 1
            elif event.key == pygame.K_LEFT and player_x > 0:
                player_sprite.facing_right = False
                try:
                    passable = map[player_y][player_x - 1].is_passable
                except IndexError:
                    passable = False
                if passable:
                    player_velocity.dx = -1
            elif event.key == pygame.K_UP and player_y > 0:
                try:
                    passable = map[player_y - 1][player_x].is_passable
                except IndexError:
                    passable = False
                if passable:
                    player_velocity.dy = -1
            elif event.key == pygame.K_DOWN and player_y < MAPHEIGHT - 1:
                try:
                    passable = map[player_y + 1][player_x].is_passable
                except IndexError:
                    passable = False
                if passable:
                    player_velocity.dy = 1

    DISPLAYSURF.fill(BLACK)

    x_1 = player_x - 11
    x_2 = player_x + 13
    y_1 = player_y - 5
    y_2 = player_y + 7

    if x_1 < 0:
        x_1 = 0
        x_2 = 24
    if x_2 > MAPWIDTH:
        x_1 = MAPWIDTH - 24
        x_2 = MAPWIDTH
    if y_1 < 0:
        y_1 = 0
        y_2 = 12
    if y_2 > MAPHEIGHT:
        y_1 = MAPHEIGHT - 12
        y_2 = MAPHEIGHT

    row = 0
    column = 0
    for i in range(x_1, x_2):
        for j in range(y_1, y_2):
            DISPLAYSURF.blit(map[j][i].sprite, (TILESIZE * row, TILESIZE * column))
            if i == player_x and j == player_y:
                DISPLAYSURF.blit(player_sprite.current_image, (TILESIZE * row, TILESIZE * column))
            column += 1
        column = 0
        row += 1

    world.process()

    message_handler.display_messages(DISPLAYSURF)

    name = message_handler.font.render('Player Name the Class', 1, SECONDARY.shades[4])
    DISPLAYSURF.blit(name, (1025, 768))

    health = message_handler.font.render('Health:', 1, COMPLEMENTARY.shades[4])
    DISPLAYSURF.blit(health, (1025, 795))
    health = message_handler.font.render(str(player_fighter.health) + '/' + str(player_fighter.health), 1,
                                         COMPLEMENTARY.shades[4])
    DISPLAYSURF.blit(health, (1100, 795))

    pygame.draw.rect(DISPLAYSURF, TERTIARY.shades[4], (0, 768, 1536, 150), 1)
    pygame.draw.line(DISPLAYSURF, TERTIARY.shades[4], (1015, 768), (1015, 768 + 150))
    pygame.display.update()
