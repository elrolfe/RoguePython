from .map import Map
from .geometry import Point, Rectangle, Edge

class GridGenerator(Map):

    def __init__(self, width=100, height=100, rng=0):

        super().__init__(width, height, rng)

        self.cell_width = 20
        self.cell_height = 20
        self.hall_width = 4
        self.min_room_width = 8
        self.max_room_width = 19
        self.min_room_height = 8
        self.max_room_height = 19
        self.min_rooms = 10
        self.max_rooms = 18

        self.rooms = []
        self.edges = []
        self.halls = []

    def set_cell_width(self, width):
        
        self.cell_width = width

    def set_cell_height(self, height):
        
        self.cell_height = height

    def set_hall_width(self, width):
        
        self.hall_width = width

    def set_min_room_width(self, width):
        
        self.min_room_width = width

    def set_max_room_width(self, width):
        
        self.max_room_width = width

    def set_min_room_height(self, height):
        
        self.min_room_height = height

    def set_max_room_height(self, height):
        
        self.max_room_height = height

    def set_min_rooms(self, rooms):
        
        self.min_rooms = rooms

    def set_max_rooms(self, rooms):
        
        self.max_rooms = rooms

    def carve_map(self):

        for i in range(len(self.rooms)):
            r = self.rooms[i]
            self.carve(r.position.x, r.position.y, r.width, r.height)

        for i in range(len(self.halls)):
            r = self.halls[i]
            self.carve(r.position.x, r.position.y, r.width, r.height)

        for x in range(self.width):
            self.map[x][0] = 0
            self.map[x][self.height - 1] = 0

        for y in range(self.height):
            self.map[0][y] = 0
            self.map[self.width - 1][y] = 0

    def create_halls(self):

        self.halls = []

        for i in range(len(self.edges)):
            self.halls += self.create_hall(
                self.edges[i].node1,
                self.edges[i].node2,
                self.hall_width
            )

    def gabriel_graph(self):
        self.edges = self.create_gabriel_graph(self.rooms)
        print(len(self.edges))

    def generate(self):
        self.place_rooms()
        self.gabriel_graph()
        self.create_halls()
        self.carve_map()

        return self.map

    def place_rooms(self):

        grid_width = self.width // self.cell_width
        grid_height = self.height // self.cell_height
        total_rooms = self.rng.random_range(self.min_rooms, self.max_rooms)

        possible_rooms = [0 for x in range(grid_width * grid_height)]

        for i in range(total_rooms):
            cell = int(self.rng.random() * len(possible_rooms))

            while possible_rooms[cell] != 0:
                cell = int(self.rng.random() * len(possible_rooms))

            room_width = self.rng.random_range(
                self.min_room_width,
                self.max_room_width
            )

            room_height = self.rng.random_range(
                self.min_room_height,
                self.max_room_height
            )

            x = (
                (cell % grid_width)
                * self.cell_width
                + self.rng.random_range(0, self.cell_width - room_width)
            )

            y = (
                (cell // grid_width)
                * self.cell_height
                + self.rng.random_range(0, self.cell_height - room_height)
            )

            possible_rooms[cell] = Rectangle(x, y, room_width, room_height)

        self.rooms = [
            possible_rooms[x]
            for x in range(len(possible_rooms))
            if possible_rooms[x] != 0
        ]