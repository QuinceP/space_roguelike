from messages import *
from theme import *


class Tile:
    def __init__(self, name, sprite, alt_sprite, z_level, is_passable):
        self.name = name
        self.sprite = pygame.image.load(sprite)
        self.alt_sprite = alt_sprite
        self.sprite = pygame.transform.scale(self.sprite, (TILESIZE, TILESIZE))
        self.z_level = z_level
        self.is_passable = is_passable

    def __repr__(self):
        return "<Tile name:%s sprite:%s z_level:%s is_passable:%s>" % (
            self.name, self.sprite, self.z_level, self.is_passable)


FLOOR = Tile('floor', 'assets/tiles/oryx_16bit_scifi_world_01.png', message_handler.ascii_font.render('.', 1, SECONDARY.shades[0]),
             1, True)
DOOR = Tile('door', 'assets/tiles/oryx_16bit_scifi_world_481.png', message_handler.ascii_font.render('+', 1, SECONDARY.shades[4]), 1,
            True)
OPEN_DOOR = Tile('open_door', 'assets/tiles/oryx_16bit_scifi_world_1106.png', message_handler.ascii_font.render('@', 1, (255, 0, 0)),
                 1, True)
WALLS = [
    Tile('wall_top_left', 'assets/tiles/oryx_16bit_scifi_world_14.png',
         message_handler.ascii_font.render('#', 1, SECONDARY.shades[3]), 1, False),
    Tile('wall_top_right', 'assets/tiles/oryx_16bit_scifi_world_15.png',
         message_handler.ascii_font.render('#', 1, SECONDARY.shades[3]), 1, False),
    Tile('wall_bottom_left', 'assets/tiles/oryx_16bit_scifi_world_16.png',
         message_handler.ascii_font.render('#', 1, SECONDARY.shades[3]), 1, False),
    Tile('wall_bottom_right', 'assets/tiles/oryx_16bit_scifi_world_17.png',
         message_handler.ascii_font.render('#', 1, SECONDARY.shades[3]), 1, False),
    Tile('wall_vertical', 'assets/tiles/oryx_16bit_scifi_world_12.png',
         message_handler.ascii_font.render('#', 1, SECONDARY.shades[3]), 1, False),
    Tile('wall_horizontal', 'assets/tiles/oryx_16bit_scifi_world_09.png',
         message_handler.ascii_font.render('#', 1, SECONDARY.shades[3]), 1, False)
]
BACKGROUND = [
    Tile('empty_space', 'assets/tiles/oryx_16bit_scifi_world_965.png', message_handler.ascii_font.render(' ', 1, (255, 0, 0)), 0,
         False),
    Tile('double_stars', 'assets/tiles/oryx_16bit_scifi_world_966.png', message_handler.ascii_font.render(' ', 1, (255, 0, 0)), 0,
         False),
    Tile('single_star', 'assets/tiles/oryx_16bit_scifi_world_967.png', message_handler.ascii_font.render(' ', 1, (255, 0, 0)), 0,
         False),
    Tile('big_star', 'assets/tiles/oryx_16bit_scifi_world_968.png', message_handler.ascii_font.render(' ', 1, (255, 0, 0)), 0, False)
]
