from collections import deque

from .map import Map
from .geometry import Point

class CellularGenerator(Map):

    def __init__(self, width=100, height=100, rng=0):

        super().__init__(width, height, rng)

        self.live_cell_chance = 0.4
        self.wall_lower_limit = 1
        self.wall_upper_limit = 5
        self.fill_empty_space_iterations = 6
        self.add_wall_iterations = 4
        self.min_floor_percentage = 0.4
        self.max_floor_percentage = 0.6

    def set_live_cell_chance(self, chance):

        self.live_cell_chance = chance

    def set_wall_lower_limit(self, limit):

        self.wall_lower_limit = limit

    def set_wall_upper_limit(self, limit):

        self.wall_upper_limit = limit

    def set_fill_empty_space_iterations(self, iterations):

        self.fill_empty_space_iterations = iterations

    def set_add_wall_iterations(self, iterations):

        self.add_wall_iterations = iterations

    def set_min_floor_percentage(self, percentage):

        self.min_floor_percentage = percentage

    def set_max_floor_percentage(self, percentage):

        self.max_floor_percentage = percentage

    def extended_walls(self, x, y):

        walls = 0

        walls += 0 if x - 2 < 0 else (1 if self.map[x - 2][y] == 0 else 0)
        walls += 0 if x + 2 >= self.width else (
            1 if self.map[x + 2][y] == 0 else 0
        )
        walls += 0 if y - x < 0 else (1 if self.map[x][y - 2] == 0 else 0)
        walls += 0 if y + 2 >= self.height else (
            1 if self.map[x][y + 2] == 0 else 0
        )

        return walls

    def find_main_region(self):

        region = 1
        largest_region = 0
        largest_size = -1

        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                if self.map[x][y] == -1:
                    size = self.set_region(x, y, region)

                    if size > largest_size:
                        largest_size = size
                        largest_region = region

                    region += 1

        floor_percentage = largest_size / (self.width * self.height)
        if (
            floor_percentage < self.min_floor_percentage
            or floor_percentage > self.max_floor_percentage
        ):
            return False

        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                self.map[x][y] = 1 if self.map[x][y] == largest_region else 0

        return True

    def generate(self):
        
        done = False

        while not done:
            self.randomize()
            self.smooth()
            done = self.find_main_region()

        return self.map

    def randomize(self):

        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                self.map[x][y] = (
                    -1 if self.rng.random() < self.live_cell_chance else 0
                )

    def set_region(self, x, y, region):

        size = 1
        floor_cells = deque([Point(x, y)])

        self.map[x][y] = region

        while len(floor_cells) > 0:
            cell = floor_cells.popleft()

            for i in range(len(self.directions)):
                dir = self.directions[i]
                if self.map[cell.x + dir.x][cell.y + dir.y] == -1:
                    floor_cells.append(Point(cell.x + dir.x, cell.y + dir.y))
                    self.map[cell.x + dir.x][cell.y + dir.y] = region
                    size += 1

        return size

    def smooth(self):

        floor_fill = self.fill_empty_space_iterations
        wall_fill = self.add_wall_iterations

        while floor_fill + wall_fill > 0:
            new_map = [
                [0 for y in range(self.height)] 
                for x in range(self.width)
            ]

            for x in range(1, self.width - 1):
                for y in range(1, self.height - 1):
                    new_map[x][y] = -1

                    walls = self.surrounding_walls(x, y)
                    if (floor_fill > 0
                        and walls + self.extended_walls(x, y) 
                        <= self.wall_lower_limit
                    ):
                        new_map[x][y] = 0

                    if walls >= self.wall_upper_limit:
                        new_map[x][y] = 0

            self.map = new_map

            if floor_fill > 0:
                floor_fill -= 1
            else:
                wall_fill -= 1

    def surrounding_walls(self, x, y):

        walls = 0

        for a in range(x - 1, x + 2):
            for b in range(y - 1, y + 2):
                if not(a == x and b == y):
                    if self.map[a][b] == 0:
                        walls += 1

        return walls