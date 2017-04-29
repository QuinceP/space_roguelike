from collections import namedtuple

MESSAGE_BOX_SIZE = 150
WINDOW_WIDTH = 1536
WINDOW_HEIGHT = 768
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT + MESSAGE_BOX_SIZE)

MINIMAP_PANEL_LEFT = 1280
MINIMAP_WIDTH = 255
MINIMAP_HEIGHT = 251
STATS_PANEL_LEFT = 1015

TILESIZE = 64
MAPWIDTH = 60
MAPHEIGHT = 30

FONT_FILENAME = 'assets/fonts/SpaceMono-Regular.ttf'
FONT_SIZE = 17

ASCII_FONT_FILENAME = FONT_FILENAME
ASCII_FONT_SIZE = 24

BLACK = (0, 0, 0)
BROWN = (153, 76, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

Color = namedtuple('Color', 'name shades')

PRIMARY = Color('primary', [(197, 211, 226),
                            (254, 254, 255),
                            (234, 240, 246),
                            (150, 173, 197),
                            (100, 130, 161)]
                )

SECONDARY = Color('secondary', [(204, 202, 230),
                                (254, 254, 255),
                                (236, 236, 247),
                                (163, 159, 205),
                                (116, 112, 172)]
                  )
TERTIARY = Color('tertiary', [(196, 227, 217),
                              (254, 255, 254),
                              (233, 246, 242),
                              (148, 199, 183),
                              (98, 164, 142)]
                 )

COMPLEMENTARY = Color('complementary', [(255, 241, 220),
                                        (255, 255, 254),
                                        (255, 250, 242),
                                        (255, 229, 190),
                                        (247, 207, 147)]
                      )
