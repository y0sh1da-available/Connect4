import os
import sys
import random
import numpy as np
import pygame

# Add current directory to path for local imports
HERE = os.path.dirname(__file__)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import config

# Game settings
ROW_COUNT = 6
COLUMN_COUNT = 7
CONNECT_N = 4

PLAYER = 0
AI = 1


#####################################################################################
WINDOW_LENGTH = 4
AI_PIECE = 2
PLAYER_PIECE = 1
EMPTY = 0
DEPTH = 1  # adjustable difficulty

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Positive Diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score Negative Diagonal
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def get_valid_locations(board):
    return [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]


def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE)[0] or winning_move(board, AI_PIECE)[0] or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    terminal = is_terminal_node(board)
    if depth == 0 or terminal:
        if terminal:
            if winning_move(board, AI_PIECE)[0]:
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE)[0]:
                return (None, -100000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))

    if maximizingPlayer:
        value = -np.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return best_col, value
    else:
        value = np.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return best_col, value

####################################################################################################################

# Predefined colors for PvP
color_red = (251, 79, 79)
color_yellow = (251, 201, 61)

BACKCOLOR = (108, 192, 229)
FORECOLOR = (0, 0, 0)

# Piece colors, to be set per game
piece_color1 = None
piece_color2 = None

LINE_COLOR = (0, 255, 0)
LINE_WIDTH = 10

# Globals set in run_game
screen = None
SQUARESIZE = None
height = None
RADIUS = None


def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal
    for c in range(COLUMN_COUNT - (CONNECT_N - 1)):
        for r in range(ROW_COUNT):
            if all(board[r][c + i] == piece for i in range(CONNECT_N)):
                return True, (r, c, r, c + CONNECT_N - 1)
    # Check vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - (CONNECT_N - 1)):
            if all(board[r + i][c] == piece for i in range(CONNECT_N)):
                return True, (r, c, r + CONNECT_N - 1, c)
    # Check diagonal (\)
    for c in range(COLUMN_COUNT - (CONNECT_N - 1)):
        for r in range(ROW_COUNT - (CONNECT_N - 1)):
            if all(board[r + i][c + i] == piece for i in range(CONNECT_N)):
                return True, (r, c, r + CONNECT_N - 1, c + CONNECT_N - 1)
    # Check diagonal (/)
    for c in range(COLUMN_COUNT - (CONNECT_N - 1)):
        for r in range(CONNECT_N - 1, ROW_COUNT):
            if all(board[r - i][c + i] == piece for i in range(CONNECT_N)):
                return True, (r, c, r - (CONNECT_N - 1), c + (CONNECT_N - 1))
    return False, None


def draw_winning_line(start_r, start_c, end_r, end_c):
    pygame.time.wait(500)
    start_x = (start_c + 0.5) * SQUARESIZE
    start_y = height - (start_r + 0.5) * SQUARESIZE
    end_x = (end_c + 0.5) * SQUARESIZE
    end_y = height - (end_r + 0.5) * SQUARESIZE
    pygame.draw.line(screen, LINE_COLOR, (start_x, start_y), (end_x, end_y), LINE_WIDTH)
    pygame.display.update()
    pygame.time.wait(2000)


