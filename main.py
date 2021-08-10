import os


class TerminalColors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    INVERTED = '\033[7m'
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_BLACK = '\033[30;1m'
    BRIGHT_RED = '\033[31;1m'
    BRIGHT_GREEN = '\033[32;1m'
    BRIGHT_YELLOW = '\033[33;1m'
    BRIGHT_BLUE = '\033[34;1m'
    BRIGHT_MAGENTA = '\033[35;1m'
    BRIGHT_CYAN = '\033[36;1m'
    BRIGHT_WHITE = '\033[37;1m'
    BACKGROUND_BLACK = '\033[40m'
    BACKGROUND_RED = '\033[41m'
    BACKGROUND_GREEN = '\033[42m'
    BACKGROUND_YELLOW = '\033[43m'
    BACKGROUND_BLUE = '\033[44m'
    BACKGROUND_MAGENTA = '\033[45m'
    BACKGROUND_CYAN = '\033[46m'
    BACKGROUND_WHITE = '\033[47m'
    BACKGROUND_BRIGHT_BLACK = '\033[40;1m'
    BACKGROUND_BRIGHT_RED = '\033[41;1m'
    BACKGROUND_BRIGHT_GREEN = '\033[42;1m'
    BACKGROUND_BRIGHT_YELLOW = '\033[43;1m'
    BACKGROUND_BRIGHT_BLUE = '\033[44;1m'
    BACKGROUND_BRIGHT_MAGENTA = '\033[45;1m'
    BACKGROUND_BRIGHT_CYAN = '\033[46;1m'
    BACKGROUND_BRIGHT_WHITE = '\033[47;1m'


def get_piece_color(piece: chr) -> str:
    if piece.upper() == piece:
        return TerminalColors.BRIGHT_YELLOW
    else:
        return TerminalColors.BRIGHT_CYAN


def draw_board(board: list[list[chr]]) -> None:
    print("   ", end="")
    for i in range(8):
        print(f"  {chr(ord('A') + i)} ", end="")
    print()

    i = 1
    for y in board:
        print("   ", end="")
        for _ in y:
            print("----", end="")
        print(f"-\n {chr(ord('0') + i)} |", end="")

        for piece in y:
            print(f" {get_piece_color(piece)}{piece}{TerminalColors.RESET} |", end="")
        print(f" {chr(ord('0') + i)}")

        i += 1

    print("   ", end="")
    for _ in board[0]:
        print("----", end="")
    print("-")

    print("   ", end="")
    for i in range(8):
        print(f"  {chr(ord('A') + i)} ", end="")
    print()


def input_coord(question: str) -> (int, int, str):
    while True:
        coord = input(question).strip().upper()
        if (len(coord) == 1 and coord[0].lower() == 'x') or len(coord) == 0:
            return -1, -1, coord
        elif len(coord) != 2:
            print("Please enter valid coord e.g. C6, B2")
            continue

        coord_x = ord(coord[0]) - ord('A')
        if 1 > coord_x > 8:
            print(f"Coordinate ({coord}) is out of range!")
            continue

        coord_y = ord(coord[1]) - ord('1')
        if 1 > coord_y > 8:
            print(f"Coordinate ({coord}) is out of range!")
            continue

        return coord_x, coord_y, coord


def move_valid(from_x: int, from_y: int, to_x: int, to_y: int, board: list[list[chr]]) -> (bool, str):
    if to_x < 0 or to_x >= 8:
        return False, "You cannot move outside of the board!"

    if to_y < 0 or to_y >= 8:
        return False, "You cannot move outside of the board!"

    from_piece: chr = board[from_y][from_x]
    from_is_upper = from_piece.upper() == from_piece

    to_piece: chr = board[to_y][to_x]
    to_is_upper = to_piece.upper() == to_piece

    is_attacking = not to_piece == ' ' and ((from_is_upper and not to_is_upper) or (not from_is_upper and to_is_upper))

    dist_x = to_x - from_x
    dist_y = to_y - from_y

    if dist_x == 0 and dist_y == 0:
        return False, "You cannot move to your current position"

    if not is_attacking and not to_piece == ' ':
        return False, "You cannot attack your own team!"

    if from_piece.upper() == 'P':
        if (from_is_upper and dist_y == 1) or (not from_is_upper and dist_y == -1):
            if abs(dist_x) == 1:
                if is_attacking:
                    return True, ""
                else:
                    return False, "You can only move diagonal when attacking!"
            elif dist_x == 0:
                return True, ""
        elif (from_is_upper and dist_y == 2) or (not from_is_upper and dist_y == -2):
            if not is_attacking:
                if from_is_upper and from_y == 1:
                    return True, ""
                elif not from_is_upper and from_y == 6:
                    return True, ""
                else:
                    return False, "You can only move 2 forward on the first move!"
            else:
                return False, "You cannot move forward while attacking!"
        return False, "You cannot move there!"

    def check_horizontal() -> bool:
        assert (dist_y == 0)
        for x in range(from_x, to_x, +1 if from_x < to_x else -1):
            if x != from_x and board[from_y][x] != ' ':
                return True
        return False

    def check_vertical() -> bool:
        assert (dist_x == 0)
        for y in range(from_y, to_y, +1 if from_y < to_y else -1):
            if y != from_y and board[y][from_x] != ' ':
                return True
        return False

    def check_diagonal() -> bool:
        assert (abs(dist_x) == abs(dist_y))
        for y in range(0, dist_y, +1 if dist_y > 0 else -1):
            for x in range(0, dist_x, +1 if dist_x > 0 else -1):
                if x != 0 and y != 0 and x == y and board[from_y + y][from_x + x] != ' ':
                    return True
        return False

    if from_piece.upper() == 'R':
        if dist_y == 0:
            if check_horizontal():
                return False, "The path is obstructed!"
            else:
                return True, ""
        elif dist_x == 0:
            if check_vertical():
                return False, "The path is obstructed!"
            else:
                return True, ""
        return False, "You cannot move there!"

    if from_piece.upper() == 'H':
        if abs(dist_x) == 2 and abs(dist_y) == 1:
            return True, ""
        elif abs(dist_x) == 1 and abs(dist_y) == 2:
            return True, ""
        return False, "You cannot move there!"

    if from_piece.upper() == 'B':
        if abs(dist_x) == abs(dist_y):
            if check_diagonal():
                return False, "The path is obstructed!"
            else:
                return True, ""
        return False, "You cannot move there!"

    if from_piece.upper() == 'K':
        if abs(dist_x) <= 1 and abs(dist_y) <= 1:
            return True, ""
        return False, "You cannot move there!"

    if from_piece.upper() == 'Q':
        if dist_y == 0:
            if check_horizontal():
                return False, "The path is obstructed!"
            else:
                return True, ""
        elif dist_x == 0:
            if check_vertical():
                return False, "The path is obstructed!"
            else:
                return True, ""
        elif abs(dist_x) == abs(dist_y):
            if check_diagonal():
                return False, "The path is obstructed!"
            else:
                return True, ""
        return False, "You cannot move there!"

    return False, "Unimplemented Case"


