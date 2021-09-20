import terminal_util


def get_piece_color(piece: chr) -> str:
    if piece.upper() == piece:
        return terminal_util.Colors.BRIGHT_RED + terminal_util.Colors.BOLD
    else:
        return terminal_util.Colors.BRIGHT_MAGENTA + terminal_util.Colors.BOLD


def draw_board(board: list[list[chr]]) -> None:
    print("   ", end="")
    for i in range(8):
        print(f"  {chr(ord('A') + i)} ", end="")
    print()

    i = 1
    j = 0
    for y in board:
        print("   ", end="")
        for _ in y:
            print("----", end="")
        print(f"-\n {chr(ord('0') + i)} |", end="")

        for piece in y:
            j += 1
            print(
                f"{terminal_util.Colors.BACKGROUND_BRIGHT_BLACK if j % 2 == 0 else terminal_util.Colors.BACKGROUND_BRIGHT_WHITE}{get_piece_color(piece)} {piece} {terminal_util.Colors.RESET}|",
                end="")
        print(f" {chr(ord('0') + i)}")

        i += 1
        j += 1

    print("   ", end="")
    for _ in board[0]:
        print("----", end="")
    print("-")

    print("   ", end="")
    for i in range(8):
        print(f"  {chr(ord('A') + i)} ", end="")
    print()


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


def get_king_pos(board: list[list[chr]], match: chr) -> (int, int):
    for y in range(8):
        for x in range(8):
            if board[y][x] == match:
                return x, y
    assert (False and "King not found!")
    return -1, -1


def is_checkmate(board: list[list[chr]], lowercase_turn: bool) -> bool:
    (king_x, king_y) = get_king_pos(board, 'k' if lowercase_turn else 'K')
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

        return not can_move
