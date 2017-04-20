from ..rng import RNG
from .geometry import Point, Rectangle, Edge, distance_sq, midpoint

class Map():

    def __init__(self, width=0, height=0, rng=0):

        self.width = width
        self.height = height
        self.map = [[0 for y in range(height)] for x in range(width)]

        self.rng = rng
        if self.rng == 0:
            self.rng = RNG()

        self.directions = [
            Point(-1, 0), 
            Point(1, 0), 
            Point(0, -1), 
            Point(0, 1)
        ]

    # Getters and Setters

    def get_height(self):

        return self.height

    def set_height(self, height):

        self.height = height

    def get_rng(self):

        return self.rng

    def set_rng(self, rng):

        self.rng = rng

    def get_width(self):

        return self.width

    def set_width(self, width):

        self.width = width

    # Generation Methods

    def carve(self, left, top, width, height, value=1):

        for x in range(left, left + width):
            for y in range(top, top + height):
                self.map[x][y] = value

    def create_gabriel_graph(self, rooms):

        edges = []

        for a in range(len(rooms) - 1):
            roomA = rooms[a]
            for b in range(a + 1, len(rooms)):
                roomB = rooms[b]
                mp = midpoint(roomA.center(), roomB.center())
                radius_sq = distance_sq(roomA.center(), mp)
                skip_edge = False

                for c in range(len(rooms)):
                    if c == a or c == b:
                        continue

                    roomC = rooms[c]
                    if distance_sq(mp, roomC.center()) <= radius_sq:
                        skip_edge = True
                        break

                if not skip_edge:
                    edges.append(Edge(roomA, roomB))

        return edges

    def create_hall(self, room1, room2, width):

        half_width = width // 2

        if room1.center().x == room2.center().x:
            h = Rectangle(
                int(room1.center().x) - half_width,
                min(int(room1.center().y), int(room2.center().y)),
                width,
                abs(int(room1.center().y) - int(room2.center().y))
            )

            return [h]

        if room1.center().y == room2.center().y:
            h = Rectangle(
                min(int(room1.center().x), int(room2.center().x)),
                int(room1.center().y) - half_width,
                abs(int(room1.center().x) - int(room2.center().x)),
                width
            )

            return [h]

        left = room1 if room1.center().x < room2.center().x else room2
        right = room2 if room1.center().x < room2.center().x else room1

        top = room1 if room1.center().y < room2.center().y else room2
        bottom = room2 if room1.center().y < room2.center().y else room1

        if self.rng.random() < 0.5:
            # draw horizontal hall from left to right,
            # then vertical hall from top to bottom

            hh = Rectangle(
                int(left.center().x),
                int(left.center().y) - half_width,
                int(right.center().x) - int(left.center().x) + half_width,
                width
            )

            hv = Rectangle(
                int(right.center().x) - half_width,
                int(top.center().y),
                width,
                int(bottom.center().y) - int(top.center().y) + half_width
            )

        else:
            # draw vertical hall first from top to bottom,
            # then horizontal hall from left to right

            hv = Rectangle(
                int(top.center().x) - half_width,
                int(top.center().y),
                width,
                int(bottom.center().y) - int(top.center().y) + half_width
            )

            hh = Rectangle(
                int(left.center().x),
                int(bottom.center().y) - half_width,
                int(right.center().x) - int(left.center().x) + half_width,
                width
            )

        return [hh, hv]
