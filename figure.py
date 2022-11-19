import random

# rgb color ranges
colors = [
    (0, 0, 0),  # black
    (120, 37, 179),  # purple
    (100, 179, 179),  # light blue
    (80, 34, 22),  # brown
    (80, 134, 22),  # green
    (180, 34, 22),  # red
    (180, 34, 122),  # pink
]


# sets up the tetrimino pieces
class Figure:
    # creates all the tetromino pieces
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    # Initialize all the data to the object
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    # define the object
    def image(self):
        return self.figures[self.type][self.rotation]

    # rotate the object
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])