def in_check(board: list[list[chr]], king_x: int, king_y: int, lowercase: bool) -> bool:
    for y in range(8):
        for x in range(8):
            if (board[y][x].lower() == board[y][x] and not lowercase) or (
                    board[y][x].upper() == board[y][x] and lowercase):
                (valid, error) = move_valid(x, y, king_x, king_y, board)
                if valid:
                    return True
    return False


def get_piece_pos(board: list[list[chr]], match: chr) -> (int, int):
    for y in range(8):
        for x in range(8):
            if board[y][x] == match:
                return x, y
    assert (False and "King not found!")
    return -1, -1


def main() -> None:
    if os.name == "nt":  # Windows
        os.system("color")

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
        if os.name == "nt":  # Windows
            os.system("cls")
        else:  # Linux
            os.system("clear")

        draw_board(board)

        (king_x, king_y) = get_piece_pos(board, 'k' if lowercase_turn else 'K')
        if in_check(board, king_x, king_y, lowercase_turn):
            def get_board_safe(y: int, x: int) -> chr:
                try:
                    return board[y][x]
                except IndexError:
                    return ' '

            can_move = False
            if get_board_safe(king_y + 1, king_x + 0) != ' ' and not in_check(board, king_y + 1, king_x + 0,
                                                                              lowercase_turn):
                can_move = True
            elif get_board_safe(king_y + 1, king_x + 1) != ' ' and not in_check(board, king_y + 1, king_x + 1,
                                                                                lowercase_turn):
                can_move = True
            elif get_board_safe(king_y + 1, king_x - 1) != ' ' and not in_check(board, king_y + 1, king_x - 1,
                                                                                lowercase_turn):
                can_move = True
            elif get_board_safe(king_y - 1, king_x + 0) != ' ' and not in_check(board, king_y - 1, king_x + 0,
                                                                                lowercase_turn):
                can_move = True
            elif get_board_safe(king_y - 1, king_x + 1) != ' ' and not in_check(board, king_y - 1, king_x + 1,
                                                                                lowercase_turn):
                can_move = True
            elif get_board_safe(king_y - 1, king_x - 1) != ' ' and not in_check(board, king_y - 1, king_x - 1,
                                                                                lowercase_turn):
                can_move = True
            elif get_board_safe(king_y + 0, king_x + 0) != ' ' and not in_check(board, king_y + 0, king_x + 0,
                                                                                lowercase_turn):
                can_move = True
            elif get_board_safe(king_y + 0, king_x + 1) != ' ' and not in_check(board, king_y + 0, king_x + 1,
                                                                                lowercase_turn):
                can_move = True
            elif get_board_safe(king_y + 0, king_x - 1) != ' ' and not in_check(board, king_y + 0, king_x - 1,
                                                                                lowercase_turn):
                can_move = True

            if not can_move:
                print(f"Checkmate! {'Orange' if lowercase_turn else 'Blue'} won!")
                break

        if len(error_message) > 0:
            print(f"{error_message}")
            error_message = ""

        (from_x, from_y, coord_str) = input_coord("What piece do you want to move? ")
        if from_x == -1 or from_y == -1:
            error_message = "Move canceled"
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
        if in_check(board, king_x, king_y, lowercase_turn) and from_piece != ('k' if lowercase_turn else 'K'):
            error_message = "You have to move your king you are in check!"
            continue

        (to_x, to_y, _) = input_coord(f"Move {piece_to_string[from_piece]} ({coord_str}) to where? ")
        if to_x == -1 or to_y == -1:
            error_message = "Move canceled"
            continue
        # to_piece = board[to_y][to_x]

        (valid, error) = move_valid(from_x, from_y, to_x, to_y, board)
        if not valid:
            error_message = error
            continue

        board[to_y][to_x] = board[from_y][from_x]
        board[from_y][from_x] = ' '

        if from_piece == ('k' if lowercase_turn else 'K'):
            if in_check(board, to_x, to_y, lowercase_turn):
                board[from_y][from_x] = board[to_y][to_x]
                board[to_y][to_x] = ' '
                error_message = "You cannot move into check!"
                continue

        lowercase_turn = not lowercase_turn


if __name__ == "__main__":
    main()
