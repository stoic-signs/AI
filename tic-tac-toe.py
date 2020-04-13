import pygame
from pygame.locals import *
import time

Player = 'x'
winner = None
draw = False
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
white = (255, 255, 255)
black = (0, 0, 0)
line_colour = (30, 30, 30)

TTT = [[None] * 3, [None] * 3, [None] * 3]
pygame.init()
fps = 30
CLOCK = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), )
pygame.display.set_caption("Tic Tac Toe")
opening = pygame.transform.scale(pygame.image.load('tic tac opening.png'),
                                 (SCREEN_WIDTH, SCREEN_HEIGHT + 10))
x_image = pygame.transform.scale(pygame.image.load('X.png'), (80, 80))
o_image = pygame.transform.scale(pygame.image.load('O.png'), (80, 80))


def game_op():
    screen.blit(opening, (0, 0))
    pygame.display.update()
    time.sleep(1)
    screen.fill(white)
    pygame.draw.line(screen, line_colour, (SCREEN_WIDTH / 3, 0),
                     (SCREEN_WIDTH / 3, SCREEN_HEIGHT), 7)
    pygame.draw.line(screen, line_colour, (SCREEN_WIDTH / 3 * 2, 0),
                     (SCREEN_WIDTH / 3 * 2, SCREEN_HEIGHT), 7)
    pygame.draw.line(screen, line_colour, (0, SCREEN_HEIGHT / 3),
                     (SCREEN_WIDTH, SCREEN_HEIGHT / 3), 7)
    pygame.draw.line(screen, line_colour, (0, SCREEN_HEIGHT / 3 * 2),
                     (SCREEN_WIDTH, SCREEN_HEIGHT / 3 * 2), 7)
    draw_status()


def draw_status():
    global draw
    if winner is None:
        message = Player.upper() + "'s Turn"
    else:
        message = winner.upper() + " won!"
    if draw:
        message = "Game Draw!"
    font = pygame.font.SysFont("Sans Serif", 30, True)
    text = font.render(message, False, white)
    screen.fill(black, (150, 400, 300, 100))
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, 500 - 50))
    screen.blit(text, text_rect)
    pygame.display.update()


def check_win():
    global TTT, winner, draw
    # check for winning rows
    for row in range(0, 3):
        if ((TTT[row][0] == TTT[row][1] == TTT[row][2]) and(TTT[row][0] is not None)):
            # this row won
            winner = TTT[row][0]
            pygame.draw.line(screen, (250, 0, 0), (0, (row + 1) * SCREEN_HEIGHT / 3 - SCREEN_HEIGHT / 6),
                             (SCREEN_WIDTH, (row + 1) * SCREEN_HEIGHT / 3 - SCREEN_HEIGHT / 6), 4)
            break
    # check for winning columns
    for col in range(0, 3):
        if (TTT[0][col] == TTT[1][col] == TTT[2][col]) and (TTT[0][col] is not None):
            # this column won
            winner = TTT[0][col]
            # draw winning line
            pygame.draw.line(screen, (250, 0, 0), ((col + 1) * SCREEN_WIDTH / 3 - SCREEN_WIDTH / 6, 0),
                             ((col + 1) * SCREEN_WIDTH / 3 - SCREEN_WIDTH / 6, SCREEN_HEIGHT), 4)
            break
    # check for diagonal winners
    if (TTT[0][0] == TTT[1][1] == TTT[2][2]) and (TTT[0][0] is not None):
        # game won diagonally left to right
        winner = TTT[0][0]
        pygame.draw.line(screen, (250, 70, 70), (50, 50), (550, 550), 4)
    if (TTT[0][2] == TTT[1][1] == TTT[2][0]) and (TTT[0][2] is not None):
        # game won diagonally right to left
        winner = TTT[0][2]
        pygame.draw.line(screen, (250, 70, 70), (550, 50), (50, 550), 4)
    if(all([all(row) for row in TTT]) and winner is None):
        draw = True
    draw_status()


def drawXO(row, col):
    global TTT, Player
    if row == 1:
        posx = 60
    elif row == 2:
        posx = SCREEN_WIDTH / 3 + 60
    else:
        posx = SCREEN_WIDTH / 3 * 2 + 60
    if col == 1:
        posy = 60
    elif col == 2:
        posy = SCREEN_HEIGHT / 3 + 60
    else:
        posy = SCREEN_HEIGHT / 3 * 2 + 60

    TTT[row - 1][col - 1] = Player
    if(Player == 'x'):
        screen.blit(x_image, (posy, posx))
        Player = 'o'
    else:
        screen.blit(o_image, (posy, posx))
        Player = 'x'
    pygame.display.update()
    # print(posx,posy)
    # print(TTT)


def userClick():
    # get coordinates of mouse click
    x, y = pygame.mouse.get_pos()
    # get column of mouse click (1-3)
    if(x < SCREEN_WIDTH / 3):
        col = 1
    elif (x < SCREEN_WIDTH / 3 * 2):
        col = 2
    elif(x < SCREEN_WIDTH):
        col = 3
    else:
        col = None
    # get row of mouse click (1-3)
    if(y < SCREEN_HEIGHT / 3):
        row = 1
    elif (y < SCREEN_HEIGHT / 3 * 2):
        row = 2
    elif(y < SCREEN_HEIGHT):
        row = 3
    else:
        row = None
    # print(row,col)
    if(row and col and TTT[row - 1][col - 1] is None):
        global Player
        # draw the x or o on screen
        drawXO(row, col)
        check_win()


def reset_game():
    global TTT, winner, Player, draw
    time.sleep(3)
    Player = 'x'
    draw = False
    winner = None
    TTT = [[None] * 3, [None] * 3, [None] * 3]
    game_op()


running = True
game_op()
pygame.display.flip()
while running:
    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            userClick()
            if (winner or draw):
                reset_game()
    pygame.display.update()
    CLOCK.tick(fps)
