import os

import pygame


class Position():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Velocity:
    def __init__(self, dx=0, dy=0):
        self.dx = dx
        self.dy = dy


class Sprite(pygame.sprite.Sprite):
    def __init__(self, images):
        super(Sprite, self).__init__()
        self.counter = 0
        self.facing_right = -1
        self.image_array = []
        for i in range(0, len(images)):
            self.image_array.append(self.load_image(images[i]))
        self.index = 0
        self.current_image = self.image_array[self.index]

    def load_image(self, name):
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
