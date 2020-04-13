from minimax import *

TTT = None
result = None
choices = None
global state
if __name__ == '__main__':
    n = int(input("Please enter size of board: "))
    k = int(input("Please enter coins required to win: "))
    choice = int(input("Choose from minimax(1), alpha_beta(2),"
                       " cutoff(3) and alpha_beta_cutoff(4): "))
    TTT = TicTacToe(n, k)
    state = TTT.initial
    # result = StringVar()
    # player1 = alpha_beta_player(state, TTT)
    # player2 = minimax_player(state, TTT)
    # result = "Your Turn!"
    end_state = False
    while not end_state:
        # print("Enter move: ")
        # (x, y) = int(i.strip()) for i in raw_input().split(' ')
        # TTT.
        #move = (query_player(TTT, state))
        state = TTT.result(state, query_player(TTT, state))
        print(TTT.utility(state, state.to_move))
        if TTT.terminal_test(state):
            end_state = True
            TTT.display(state)
            # print(TTT.utility(state, state.to_move))
            if TTT.utility(state, state.to_move) < 0:
                print("Player 1 wins!")
            else:
                print("Game was a Draw.")
            break
        print()
        print("current state:")
        TTT.display(state)
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
        state = TTT.result(state, (x, y))
        print(TTT.utility(state, state.to_move))
        # TTT.display(state)
        if TTT.terminal_test(state):
            TTT.display(state)
            print("Player 2 wins!")
            end_state = True