def draw_board(board):
    # Draw grid and empty slots
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            pygame.draw.rect(screen, BACKCOLOR,
                             (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE,
                              SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, FORECOLOR,
                               (int(c * SQUARESIZE + SQUARESIZE / 2),
                                int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                               RADIUS)
    # Draw pieces
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, piece_color1,
                                   (int(c * SQUARESIZE + SQUARESIZE / 2),
                                    height - int(r * SQUARESIZE + SQUARESIZE / 2)),
                                   RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, piece_color2,
                                   (int(c * SQUARESIZE + SQUARESIZE / 2),
                                    height - int(r * SQUARESIZE + SQUARESIZE / 2)),
                                   RADIUS)
    pygame.display.update()


def run_game(pvp=True):
    global screen, SQUARESIZE, height, RADIUS, piece_color1, piece_color2
    if not pvp:
        if config.difficulty == "Easy":
            DEPTH = 1
        elif config.difficulty == "Medium":
            DEPTH = 3
        elif config.difficulty == "Hard":
            DEPTH = 5

    board = create_board()
    game_over = False
    winner_piece = None

    pygame.init()
    pygame.mixer.init()

    # Load sounds
    drop_sound = pygame.mixer.Sound(os.path.join(HERE, "tha.mp3"))
    win_sound = pygame.mixer.Sound(os.path.join(HERE, "victory.mp3"))
    lose_sound = pygame.mixer.Sound(os.path.join(HERE, "lose.mp3"))
    pygame.mixer.music.set_volume(1.0 if config.sound_on else 0.0)

    # Determine piece colors
    if pvp:
        # Randomly assign red and yellow to players
        if random.choice([True, False]):
            piece_color1 = color_red
            piece_color2 = color_yellow
        else:
            piece_color1 = color_yellow
            piece_color2 = color_red
    else:
        # Default colors for Player vs Bot
        piece_color1 = color_red
        piece_color2 = color_yellow

    # Setup display
    SQUARESIZE = 100
    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE
    screen = pygame.display.set_mode((width, height))
    RADIUS = int(SQUARESIZE / 2 - 5)
    draw_board(board)

    # Random first turn and piece mapping
    turn = random.randint(PLAYER, AI)
    piece_map = {turn: 1, (turn + 1) % 2: 2}

    # Create a mapping for piece ownership (Player vs Bot or PvP)
    piece_to_player = {
        piece_map[PLAYER]: "Player 1" if pvp else "Player",
        piece_map[AI]: "Player 2" if pvp else "Bot"
    }

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, FORECOLOR, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                hover_piece = piece_map[turn]
                color = piece_color1 if hover_piece == 1 else piece_color2
                pygame.draw.circle(screen, color, (posx, SQUARESIZE // 2), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, FORECOLOR, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                col = posx // SQUARESIZE

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    if config.sound_on:
                        drop_sound.play()

                    piece = piece_map[turn]
                    drop_piece(board, row, col, piece)
                    draw_board(board)

                    won, coords = winning_move(board, piece)
                    if won:
                        winner_piece = piece
                        if config.sound_on:
                            win_sound.play()
                        pygame.display.update()
                        draw_winning_line(*coords)
                        game_over = True
                    elif is_terminal_node(board):
                        if config.sound_on:
                            lose_sound.play()
                        game_over = True
                    else:
                        turn = (turn + 1) % 2

                print_board(board)

        # AI move
        if not pvp and turn == AI and not game_over:
            col, minimax_score = minimax(board, DEPTH, -np.inf, np.inf, True)
            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                if config.sound_on:
                    drop_sound.play()

                piece = piece_map[turn]
                drop_piece(board, row, col, piece)
                draw_board(board)

                won, coords = winning_move(board, piece)
                if won:
                    winner_piece = piece
                    if config.sound_on:
                        (win_sound if piece == 1 else lose_sound).play()
                    pygame.display.update()
                    draw_winning_line(*coords)
                    game_over = True

                print_board(board)
                if not game_over and is_terminal_node(board):
                    if config.sound_on:
                        lose_sound.play()
                    game_over = True
                else:
                    turn = (turn + 1) % 2

    from winner_popup import show_winner_popup
    from menu import main_menu

    # Display win message based on PvP or PvE mode
    if winner_piece is not None:
        if pvp:
            result = show_winner_popup(screen, winner=f"Player {1 if winner_piece == 1 else 2} wins", on_restart=lambda: run_game(pvp))
        else:
            result = show_winner_popup(screen, winner=f"{piece_to_player[winner_piece]} wins", on_restart=lambda: run_game(pvp))

        if result == "home":
            main_menu()
        elif result == "restart":
            run_game(pvp)  # Restart game
