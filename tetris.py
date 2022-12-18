import pygame

import figure


class Tetris(object):
    pressing_down = False
    level = 1
    score = 0
    field = []
    height = 0
    width = 0
    time_elapsed = 0
    x = 100
    y = 60
    zoom = 20
    hold_pressed = False
    figure = None
    next_figure = None
    next_figure2 = None
    next_figure3 = None
    hold_figure = None
    """
    A single instance of this class is responsible for
    managing which individual game state is active
    and keeping it updated. It also handles many of
    pygame's nuts and bolts (managing the event
    queue, framerate, updating the display, etc.).
    and its run method serves as the "game loop".
    """

    def __init__(self, width, height, screen, states, start_state):
        """
        Initialize the Game object.

        screen: the pygame display surface
        states: a dict mapping state-names to GameState objects
        start_state: name of the first active game state
        """
        self.done = False
        self.screen = screen
        self.width = width
        self.height = height
        self.field = []
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.score = 0
        self.states = states
        self.state_name = start_state
        self.next_figure = figure.Figure(3, 0)
        self.next_figure2 = figure.Figure(3, 0)
        self.next_figure3 = figure.Figure(3, 0)
        self.state = self.states[self.state_name]
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def event_loop(self):
        """Events are passed for handling to the current state."""
        for event in pygame.event.get():
            self.state.get_event(event)

    def flip_state(self):
        """Switch to the next game state."""
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)

    def run(self):
        """
        Pretty much the entirety of the game's runtime will be
        spent inside this while loop.
        """
        while not self.done:
            if self.figure is None:
                self.new_figure()
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.draw()
            self.update(dt)
            pygame.display.update()

    def update(self, dt):
        """
        Check for state flip and update active state.

        dt: milliseconds since last frame
        """
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self):
        """Pass display surface to active state for drawing."""
        self.state.draw(self.screen)

    # new random figure
    def new_figure(self):
        self.figure = self.next_figure
        self.next_figure = self.next_figure2
        self.next_figure2 = self.next_figure3
        self.next_figure3 = figure.Figure(3, 0)
        self.hold_pressed = False

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
        self.check_level()

    # check what level we are currently on, used to determine speed, totally arbitrary code values
    def check_level(self):
        if self.score < 25:
            self.level = 1
        elif self.score < 65:
            self.level = 2
        elif self.score < 115:
            self.level = 3
        elif self.score < 175:
            self.level = 4
        elif self.score < 245:
            self.level = 5
        elif self.score < 325:
            self.level = 6
        elif self.score < 405:
            self.level = 7
        elif self.score < 485:
            self.level = 8
        elif self.score < 525:
            self.level = 9
        elif self.score < 605:
            self.level = 10
        elif self.score < 685:
            self.level = 11
        elif self.score < 765:
            self.level = 12
        elif self.score < 855:
            self.level = 13
        elif self.score < 895:
            self.level = 14
        elif self.score < 995:
            self.level = 15


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
            self.state.next_state = "GAMEOVER"
            # not sure why, but just setting done = True doesn't work, so i just flip here
            self.flip_state()

    # move left_right
    def move_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.collision():
            self.figure.x = old_x

    # rotate the piece
    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.collision():
            self.figure.rotation = old_rotation

    def revrotate(self):
        old_rotation = self.figure.rotation
        self.figure.revrotate()
        if self.collision():
            self.figure.rotation = old_rotation

    def hold(self):
        if not self.hold_pressed:
            if self.hold_figure is None:
                self.hold_figure = self.figure
                self.new_figure()
            else:
                temp = self.figure
                self.figure = self.hold_figure
                self.hold_figure = temp

            self.hold_pressed = True
            self.figure.x = 3
            self.figure.y = 0
