import figure


# Logic of the tetris program
class Tetris:
    level = 2
    score = 0
    state = ""
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None

    # initialize the tetris object
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    # new random figure
    def new_figure(self):
        self.figure = figure.Figure(3, 0)

    # collision check
    def collision(self):
        collision = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        collision = True
        return collision

    # check if line complete, add to score
    def full_line(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    # drop the piece instantly
    def move_drop(self):
        while not self.collision():
            self.figure.y += 1
        self.figure.y -= 1
        self.move_freeze()

    # move the piece down
    def move_down(self):
        self.figure.y += 1
        if self.collision():
            self.figure.y -= 1
            self.move_freeze()

    # check if game over
    def move_freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.piece.color
        self.full_line()
        self.new_figure()
        if self.collision():
            self.state = "gameover"

    # move left_right
    def move_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.collision():
            self.figure.x = old_x

    # rotate the piece / currently broken
    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.collision():
            self.figure.rotation = old_rotation

