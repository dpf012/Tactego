"""
File:    tactego.py
Author:  Daniel Finney
Date:    11/11/2023
Section: 31
E-mail:  dfinney1@umbc.edu
Description:
  Implement a game of Tactego.

"""

import random

# Constants
RED = 'R'
BLUE = 'B'
FLAG = 'F'
EMPTY = '.'

def initialize_board(length, width):
    """Initialize an empty game board."""
    return [[EMPTY] * width for _ in range(length)]

def load_pieces(file_name):
    """Load pieces from the specified file."""
    with open(file_name, 'r') as file:
        pieces = [line.strip().split() for line in file]
    return pieces

def place_pieces(board, pieces, player):
    """Place player pieces on the board."""
    if player == RED:
        row_range = range(len(pieces))
    elif player == BLUE:
        row_range = range(len(board) - 1, len(board) - 1 - len(pieces), -1)

    piece_index = 0
    for i, row in enumerate(row_range):
        for j in range(len(board[i])):
            if pieces[piece_index] != FLAG:
                board[row][j] = player
                pieces[piece_index] -= 1
                if pieces[piece_index] == 0:
                    piece_index += 1
            else:
                piece_index += 1

def shuffle_pieces(pieces):
    """Shuffle the order of pieces."""
    random.shuffle(pieces)

def draw_board(board):
    """Draw the current state of the board."""
    for row in board:
        print(" ".join(row))
    print()

def get_move():
    """Get a valid move from the player."""
    while True:
        try:
            start = tuple(map(int, input("Enter starting position (row col): ").split()))
            end = tuple(map(int, input("Enter ending position (row col): ").split()))
            return start, end
        except ValueError:
            print("Invalid input. Please enter two integers separated by a space.")

def is_valid_move(board, start, end, player):
    """Check if the move is valid."""
    # Check if the starting position is the player's piece
    if board[start[0]][start[1]] != player:
        return False

    # Check if the ending position is within one square in any direction
    row_diff = abs(start[0] - end[0])
    col_diff = abs(start[1] - end[1])
    if row_diff > 1 or col_diff > 1 or (row_diff == 0 and col_diff == 0):
        return False

    # Check if the ending position is not occupied by the player's own piece
    return board[end[0]][end[1]] != player

def move_piece(board, start, end):
    """Move the piece on the board."""
    board[end[0]][end[1]] = board[start[0]][start[1]]
    board[start[0]][start[1]] = EMPTY

def combat_result(attacker_strength, defender_strength):
    """Determine the result of combat."""
    if attacker_strength >= defender_strength:
        return 'win'
    else:
        return 'lose'

def tactego(pieces_file, length, width):
    # Set random seed
    random.seed(input('What is seed? '))

    # Initialize the game board
    board = initialize_board(length, width)

    # Load and shuffle red pieces
    red_pieces = load_pieces(pieces_file)
    shuffle_pieces(red_pieces)
    place_pieces(board, red_pieces, RED)

    # Load and shuffle blue pieces
    blue_pieces = load_pieces(pieces_file)
    shuffle_pieces(blue_pieces)
    place_pieces(board, blue_pieces, BLUE)

    # Main game loop
    while True:
        # Draw the current state of the board
        draw_board(board)

        # Get red player's move
        start, end = get_move()
        while not is_valid_move(board, start, end, RED):
            print("Invalid move. Please try again.")
            start, end = get_move()

        # Move the red player's piece
        move_piece(board, start, end)

        # Determine the result of combat
        combat = combat_result(int(red_pieces[start[0]][1]), int(blue_pieces[end[0]][1]))
        if combat == 'win':
            # Red player wins the combat and captures the position
            board[end[0]][end[1]] = RED
        elif combat == 'lose':
            # Blue player wins the combat, remove red player's piece
            board[start[0]][start[1]] = EMPTY

        # Check for victory condition
        if FLAG not in [piece for row in board for piece in row]:
            print("Red player wins! Blue player has lost all flags.")
            break

        # Draw the current state of the board
        draw_board(board)

        # Get blue player's move
        start, end = get_move()
        while not is_valid_move(board, start, end, BLUE):
            print("Invalid move. Please try again.")
            start, end = get_move()

        # Move the blue player's piece
        move_piece(board, start, end)

        # Determine the result of combat
        combat = combat_result(int(blue_pieces[start[0]][1]), int(red_pieces[end[0]][1]))
        if combat == 'win':
            # Blue player wins the combat and captures the position
            board[end[0]][end[1]] = BLUE
        elif combat == 'lose':
            # Red player wins the combat, remove blue player's piece
            board[start[0]][start[1]] = EMPTY

        # Check for victory condition
        if FLAG not in [piece for row in board for piece in row]:
            print("Blue player wins! Red player has lost all flags.")
            break

# Main block
if __name__ == '__main__':
    file_name = input('What is the filename for the pieces? ')
    length = int(input('What is the length? '))
    width = int(input('What is the width? '))
    pieces = load_pieces(file_name)
    tactego(pieces, length, width)
