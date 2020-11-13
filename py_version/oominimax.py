from math import inf as infinity
from random import choice
from random import seed as randomseed       # Paul Lu
import platform
import time
from os import system


def clean():
    """
    Clears the console
    """
    # Paul Lu.  Do not clear screen to keep output human readable.
    print()
    return

    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


class tictactoe:
    def __init__(self):
        """
        Initializes the attributes used by methods
        """
        self.type = str(self.__class__)
        self.h_choice = ''  # X or O
        self.c_choice = ''  # X or O
        self.first = ''  # if human is the first
        self.boardstate = state()

    def __str__(self):
        """
        Returns the string representation of this object type.
        """
        return self.type

    def __repr__(self):
        """
        Returns this object representation.
        """
        s = "<%d> %s" % (id(self), self.type)
        return s

    def start(self):
        """
        Start sequence for the game, asks user a couple questions.
        """

        # Paul Lu.  Set the seed to get deterministic behaviour for each run.
        #       Makes it easier for testing and tracing for understanding.
        randomseed(274 + 2020)
        clean()

        # Human chooses X or O to play
        while self.h_choice != 'O' and self.h_choice != 'X':
            try:
                print('')
                self.h_choice = input('Choose X or O\nChosen: ').upper()
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')

        # Setting computer's choice
        if self.h_choice == 'X':
            self.c_choice = 'O'
        else:
            self.c_choice = 'X'

        # Human chooses who starts the game
        clean()
        while self.first != 'Y' and self.first != 'N':
            try:
                self.first = input('First to start?[y/n]: ').upper()
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')
        return

    def play(self):
        """
        The main game loop, also initiates the start & end sequence
        """

        # begin the start sequence
        self.start()

        # Main loop of this game
        while len(self.boardstate.empty_cells()) > 0 and \
                not self.boardstate.game_over(self.boardstate.board):
            if self.first == 'N':
                self.ai_turn()
                self.first = ''

            self.human_turn()
            self.ai_turn()

        # game is over, begin end sequence
        self.end()

    def human_turn(self):
        """
        The Human plays choosing a valid move.
        """

        # check that the game should continue
        depth = len(self.boardstate.empty_cells())
        if depth == 0 or self.boardstate.game_over(self.boardstate.board):
            return

        # Dictionary of valid moves
        move = -1
        moves = {
            1: [0, 0], 2: [0, 1], 3: [0, 2],
            4: [1, 0], 5: [1, 1], 6: [1, 2],
            7: [2, 0], 8: [2, 1], 9: [2, 2],
        }

        # print current board
        clean()
        print(f'Human turn [{self.h_choice}]')
        self.render(self.boardstate.board)

        # get input for where user wants to place their turn
        while move < 1 or move > 9:
            try:
                move = int(input('Use numpad (1..9): '))
                coord = moves[move]
                can_move = self.boardstate.set_move(coord[0], coord[1],
                                                    self.boardstate.HUMAN)
                if not can_move:
                    print('Bad move')
                    move = -1
            except (EOFError, KeyboardInterrupt):
                print('Bye')
                exit()
            except (KeyError, ValueError):
                print('Bad choice')

    def ai_turn(self):
        """
        It calls the minimax function if the depth < 9,
        else it choices a random coordinate.
        """

        # check if the game should continue
        depth = len(self.boardstate.empty_cells())
        if depth == 0 or self.boardstate.game_over(self.boardstate.board):
            return

        # print the current board
        clean()
        print(f'Computer turn [{self.c_choice}]')
        self.render(self.boardstate.board)

        # use minimax to find optimal move
        if depth == 9:
            x = choice([0, 1, 2])
            y = choice([0, 1, 2])
        else:
            board = self.boardstate
            move = board.minimax(depth, self.boardstate.COMP)
            x, y = move[0], move[1]

        # set the move
        self.boardstate.set_move(x, y, self.boardstate.COMP)
        # Paul Lu.  Go full speed.
        # time.sleep(1)

    def end(self):
        """
        The end sequence, prints the appropriate game over message
        """

        if self.boardstate.wins(self.boardstate.board, self.boardstate.HUMAN):
            clean()
            print(f'Human turn [{self.h_choice}]')
            self.render(self.boardstate.board)
            print('YOU WIN!')
        elif self.boardstate.wins(self.boardstate.board, self.boardstate.COMP):
            clean()
            print(f'Computer turn [{self.c_choice}]')
            self.render(self.boardstate.board)
            print('YOU LOSE!')
        else:
            clean()
            self.render(self.boardstate.board)
            print('DRAW!')
        return

    def render(self, bstate):
        """
        Print the board on console
        :param bstate: current state of the board
        """

        chars = {
            -1: self.h_choice,
            +1: self.c_choice,
            0: ' '
        }
        str_line = '---------------'

        print('\n' + str_line)
        for row in bstate:
            for cell in row:
                symbol = chars[cell]
                print(f'| {symbol} |', end='')
            print('\n' + str_line)

        return


