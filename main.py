import sys
import pygame
import pygame.display

import figure
import highScore
import tetris

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

clock = pygame.time.Clock()
fps = 60


class GameState(object):
    """
    Parent class for individual game states to inherit from.
    """

    def __init__(self):
        self.done = False
        self.quit = False
        self.next_state = None
        self.screen_rect = pygame.display.get_surface().get_rect()
        self.persist = {}
        self.font = pygame.font.Font(None, 24)

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
        self.title = self.font.render("Python tetris.py", True, pygame.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = "black"
        self.next_state = "GAMEPLAY"

    # continue on any button press
    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYUP:
            self.persist["screen_color"] = "gold"
            self.done = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.persist["screen_color"] = "dodgerblue"
            self.done = True

    # renders the screen
    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        # Add background image to tile screen
        titleImage = pygame.image.load("images/titleImage.jpg").convert()
        titleImage = pygame.transform.scale(titleImage, (400, 500)) 
        surface.blit(titleImage, ( 0,0))
        surface.blit(self.title, self.title_rect)


class PauseScreen(GameState):
    def __init__(self):
        super(PauseScreen, self).__init__()
        self.title = self.font.render("Paused, press r to resume", True, pygame.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = "black"
        self.next_state = "GAMEPLAY"

    # continue on any button press
    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.done = True
                game.flip_state()

    # renders the screen
    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.title, self.title_rect)


class HigscoreScreen(GameState):
    def __init__(self):
        super(HigscoreScreen, self).__init__()
        self.title = self.font.render("HighScores: ", True, pygame.Color("dodgerblue"))
        self.persist["screen_color"] = "black"

        # create rectangle
        self.input_rect = pygame.Rect(150, 280, 140, 32)

    # continue on any button press
    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.quit = True

    # renders the screen
    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.title, [160, 100, 240, 240])

        # Get the highscores
        scores = highScore.gethighscores()

        # create scores text for the 10 entries
        score1 = self.font.render("Name: " + scores[0].name + " score: " + str(scores[0].score), True, pygame.Color("dodgerblue"))
        score2 = self.font.render("Name: " + scores[1].name + " score: " + str(scores[1].score), True, pygame.Color("dodgerblue"))
        score3 = self.font.render("Name: " + scores[2].name + " score: " + str(scores[2].score), True, pygame.Color("dodgerblue"))
        score4 = self.font.render("Name: " + scores[3].name + " score: " + str(scores[3].score), True, pygame.Color("dodgerblue"))
        score5 = self.font.render("Name: " + scores[4].name + " score: " + str(scores[4].score), True, pygame.Color("dodgerblue"))
        score6 = self.font.render("Name: " + scores[5].name + " score: " + str(scores[5].score), True, pygame.Color("dodgerblue"))
        score7 = self.font.render("Name: " + scores[6].name + " score: " + str(scores[6].score), True, pygame.Color("dodgerblue"))
        score8 = self.font.render("Name: " + scores[7].name + " score: " + str(scores[7].score), True, pygame.Color("dodgerblue"))
        score9 = self.font.render("Name: " + scores[8].name + " score: " + str(scores[8].score), True, pygame.Color("dodgerblue"))
        score10 = self.font.render("Name: " + scores[9].name + " score: " + str(scores[9].score), True, pygame.Color("dodgerblue"))

        surface.blit(score1, [120, 120, 240, 240])
        surface.blit(score2, [120, 140, 240, 240])
        surface.blit(score3, [120, 160, 240, 240])
        surface.blit(score4, [120, 180, 240, 240])
        surface.blit(score5, [120, 200, 240, 240])
        surface.blit(score6, [120, 220, 240, 240])
        surface.blit(score7, [120, 240, 240, 240])
        surface.blit(score8, [120, 260, 240, 240])
        surface.blit(score9, [120, 280, 240, 240])
        surface.blit(score10, [120, 300, 240, 240])
        # display.flip() will update only a portion of the
        # screen to updated, not full area
        pygame.display.flip()


