import random

import esper

from components import *


class AISystem(esper.Processor):
    def __init__(self, map, mapwidth, mapheight):
        self.map = map
        self.mapwidth = mapwidth
        self.mapheight = mapheight

    def process(self):
        for ent, (position, velocity, ai, sprite) in self.world.get_components(Position, Velocity, AI, Sprite):
            if ai.is_turn:
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
                ai.is_turn = False
            pass


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
            sprite.image = pygame.transform.scale(sprite.image, (64, 64))
            sprite.current_image = pygame.transform.scale(sprite.image, (64, 64))


from collections import deque


class TurnTakerSystem(esper.Processor):
    def __init__(self):
        self.time_travelers = deque()
        self.turn_taken = False
        self.turns = 0

    def register(self, obj):
        self.time_travelers.append(obj)
        obj.action_points = 0

    def release(self, obj):
        self.time_travelers.remove(obj)

    def tick(self):
        if len(self.time_travelers) > 0:
            obj = self.time_travelers[0]
            self.time_travelers.rotate()
            obj.action_points += obj.agility
            while obj.action_points > 0:
                obj.action_points -= obj.take_turn()
        self.turns += 1

    def process(self):
        if self.turn_taken:
            self.tick()
            self.turn_taken = False
