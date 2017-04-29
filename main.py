from tkinter import *

from pygame.locals import *

from map import *
from messages import Message as messages_Message
from systems import *
from tile import *


def blit_map(display_width, display_height, map_type):
    x_1 = player_x - int(display_width / 2)
    x_2 = player_x + int(display_width / 2)
    y_1 = player_y - int(display_height / 2)
    y_2 = player_y + int(display_height / 2)

    if x_1 < 0:
        x_1 = 0
        x_2 = display_width
    if x_2 > MAPWIDTH:
        x_1 = MAPWIDTH - display_width
        x_2 = MAPWIDTH
    if y_1 < 0:
        y_1 = 0
        y_2 = display_height
    if y_2 > MAPHEIGHT:
        y_1 = MAPHEIGHT - display_height
        y_2 = MAPHEIGHT

    row = 0
    column = 0
    for i in range(x_1, x_2):
        for j in range(y_1, y_2):
            if map_type == 'main':
                blit_main_map(row, column, i, j)
            else:
                blit_minimap(row, column, i, j)
            column += 1
        column = 0
        row += 1


def blit_minimap(row, column, i, j):
    object_blit = True
    if i == monster_x and j == monster_y:
        DISPLAYSURF.blit(message_handler.ascii_font.render('c', 1, COMPLEMENTARY.shades[4]),
                         ((25 * row) + 1280, (25 * column) - 6))
        object_blit = False
    if i == player_x and j == player_y:
        DISPLAYSURF.blit(message_handler.ascii_font.render('@', 1, SECONDARY.shades[2]),
                         ((25 * row) + 1280, (25 * column) - 6))
        object_blit = False
    if object_blit:
        DISPLAYSURF.blit(map[j][i].alt_sprite, ((25 * row) + 1287, (25 * column) - 6))


def blit_main_map(row, column, i, j):
    DISPLAYSURF.blit(map[j][i].sprite, (TILESIZE * row, TILESIZE * column))
    if i == monster_x and j == monster_y:
        DISPLAYSURF.blit(monster_sprite.current_image, (TILESIZE * row, TILESIZE * column))
    if i == player_x and j == player_y:
        DISPLAYSURF.blit(player_sprite.current_image, (TILESIZE * row, TILESIZE * column))


def handle_input():
    for event in pygame.event.get():
        if event.type == QUIT:
            quitGame()

        elif event.type == KEYDOWN:
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


def place_in_random_room(object):
    room_found = False
    while not room_found:
        room_index = random.randint(1, len(map_generator.text_map.roomList) - 1)
        starting_room = map_generator.text_map.roomList[room_index]
        try:
            x_pos = random.randint(starting_room[2] + 1, starting_room[2] + starting_room[1] - 1)
            y_pos = random.randint(starting_room[3] + 1, starting_room[3] + starting_room[0] - 1)
        except ValueError:
            continue

        if map[y_pos][x_pos] == FLOOR:
            room_found = True
            world.component_for_entity(object, Position).x = x_pos
            world.component_for_entity(object, Position).y = y_pos
            return x_pos, y_pos


def quitGame():
    pygame.quit()
    sys.exit()


pygame.init()
world = esper.World
map_generator = MapGenerator(MAPWIDTH, MAPHEIGHT)
map_generator.make_map()
map = map_generator.map
DISPLAYSURF = pygame.display.set_mode(WINDOW_SIZE)

clock = pygame.time.Clock()

world = esper.World()

ai_system = AISystem(map, MAPWIDTH, MAPHEIGHT)
movement_system = MovementSystem()
sprite_system = SpriteSystem(DISPLAYSURF, TILESIZE)

world.add_processor(ai_system, priority=2)
world.add_processor(movement_system, priority=0)
world.add_processor(sprite_system, priority=0)

PLAYER = world.create_entity(Sprite(['assets/denizens/oryx_16bit_scifi_creatures_33.png', 'assets/denizens/oryx_16bit_scifi_creatures_34.png']),
                             Position(),
                             Velocity(),
                             Fighter(health=100, max_health=100))

MONSTER = world.create_entity(Sprite(['assets/denizens/oryx_16bit_scifi_creatures_553.png', 'assets/denizens/oryx_16bit_scifi_creatures_554.png']),
                              Position(0, 0),
                              Velocity(),
                              Fighter(health=100, max_health=100))

x_pos, y_pos = place_in_random_room(PLAYER)
place_in_random_room(MONSTER)
camera = world.create_entity(Position(x_pos - 1, y_pos - 1),
                             Velocity(),
                             Camera(target=PLAYER))

message_handler.messages.append(messages_Message('Welcome to <Game Name>.', 'warning'))

while True:
    clock.tick(10)

    player_x = world.component_for_entity(PLAYER, Position).x
    player_y = world.component_for_entity(PLAYER, Position).y
    player_velocity = world.component_for_entity(PLAYER, Velocity)
    player_sprite = world.component_for_entity(PLAYER, Sprite)
    player_fighter = world.component_for_entity(PLAYER, Fighter)

    monster_x = world.component_for_entity(MONSTER, Position).x
    monster_y = world.component_for_entity(MONSTER, Position).y
    monster_sprite = world.component_for_entity(MONSTER, Sprite)

    world.component_for_entity(camera, Position).x = player_x
    world.component_for_entity(camera, Position).y = player_y

    camera_x = world.component_for_entity(camera, Position).x
    camera_y = world.component_for_entity(camera, Position).y
    camera_velocity = world.component_for_entity(camera, Velocity)

    handle_input()

    DISPLAYSURF.fill(BLACK)

    blit_map(20, 12, 'main')
    blit_map(10, 10, 'minimap')

    world.process()

    message_handler.display_messages(DISPLAYSURF)

    name = message_handler.font.render('Player Name the Class', 1, SECONDARY.shades[4])
    DISPLAYSURF.blit(name, (1025, WINDOW_HEIGHT))

    health = message_handler.font.render('Health:', 1, COMPLEMENTARY.shades[4])
    DISPLAYSURF.blit(health, (1025, 795))
    health = message_handler.font.render(str(player_fighter.health) + '/' + str(player_fighter.health), 1,
                                         COMPLEMENTARY.shades[4])
    DISPLAYSURF.blit(health, (1100, 795))

    pygame.draw.rect(DISPLAYSURF, TERTIARY.shades[4], (0, WINDOW_HEIGHT, WINDOW_WIDTH, MESSAGE_BOX_SIZE), 1)
    pygame.draw.rect(DISPLAYSURF, TERTIARY.shades[4], (MINIMAP_PANEL_LEFT, 0, MINIMAP_WIDTH, WINDOW_HEIGHT + 1), 1)
    pygame.draw.rect(DISPLAYSURF, TERTIARY.shades[4], (MINIMAP_PANEL_LEFT, 0, MINIMAP_WIDTH, MINIMAP_HEIGHT), 1)
    pygame.draw.line(DISPLAYSURF, TERTIARY.shades[4], (STATS_PANEL_LEFT, WINDOW_HEIGHT),
                     (STATS_PANEL_LEFT, WINDOW_HEIGHT + MESSAGE_BOX_SIZE))
    pygame.display.update()
