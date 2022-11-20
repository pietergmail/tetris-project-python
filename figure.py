import random

# rgb color ranges
colors = [
    (255, 111, 0),  # orange
    (9, 0, 255),  # dark blue
    (0, 255, 247),  # light blue
    (255, 255, 0),  # yellow
    (80, 134, 22),  # green
    (180, 34, 22),  # red
    (171, 0, 255), # purple
]


# official names from https://tetris.fandom.com/wiki/Tetromino
I_piece = [[1, 5, 9, 13], [4, 5, 6, 7]]
T_piece = [[1, 4, 5, 6], [1, 4, 5, 9], [1, 5, 9, 6], [4, 5, 6, 9]]
L_piece = [[2, 6, 10, 11], [5, 6, 7, 3], [1, 2, 6, 10], [5, 9, 6, 7]]
J_piece = [[1, 5, 9, 8], [4, 5, 6, 10], [1, 2, 5, 9], [0, 4, 5, 6]]
O_piece = [[1, 2, 5, 6]]
S_piece = [[4, 5, 1, 2], [0, 4, 5, 9]]
Z_piece = [[0, 1, 5, 6], [1, 5, 4, 8]]


class Piece:
    def __init__(self, color, shape):
        self.color = color
        self.shape = shape


# sets up the tetrimino pieces
class Figure:
    # creates all the tetromino pieces
    figures = [
        Piece(2, I_piece),
        Piece(6, T_piece),
        Piece(0, L_piece),
        Piece(1, J_piece),
        Piece(3, O_piece),
        Piece(5, S_piece),
        Piece(4, Z_piece),
    ]

    # Initialize all the data to the object
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.piece = self.figures[random.randint(0, len(self.figures) - 1)]
        self.rotation = 0

    # define the object
    def image(self):
        return self.piece.shape[self.rotation]

    # rotate the object // needs to be rewritten
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.piece.shape)