class state:
    def __init__(self):
        """
        Initializes the attributes used by methods
        """
        self.type = str(self.__class__)
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        self.HUMAN = -1
        self.COMP = +1
        return

    def __str__(self):
        """
        Returns the string representation of this object type.
        """
        return self.type

    def __repr__(self):
        """
        Returns this object representation.
        """
        s = "<%d> %s" % (id(self), self.type)
        return s

    def minimax(self, depth, player):
        """
        AI function that choice the best move
        :param depth: node index in the tree (0 <= depth <= 9),
        but never nine in this case (see iaturn() function)
        :param player: an human or a computer
        :return: a list with [the best row, best col, best score]
        """
        if player == self.COMP:
            best = [-1, -1, -infinity]
        else:
            best = [-1, -1, +infinity]

        if depth == 0 or self.game_over(self.board):
            score = self.evaluate(self.board)
            return [-1, -1, score]

        for cell in self.empty_cells():
            x, y = cell[0], cell[1]
            self.board[x][y] = player
            score = self.minimax(depth - 1, -player)
            self.board[x][y] = 0
            score[0], score[1] = x, y

            if player == self.COMP:
                if score[2] > best[2]:
                    best = score  # max value
            else:
                if score[2] < best[2]:
                    best = score  # min value

        return best

    def evaluate(self, bstate):
        """
        Function to heuristic evaluation of state.
        :param bstate: the state of the current board
        :return: +1 if the computer wins; -1 if the human wins; 0 draw
        """
        if self.wins(bstate, self.COMP):
            score = +1
        elif self.wins(bstate, self.HUMAN):
            score = -1
        else:
            score = 0

        return score

    def set_move(self, x, y, player):
        """
        Set the move on board, if the coordinates are valid
        :param x: X coordinate
        :param y: Y coordinate
        :param player: the current player
        """
        if self.valid_move(x, y):
            self.board[x][y] = player
            return True
        else:
            return False

    def valid_move(self, x, y):
        """
        A move is valid if the chosen cell is empty
        :param x: X coordinate
        :param y: Y coordinate
        :return: True if the board[x][y] is empty
        """
        if [x, y] in self.empty_cells():
            return True
        else:
            return False

    def empty_cells(self):
        """
        Each empty cell will be added into cells' list
        :return: a list of empty cells
        """
        cells = []

        for x, row in enumerate(self.board):
            for y, cell in enumerate(row):
                if cell == 0:
                    cells.append([x, y])

        return cells

    def game_over(self, bstate):
        """
        This function test if the human or computer wins
        :param bstate: the state of the current board
        :return: True if the human or computer wins
        """
        return self.wins(bstate, self.HUMAN) or self.wins(bstate, self.COMP)

    def wins(self, state, player):
        """
        This function tests if a specific player wins. Possibilities:
        * Three rows    [X X X] or [O O O]
        * Three cols    [X X X] or [O O O]
        * Two diagonals [X X X] or [O O O]
        :param state: the state of the current board
        :param player: a human or a computer
        :return: True if the player wins
        """
        win_state = [
            [state[0][0], state[0][1], state[0][2]],
            [state[1][0], state[1][1], state[1][2]],
            [state[2][0], state[2][1], state[2][2]],
            [state[0][0], state[1][0], state[2][0]],
            [state[0][1], state[1][1], state[2][1]],
            [state[0][2], state[1][2], state[2][2]],
            [state[0][0], state[1][1], state[2][2]],
            [state[2][0], state[1][1], state[0][2]],
        ]
        if [player, player, player] in win_state:
            return True
        else:
            return False


def main():
    """
    Main function that instantiates the object and calls its main method
    """
    game1 = tictactoe()
    game1.play()
    exit()


if __name__ == '__main__':
    main()
