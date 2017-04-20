class Edge():

    def __init__(self, node1, node2):

        self.node1 = node1
        self.node2 = node2

class Point():

    def __init__(self, x, y):

        self.x = x
        self.y = y

class Rectangle():

    def __init__(self, x, y, width, height):

        self.position = Point(x, y)
        self.width = width
        self.height = height

    def center(self):

        return Point(
            self.position.x + self.width / 2,
            self.position.y + self.height / 2
        )

def distance_sq(p1, p2):

    dx = p1.x - p2.x
    dy = p1.y - p2.y

    return dx * dx + dy * dy

def midpoint(p1, p2):

    return Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)