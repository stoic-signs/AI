import pygame
from pygame.locals import *
import time
from minimax import *


winner = None
draw = False
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
white = (255, 255, 255)
black = (0, 0, 0)
line_colour = (30, 30, 30)
TTT = None
ttt = None
result = None
choices = None
CLOCK = pygame.time.Clock()
global state, Player, inputs, size, win
Player = 'X'


def game_op():
    screen.blit(opening, (0, 0))
    pygame.display.update()
    time.sleep(1)
    screen.fill(white)
    font = pygame.font.SysFont("Liberation Sans", 30, True)
    message1 = "Instructions: Enter space-separated"
    message2 = "board size,"
    message3 = "coins in a row to win,"
    message4 = "and the algorithm you wish to use"
    message5 = "1 - minimax    2 - minimax_cutoff"
    message6 = "3 - alpha_beta_pruning     4 - alpha_beta_cutoff"
    text1 = font.render(message1, True, black)
    text_rect1 = text1.get_rect(center=(SCREEN_WIDTH / 2, 50))
    screen.blit(text1, text_rect1)
    text2 = font.render(message2, True, black)
    text_rect2 = text2.get_rect(center=(SCREEN_WIDTH / 2, 150))
    screen.blit(text2, text_rect2)
    text3 = font.render(message3, True, black)
    text_rect3 = text3.get_rect(center=(SCREEN_WIDTH / 2, 250))
    screen.blit(text3, text_rect3)
    text4 = font.render(message3, True, black)
    text_rect4 = text4.get_rect(center=(SCREEN_WIDTH / 2, 350))
    screen.blit(text4, text_rect4)
    text5 = font.render(message5, True, black)
    text_rect5 = text5.get_rect(center=(SCREEN_WIDTH / 2, 450))
    screen.blit(text5, text_rect5)
    text6 = font.render(message6, True, black)
    text_rect6 = text6.get_rect(center=(SCREEN_WIDTH / 2, 550))
    screen.blit(text6, text_rect6)
    pygame.display.update()
    time.sleep(3)
    screen.fill(white)
    pygame.display.update()
    time.sleep(2)


def draw_grid():
    screen.fill(white)
    for i in range(1, size):
        pygame.draw.line(screen, line_colour, (SCREEN_WIDTH / size * i, 0),
                         (SCREEN_WIDTH / size * i, SCREEN_HEIGHT), 7)
        pygame.draw.line(screen, line_colour, (0, SCREEN_HEIGHT / size * i),
                         (SCREEN_WIDTH, SCREEN_HEIGHT / size * i), 7)
        pygame.display.update()


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


# def check_win():
#     global TTT, winner, draw
#     # check for winning rows
#     for row in range(0, 3):
#         if ((TTT[row][0] == TTT[row][1] == TTT[row][2]) and(TTT[row][0] is not None)):
#             # this row won
#             winner = TTT[row][0]
#             pygame.draw.line(screen, (250, 0, 0), (0, (row + 1) * SCREEN_HEIGHT / 3 - SCREEN_HEIGHT / 6),
#                              (SCREEN_WIDTH, (row + 1) * SCREEN_HEIGHT / 3 - SCREEN_HEIGHT / 6), 4)
#             break
#     # check for winning columns
#     for col in range(0, 3):
#         if (TTT[0][col] == TTT[1][col] == TTT[2][col]) and (TTT[0][col] is not None):
#             # this column won
#             winner = TTT[0][col]
#             # draw winning line
#             pygame.draw.line(screen, (250, 0, 0), ((col + 1) * SCREEN_WIDTH / 3 - SCREEN_WIDTH / 6, 0),
#                              ((col + 1) * SCREEN_WIDTH / 3 - SCREEN_WIDTH / 6, SCREEN_HEIGHT), 4)
#             break
#     # check for diagonal winners
#     if (TTT[0][0] == TTT[1][1] == TTT[2][2]) and (TTT[0][0] is not None):
#         # game won diagonally left to right
#         winner = TTT[0][0]
#         pygame.draw.line(screen, (250, 70, 70), (50, 50), (550, 550), 4)
#     if (TTT[0][2] == TTT[1][1] == TTT[2][0]) and (TTT[0][2] is not None):
#         # game won diagonally right to left
#         winner = TTT[0][2]
#         pygame.draw.line(screen, (250, 70, 70), (550, 50), (50, 550), 4)
#     if(all([all(row) for row in TTT]) and winner is None):
#         draw = True
#     draw_status()


