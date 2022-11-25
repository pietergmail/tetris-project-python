import sys
import pygame as pg
import pygame.display

import figure

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

clock = pygame.time.Clock()
fps = 25
counter = 0


class Game(object):
    pressing_down = False
    level = 2
    score = 0
    field = []
    height = 0
    width = 0
    x = 100
    y = 60
    zoom = 20
    figure = None
    """
    A single instance of this class is responsible for
    managing which individual game state is active
    and keeping it updated. It also handles many of
    pygame's nuts and bolts (managing the event
    queue, framerate, updating the display, etc.).
    and its run method serves as the "game loop".
    """

    def __init__(self, width, height, screen, statess, start_state):
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
        self.clock = pg.time.Clock()
        self.fps = 25
        self.score = 0
        self.states = statess
        self.state_name = start_state
        self.state = self.states[self.state_name]
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def event_loop(self):
        """Events are passed for handling to the current state."""
        for event in pg.event.get():
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
            if game.figure is None:
                game.new_figure()
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()

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
            for j in range(self.height):
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

    # rotate the piece
    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.collision():
            self.figure.rotation = old_rotation


class GameState(object):
    """
    Parent class for individual game states to inherit from.
    """

    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pg.display.get_surface().get_rect()
        self.persist = {}
        self.font = pg.font.Font(None, 24)

    def startup(self, persistent):
        """
        Called when a state resumes being active.
        Allows information to be passed between states.

        persistent: a dict passed from state to state
        """
        self.persist = persistent

    def get_event(self, event):
        """
        Handle a single event passed by the Game object.
        """
        pass

    def update(self, dt):
        """
        Update the state. Called by the Game object once
        per frame.

        dt: time since last frame
        """
        pass

    def draw(self, surface):
        """
        Draw everything to the screen.
        """
        pass


class TitleScreen(GameState):
    def __init__(self):
        super(TitleScreen, self).__init__()
        self.title = self.font.render("Python Tetris", True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = "black"
        self.next_state = "GAMEPLAY"

    # continue on any button press
    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYUP:
            self.persist["screen_color"] = "gold"
            self.done = True
        elif event.type == pg.MOUSEBUTTONUP:
            self.persist["screen_color"] = "dodgerblue"
            self.done = True

    # renders the screen
    def draw(self, surface):
        surface.fill(pg.Color("black"))
        surface.blit(self.title, self.title_rect)


class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.rect = pg.Rect((0, 0), (128, 128))
        self.x_velocity = 1

    def startup(self, persistent):
        self.persist = persistent
        color = self.persist["screen_color"]
        self.screen_color = pg.Color(color)
        if color == "dodgerblue":
            text = "You clicked the mouse to get here"
        elif color == "gold":
            text = "You pressed a key to get here"
        self.title = self.font.render(text, True, pg.Color("gray10"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)

    def get_event(self, event):
        if event.type == pg.QUIT:
            done = True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                game.move_drop()
            if event.key == pg.K_DOWN:
                pressing_down = True
            if event.key == pg.K_LEFT:
                game.move_side(-1)
            if event.key == pg.K_RIGHT:
                game.move_side(1)
            if event.key == pg.K_SPACE:
                game.rotate()

        # check if key is held down, used to change dropping speed
        if event.type == pg.KEYUP:
            if event.key == pg.K_DOWN:
                pressing_down = False

    def update(self, dt):
        game.move_down()

        self.rect.move_ip(self.x_velocity, 0)
        if (self.rect.right > self.screen_rect.right
                or self.rect.left < self.screen_rect.left):
            self.x_velocity *= -1
            self.rect.clamp_ip(self.screen_rect)

    def draw(self, surface):
        # set background color
        screen.fill(WHITE)

        # draw the game screen and the objects
        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom],
                                 1)
                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, figure.colors[game.field[i][j]],
                                     [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2,
                                      game.zoom - 1])

        # create the game screen
        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.figure.image():
                        pg.draw.rect(screen, figure.colors[game.figure.piece.color],
                                         [game.x + game.zoom * (j + game.figure.x) + 1,
                                          game.y + game.zoom * (i + game.figure.y) + 1,
                                          game.zoom - 2, game.zoom - 2])

        # set screen variables
        font = pg.font.SysFont('Calibri', 25, True, False)
        font1 = pg.font.SysFont('Calibri', 45, True, False)
        font2 = pg.font.SysFont('Calibri', 65, True, False)
        text = font.render("Score: " + str(game.score), True, BLACK)
        text_game_over = font2.render("Game Over", True, (255, 125, 0))
        text_game_over1 = font2.render("Press ESC", True, (255, 215, 0))
        text_game_paused = font1.render("Game Paused", True, (255, 125, 0))
        text_game_paused1 = font1.render("Press p to start", True, (255, 215, 0))

        # refresh the screen and check game over
        screen.blit(text, [0, 0])
        if game.state == "gameover":
            paused = False  # pause the game
            screen.blit(text_game_over, [20, 200])
            screen.blit(text_game_over1, [25, 265])

        # draw pause screen
        if game.state == "paused":
            screen.blit(text_game_paused, [45, 200])
            screen.blit(text_game_paused1, [38, 265])

        # refresh screen and set clock speed
        pg.display.flip()


if __name__ == "__main__":
    pg.init()
    size = (400, 500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tetris")
    states = {"TITLESCREEN": TitleScreen(),
              "GAMEPLAY": Gameplay()}
    game = Game(10, 20, screen, states, "TITLESCREEN")
    game.run()
    pg.quit()
    sys.exit()
