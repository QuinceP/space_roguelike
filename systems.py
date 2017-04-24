import esper
import pygame

from components import *


class MovementSystem(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        for ent, (position, velocity) in self.world.get_components(Position, Velocity):
            position.x += velocity.dx
            position.y += velocity.dy
            velocity.dx = 0
            velocity.dy = 0


class SpriteSystem(esper.Processor):
    def __init__(self, parent_surface, tile_size):
        self.parent_surface = parent_surface
        self.tile_size = tile_size

    @staticmethod
    def flip(sprite):
        sprite.image = pygame.transform.flip(sprite.image, sprite.facing_right, False)

    def process(self):
        for ent, (sprite, position) in self.world.get_components(Sprite, Position):
            sprite.counter += 1

            if sprite.counter == 5:
                sprite.index += 1
                sprite.counter = 0

            if sprite.index >= len(sprite.image_array):
                sprite.index = 0

            sprite.image = sprite.image_array[sprite.index]
            self.flip(sprite)
            self.parent_surface.blit(sprite.image, (position.x * self.tile_size, position.y * self.tile_size))
