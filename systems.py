import esper
import random
from components import *

class AISystem(esper.Processor):
    def __init__(self, map, mapwidth, mapheight):
        self.map = map
        self.mapwidth = mapwidth
        self.mapheight = mapheight

    def process(self):
        for ent, (position, velocity, ai, sprite) in self.world.get_components(Position, Velocity, AI, Sprite):
            should_move = random.randint(0, 10)
            # if should_move == 1:
            direction = random.choice(['north', 'east', 'south', 'west'])
            if direction == 'east' and position.x < self.mapwidth - 1:
                sprite.facing_right = True
                try:
                    passable = self.map[position.y][position.x + 1].is_passable
                except IndexError:
                    passable = False

                if passable:
                    velocity.dx = 1
            elif direction == 'west' and position.x > 0:
                sprite.facing_right = False
                try:
                    passable = self.map[position.y][position.x - 1].is_passable
                except IndexError:
                    passable = False

                if passable:
                    velocity.dx = -1
            elif direction == 'north' and position.y > 0:
                try:
                    passable = self.map[position.y - 1][position.x].is_passable
                except IndexError:
                    passable = False
                if passable:
                    velocity.dy = -1
            elif direction == 'south' and position.y < self.mapheight - 1:
                try:
                    passable = self.map[position.y + 1][position.x].is_passable
                except IndexError:
                    passable = False

                if passable:
                    velocity.dy = 1


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
