from collections import deque

from .geometry import Rectangle
from .map import Map

class BSPNode(Rectangle):

    def __init__(self, x, y, width, height):

        super().__init__(x, y, width, height)

        self.left = 0
        self.right = 0
        self.room = 0

class BSPMapGenerator(Map):

    def __init__(self, width=100, height=100, rng=0):

        super().__init__(width, height, rng)

        self.hall_width = 2
        self.max_space_size = 45
        self.min_space_size = 20
        self.min_room_size = 10

        self.tree = 0
        self.spaces = 0
        self.halls = []

    def set_hall_width(self, width):

        self.hall_width = width + (width % 2)

    def set_max_space_size(self, size):

        self.max_space_size = size

    def set_min_space_size(self, size):

        self.min_space_size = size

    def set_min_room_size(self, size):

        self.min_room_size = size

    def carve_map(self):

        for i in range(len(self.spaces)):
            left = self.spaces[i].room.position.x
            top = self.spaces[i].room.position.y
            width = self.spaces[i].room.width
            height = self.spaces[i].room.height

            self.carve(left, top, width, height)

        for i in range(len(self.halls)): 
            left = self.halls[i].position.x
            top = self.halls[i].position.y
            width = self.halls[i].width
            height = self.halls[i].height

            self.carve(left, top, width, height)

    def connect_rooms(self):
        nodes = self.tree_branches(self.tree)

        for i in range(len(nodes)):
            room1 = self.find_room(nodes[i].left)
            room2 = self.find_room(nodes[i].right)

            self.halls += self.create_hall(room1, room2, self.hall_width)

    def create_rooms(self):

        for i in range(len(self.spaces)):
            space = self.spaces[i]
            w = self.rng.random_range(self.min_room_size, space.width - 2)
            h = self.rng.random_range(self.min_room_size, space.height - 2)
            x = self.rng.random_range(1, space.width - w - 1)
            y = self.rng.random_range(1, space.height - h - 1)

            space.room = Rectangle(
                space.position.x + x, 
                space.position.y + y,
                w, 
                h
            )

    def find_room(self, node):

        if node.room != 0:
            return node.room

        if self.rng.random() < 0.5:
            return self.find_room(node.left)

        return self.find_room(node.right)

    def generate(self):

        self.partition_space()
        self.create_rooms()
        self.connect_rooms()
        self.carve_map()

        return self.map

    def partition_space(self):

        self.tree = BSPNode(0, 0, self.width, self.height)

        toSplit = deque([self.tree])

        while len(toSplit) > 0:
            node = toSplit.popleft()

            if (node.width > self.max_space_size
                or node.height > self.max_space_size
                or self.rng.random() < 0.75
            ):
                if self.split(node):
                    toSplit.append(node.left)
                    toSplit.append(node.right)

        self.spaces = self.tree_leafs(self.tree)

    def split(self, node):

        if node.left != 0 or node.right != 0:
            return False

        split_h = self.rng.random() < 0.5
        if node.width > node.height and node.width / node.height >= 1.25:
            split_h = False
        elif node.height > node.width and node.height / node.width >= 1.25:
            split_h = True

        max_split = (
            (node.height if split_h else node.width)
            - self.min_space_size
        )

        if max_split < self.min_space_size:
            return False

        split_position = self.rng.random_range(self.min_space_size, max_split)
        if split_h:
            node.left = BSPNode(
                node.position.x,
                node.position.y,
                node.width,
                split_position
            )

            node.right = BSPNode(
                node.position.x,
                node.position.y + split_position,
                node.width,
                node.height - split_position
            )
        else:
            node.left = BSPNode(
                node.position.x,
                node.position.y,
                split_position,
                node.height
            )

            node.right = BSPNode(
                node.position.x + split_position,
                node.position.y,
                node.width - split_position,
                node.height
            )

        return True

    def tree_branches(self, node):

        if node.left == 0 and node.right == 0:
            return []

        return (
            [node]
            + self.tree_branches(node.left)
            + self.tree_branches(node.right)
        )

    def tree_leafs(self, node):

        if node.left == 0 and node.right == 0:
            return [node]

        return self.tree_leafs(node.left) + self.tree_leafs(node.right)