class GameOverScreen(GameState):
    def __init__(self):
        super(GameOverScreen, self).__init__()
        self.title = self.font.render("press Escape to quit", True, pygame.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist["screen_color"] = "black"
        self.user_text = ""
        self.next_state = "HIGHSCORE"

        # create rectangle
        self.input_rect = pygame.Rect(150, 280, 140, 32)

    # continue on any button press
    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                highScore.addhighscore(self.user_text, score)
                game.flip_state()
                # Check for backspace
            if event.key == pygame.K_BACKSPACE:

                # get text input from 0 to -1 i.e. end.
                self.user_text = self.user_text[:0]

                # Unicode standard is used for string
                # formation
            else:
                self.user_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False

    # renders the screen
    def draw(self, surface):
        scoretext = self.font.render("Score: " + str(score), True, pygame.Color("dodgerblue"))

        surface.fill(pygame.Color("black"))
        gameOverImage = pygame.image.load("images/gameOver.png").convert()
        gameOverImage = pygame.transform.scale(gameOverImage, (400, 500))
        surface.blit(gameOverImage, ( 0,0))
        surface.blit(scoretext, [170, 200])
        surface.blit(self.title, self.title_rect)

        # basic font for user typed
        base_font = pygame.font.Font(None, 32)

        # draw rectangle and argument passed which should
        # be on screen
        pygame.draw.rect(screen, WHITE, self.input_rect)

        text_surface = base_font.render(self.user_text, True, (0, 0, 0))

        # render at position stated in arguments
        screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        # set width of textfield so that text cannot get
        # outside of user's text input
        self.input_rect.w = max(100, text_surface.get_width() + 10)

        # display.flip() will update only a portion of the
        # screen to updated, not full area
        pygame.display.flip()


class Gameplay(GameState):
    def __init__(self):
        super(Gameplay, self).__init__()
        self.rect = pygame.Rect((0, 0), (128, 128))
        self.x_velocity = 1
        self.next_state = "GAMEOVER"

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.move_drop()
            if event.key == pygame.K_DOWN:
                game.pressing_down = True
            if event.key == pygame.K_LEFT:
                game.move_side(-1)
            if event.key == pygame.K_RIGHT:
                game.move_side(1)
            if event.key == pygame.K_SPACE:
                game.rotate()
            if event.key == pygame.K_v:
                game.revrotate()
            if event.key == pygame.K_c:
                game.hold()
            if event.key == pygame.K_ESCAPE:
                self.done = True
            if event.key == pygame.K_p:
                self.next_state = "PAUSED"
                self.done = True

        # check if key is held down, used to change dropping speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                game.pressing_down = False

    def update(self, dt):
        # move piece down every +- 200 ticks
        game.time_elapsed += dt
        if game.time_elapsed/game.level > 200 or game.pressing_down:
            game.time_elapsed = 0
            game.move_down()

        self.rect.move_ip(self.x_velocity, 0)
        if (self.rect.right > self.screen_rect.right
                or self.rect.left < self.screen_rect.left):
            self.x_velocity *= -1
            self.rect.clamp_ip(self.screen_rect)

    def draw(self, surface):
        # set background color
        screen.fill(WHITE)
        backgroundImage = pygame.image.load("images/background.jpg").convert()
        backgroundImage = pygame.transform.scale(backgroundImage, (400, 500))
        surface.blit(backgroundImage, ( 0,0))

        # draw the grid
        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom],
                                 1)
                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, figure.colors[game.field[i][j]],
                                     [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2,
                                      game.zoom - 1])

        # draw the preview1 window
        for i in range(4):
            for j in range(3):
                pygame.draw.rect(screen, GRAY, [320 + 20 * j, 60 + i * 20, game.zoom, game.zoom],
                                 1)

        # draw the preview2 window
        for i in range(4):
            for j in range(3):
                pygame.draw.rect(screen, GRAY, [320 + 20 * j, 160 + i * 20, game.zoom, game.zoom],
                                 1)

        # draw the preview3 window
        for i in range(4):
            for j in range(3):
                pygame.draw.rect(screen, GRAY, [320 + 20 * j, 260 + i * 20, game.zoom, game.zoom],
                                 1)

        # draw the hold window
        for i in range(4):
            for j in range(3):
                pygame.draw.rect(screen, GRAY, [20 + 20 * j, 60 + i * 20, game.zoom, game.zoom],
                                 1)
        # draw the figure on the screen
        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.figure.image():
                        pygame.draw.rect(screen, figure.colors[game.figure.piece.color],
                                         [game.x + game.zoom * (j + game.figure.x) + 1,
                                          game.y + game.zoom * (i + game.figure.y) + 1,
                                          game.zoom - 2, game.zoom - 2])

        # draw the preview figure1
        if game.next_figure is not None:
            for i in range(4):
                for j in range(3):
                    p = i * 4 + j
                    if p in game.next_figure.image():
                        pygame.draw.rect(screen, figure.colors[game.next_figure.piece.color],
                                         [320 + 20 * j + 1, 60 + i * 20 + 1, game.zoom - 2, game.zoom - 2])

        # draw the preview figure2
        if game.next_figure2 is not None:
            for i in range(4):
                for j in range(3):
                    p = i * 4 + j
                    if p in game.next_figure2.image():
                        pygame.draw.rect(screen, figure.colors[game.next_figure2.piece.color],
                                         [320 + 20 * j + 1, 160 + i * 20 + 1, game.zoom - 2, game.zoom - 2])

        # draw the preview figure3
        if game.next_figure3 is not None:
            for i in range(4):
                for j in range(3):
                    p = i * 4 + j
                    if p in game.next_figure3.image():
                        pygame.draw.rect(screen, figure.colors[game.next_figure3.piece.color],
                                         [320 + 20 * j + 1, 260 + i * 20 + 1, game.zoom - 2, game.zoom - 2])

        # draw the preview figure3
        if game.hold_figure is not None:
            for i in range(4):
                for j in range(3):
                    p = i * 4 + j
                    if p in game.hold_figure.image():
                        pygame.draw.rect(screen, figure.colors[game.hold_figure.piece.color],
                                         [20 + 20 * j + 1, 60 + i * 20 + 1, game.zoom - 2, game.zoom - 2])

        # set screen variables
        font = pygame.font.SysFont('Calibri', 25, True, False)
        text = font.render("Score: " + str(game.score), True, GRAY)

        screen.blit(text, [0, 0])

        # may need to use persist, haven't figured it out yet
        global score
        score = game.score

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    score = 0
    size = (400, 500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("tetris.py")
    states = {"TITLESCREEN": TitleScreen(),
              "GAMEPLAY": Gameplay(),
              "GAMEOVER": GameOverScreen(),
              "PAUSED": PauseScreen(),
              "HIGHSCORE": HigscoreScreen()}
    game = tetris.Tetris(10, 20, screen, states, "TITLESCREEN")
    game.run()
    pygame.quit()
    sys.exit()
