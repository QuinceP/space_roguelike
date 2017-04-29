from generator import *
from tile import *


class MapGenerator:
    def __init__(self, start_x, start_y):
        self.background_weights = [0.85, 0.05, 0.08, 0.02]
        self.map = []
        self.start_x = start_x
        self.start_y = start_y
        self.text_map = dMap()
        self.text_map.makeMap(self.start_x, self.start_y, 100, 45, 101)

    def make_map(self):
        for y in range(self.start_y):
            line = []
            for x in range(self.start_x):
                if self.text_map.mapArr[y][x] == 0:
                    line.append(FLOOR)
                if self.text_map.mapArr[y][x] == 1:
                    line.append(numpy.random.choice(BACKGROUND, p=self.background_weights))
                if self.text_map.mapArr[y][x] == 2:
                    line.append(WALLS[5])
                if self.text_map.mapArr[y][x] == 3 or self.text_map.mapArr[y][x] == 4 or self.text_map.mapArr[y][
                    x] == 5:
                    line.append(DOOR)
                if self.text_map.mapArr[y][x] == 6:
                    line.append(WALLS[0])
                if self.text_map.mapArr[y][x] == 7:
                    line.append(WALLS[1])
                if self.text_map.mapArr[y][x] == 8:
                    line.append(WALLS[2])
                if self.text_map.mapArr[y][x] == 9:
                    line.append(WALLS[3])
                if self.text_map.mapArr[y][x] == 10:
                    line.append(WALLS[4])
                if self.text_map.mapArr[y][x] == 11:
                    line.append(WALLS[5])
            self.map.append(line)
