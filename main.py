import os

import terminal_util
import chess


def input_coord(question: str) -> (int, int, str):
    while True:
        coord = input(question).strip().upper()
        if len(coord) == 0:
            return -1, -1, coord
        elif len(coord) != 2:
            print("Please enter valid coord e.g. C6, B2")
            continue

        coord_x = ord(coord[0]) - ord('A')
        if coord_x < 0 or coord_x > 7:
            print(f"Coordinate ({coord}) is out of range!")
            continue

        coord_y = ord(coord[1]) - ord('1')
        if coord_y < 0 or coord_y > 7:
            print(f"Coordinate ({coord}) is out of range!")
            continue

        return coord_x, coord_y, coord


def show_instructions() -> None:
    print("Q or q: Queen")
    print("    The queen can move vertically, horizontally, or diagonally in a straight line")
    print()
    print("K or k: King")
    print("    The king can move on unit in any direction")
    print()
    print("B or b: Bishop")
    print("    The bishop can move diagonally in a straight line")
    print()
    print("H or h: Horse")
    print("    The horse can move in a L shape e.g. 2 up 1 left")
    print()
    print("R or r: Rook")
    print("    The rook can move vertically or horizontally in a straight line")
    print()
    print("P or p: Pawn")
    print("    The pawn can move 1 square forward, 2 on its first turn, and to attack it moves 1 square diagonally")
    print()


def main() -> None:
    terminal_util.enable_color()
    terminal_util.clear()

    show_instructions()
    terminal_util.wait_for_key()

    piece_to_string: dict[chr, str] = {
        'Q': "Queen",
        'K': "King",
        'B': "Bishop",
        'H': "Horse",
        'R': "Rook",
        'P': "Pawn",
        'q': "Queen",
        'k': "King",
        'b': "Bishop",
        'h': "Horse",
        'r': "Rook",
        'p': "Pawn",
    }

    board: list[list[chr]] = [
        ['R', 'H', 'B', 'K', 'Q', 'B', 'H', 'R'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['r', 'h', 'b', 'k', 'q', 'b', 'h', 'r'],
    ]

    lowercase_turn: bool = True

    error_message: str = ""
    while True:
        terminal_util.clear()

        chess.draw_board(board)

        if chess.is_checkmate(board, lowercase_turn):
            print(f"Checkmate! {'Orange' if lowercase_turn else 'Blue'} won!")

        if len(error_message) > 0:
            print(f"{error_message}")
            error_message = ""

        (from_x, from_y, coord_str) = input_coord("What piece do you want to move? ")
        if from_x == -1 or from_y == -1:
            continue
        from_piece = board[from_y][from_x]

        if from_piece == ' ':
            error_message = "You cannot move nothing!"
            continue

        if from_piece.lower() == from_piece and not lowercase_turn:
            error_message = "Its not your turn!"
            continue
        elif from_piece.upper() == from_piece and lowercase_turn:
            error_message = "Its not your turn!"
            continue

        # TODO: Should this removed? It just adds more complexity and issues with the code
        if chess.in_check(board, king_x, king_y, lowercase_turn) and from_piece != ('k' if lowercase_turn else 'K'):
            error_message = "You have to move your king you are in check!"
            continue

        (to_x, to_y, _) = input_coord(f"Move {piece_to_string[from_piece]} ({coord_str}) to where? ")
        if to_x == -1 or to_y == -1:
            error_message = "Move canceled"
            continue
        # to_piece = board[to_y][to_x]

        (valid, error) = chess.move_valid(from_x, from_y, to_x, to_y, board)
        if not valid:
            error_message = error
            continue

        board[to_y][to_x] = board[from_y][from_x]
        board[from_y][from_x] = ' '

        if from_piece == ('k' if lowercase_turn else 'K'):
            if chess.in_check(board, to_x, to_y, lowercase_turn):
                board[from_y][from_x] = board[to_y][to_x]
                board[to_y][to_x] = ' '
                error_message = "You cannot move into check!"
                continue
        elif (from_piece == 'P' and to_y == 7) or (from_piece == 'p' and to_y == 0):
            print("You have gotten a pawn to the other side of the board!")
            while True:
                piece = input("Please enter a piece that you want to promote the pawn to: ")
                if piece_to_string.get(piece.lower()) is None or piece.lower() == 'k' or piece.lower() == 'p':
                    print("Please enter a valid piece")
                    continue
                break
            board[to_y][to_x] = piece.lower() if lowercase_turn else piece.upper()

        lowercase_turn = not lowercase_turn


if __name__ == "__main__":
    main()
