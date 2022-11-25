import pygame
import tetris
import figure

# Initialize the game engine
pygame.init()

paused = True
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# define screen
size = (400, 500)
screen = pygame.display.set_mode(size)

# set name
pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 25
game = tetris.Tetris(20, 10)
counter = 0
pressing_down = False

# main game loop
while not done:
    # check if game paused, with a gameover check
    if game.state != "gameover":
        if paused:
            game.state = "paused"
        else:
            game.state = "start"

    # if no figure, create a new one
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    # set
    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.move_down()

    # check inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.move_drop()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.move_side(-1)
            if event.key == pygame.K_RIGHT:
                game.move_side(1)
            if event.key == pygame.K_SPACE:
                game.rotate()
            if event.key == pygame.K_p:
                paused = not paused
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

    # check if key is held down, used to change dropping speed
    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    # set background color
    screen.fill(WHITE)

    # draw the game screen and the objects
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, figure.colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    # create the game screen
    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, figure.colors[game.figure.piece.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    # set screen variables
    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 45, True, False)
    font2 = pygame.font.SysFont('Calibri', 65, True, False)
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
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()



