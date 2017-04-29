import numpy
import pygame
from theme import *

MESSAGE_TYPES = {'default': PRIMARY.shades[0],
                 'warning': COMPLEMENTARY.shades[4]}
MAX_LINE_LENGTH = 100
MAX_DISPLAY_LINES = 6
MESSAGES_XPOS = 10
MESSAGES_YPOS = WINDOW_WIDTH
MESSAGES_VERTICAL_SPACING = 25


class Message:
    def __init__(self, text, message_type):
        self.text = text
        self.message_type = type
        self.font_color = MESSAGE_TYPES[message_type]
        self.line_count = int(numpy.floor(len(self.text) / MAX_LINE_LENGTH) + 1)
        self.length = len(text)
        self.lines = [self.text[i:i + MAX_LINE_LENGTH] for i in range(0, self.length, MAX_LINE_LENGTH)]


class MessageHandler:
    def __init__(self):
        self.messages = []
        self.font = pygame.font.Font(FONT_FILENAME, FONT_SIZE)
        self.ascii_font = pygame.font.Font(ASCII_FONT_FILENAME, ASCII_FONT_SIZE)

    def display_messages(self, surface):
        if len(self.messages) > 0:
            line_count = 0
            lines = []
            colors = []
            for i in reversed(range(len(self.messages))):
                if line_count >= MAX_DISPLAY_LINES:
                    break
                color = self.messages[i].font_color
                for j in range(0, self.messages[i].line_count):
                    lines.append(self.messages[i].lines[-j])
                    colors.append(color)
                    line_count += 1
                    if line_count >= MAX_DISPLAY_LINES:
                        break

            for k in range(MAX_DISPLAY_LINES):
                if k < len(lines):
                    label = self.font.render(lines[k], 1, colors[k])
                    surface.blit(label, (MESSAGES_XPOS, MESSAGES_YPOS + (k * MESSAGES_VERTICAL_SPACING)))


pygame.font.init()
message_handler = MessageHandler()