def drawXO(row, col):
    global ttt, Player
    if row == 1:
        posx = 60
    elif row == 2:
        posx = SCREEN_WIDTH / size + 60
    else:
        posx = SCREEN_WIDTH / size * 2 + 60
    if col == 1:
        posy = 60
    elif col == 2:
        posy = SCREEN_HEIGHT / size + 60
    else:
        posy = SCREEN_HEIGHT / size * 2 + 60

    ttt[row - 1][col - 1] = Player
    if(Player == 'X'):
        screen.blit(x_image, (posy, posx))
        Player = 'X'
    else:
        screen.blit(o_image, (posy, posx))
        Player = 'X'
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
    if(row and col and ttt[row - 1][col - 1] is None):
        global Player
        # draw the x or o on screen
        drawXO(row, col)
    return row, col


def reset_game():
    global ttt, winner, Player, draw
    time.sleep(3)
    Player = 'X'
    draw = False
    winner = None
    ttt = [[None] * size for i in range(size)]
    TTT = TicTacToe(size, win)
    game_op()


if __name__ == "__main__":
    pygame.init()
    fps = 30
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), )
    pygame.display.set_caption("Tic Tac Toe")
    opening = pygame.transform.scale(pygame.image.load('tic tac opening.png'),
                                     (SCREEN_WIDTH, SCREEN_HEIGHT + 10))

    running = True
    end_state = False
    game_op()
    pygame.display.flip()
    n = int(input("Please enter size of board: "))
    size = n
    x_image = pygame.transform.scale(pygame.image.load(
        'X.png'), (50, 50))
    o_image = pygame.transform.scale(pygame.image.load('O.png'), (50,
                                                                  50))
    k = int(input("Please enter coins required to win: "))
    win = k
    draw_grid()
    choice = int(input("Choose from minimax(1), alpha_beta(2),"
                       " cutoff(3) and alpha_beta_cutoff(4): "))
    TTT = TicTacToe(n, k)
    state = TTT.initial
    Player = state.to_move
    ttt = [[None] * n for i in range(n)]
    draw_status()
    while running and not end_state:
        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                state = TTT.result(state, userClick())
                Player = state.to_move
                if (winner or draw):
                    reset_game()
                if TTT.terminal_test(state):
                    pygame.display.update()
                    # print(TTT.utility(state, state.to_move))
                    if TTT.utility(state, state.to_move) < 0:
                        print("Player 1 wins!")
                    else:
                        print("Game was a Draw.")
                    break
                if choice == 1:
                    x, y = basic_minimax(state, TTT)
                    print("AI moves: (" + str(x) + "," + str(y) + ")")
                elif choice == 2:
                    x, y = alpha_beta_pruning(state, TTT)
                    print("AI moves: (" + str(x) + "," + str(y) + ")")
                elif choice == 3:
                    x, y = minimax_cutoff(state, TTT, 9)
                    print("AI moves: (" + str(x) + "," + str(y) + ")")
                elif choice == 4:
                    x, y = alpha_beta_cutoff(state, TTT, 9)
                    print("AI moves: (" + str(x) + "," + str(y) + ")")
                drawXO(x, y)
                state = TTT.result(state, (x, y))
                Player = state.to_move
                if TTT.terminal_test(state):
                    TTT.display(state)
                    if TTT.utility(state, state.to_move) != 0:
                        print("Player 2 wins!")
                    else:
                        print("Game was a Draw.")
                    end_state = True
                #print(TTT.utility(state, state.to_move))
                # print()
        pygame.display.update()
        CLOCK.tick(fps)

        # print("Enter move: ")
        # (x, y) = int(i.strip()) for i in raw_input().split(' ')
        # TTT.
        # move = (query_player(TTT, state))
        #print(TTT.utility(state, state.to_move))
        # TTT.display(state)
