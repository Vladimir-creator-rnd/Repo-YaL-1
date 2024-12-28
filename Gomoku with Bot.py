import pygame
import sys
import random

# Константы
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 15
CELL_SIZE = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
gameover = False
start_x_for_winner = 0
start_y_for_winner = 0
finish_x_for_winner = 0
finish_y_for_winner = 0


# Функция для инициализации Pygame
def init_game():
    pygame.init()
    return pygame.display.set_mode((WIDTH, HEIGHT)), pygame.font.Font(None, 36)


def check_winner_for_move(board, player):
    global start_x_for_winner, start_y_for_winner, finish_x_for_winner, finish_y_for_winner
    # Проверка горизонталей, вертикалей и диагоналей
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if board[x][y] == player:
                if x + 4 < GRID_SIZE and all(board[x + i][y] == player for i in range(5)):
                    return True
                if y + 4 < GRID_SIZE and all(board[x][y + i] == player for i in range(5)):
                    return True
                if x + 4 < GRID_SIZE and y + 4 < GRID_SIZE and all(board[x + i][y + i] == player for i in range(5)):
                    return True
                if x - 4 >= 0 and y + 4 < GRID_SIZE and all(board[x - i][y + i] == player for i in range(5)):
                    return True
    return False


# Функция для отрисовки сетки
def draw_grid(screen):
    for x in range(GRID_SIZE + 1):
        pygame.draw.line(screen, BLACK, (x * CELL_SIZE - CELL_SIZE / 2, 0), (x * CELL_SIZE - CELL_SIZE / 2, HEIGHT))
        pygame.draw.line(screen, BLACK, (0, x * CELL_SIZE - CELL_SIZE / 2), (WIDTH, x * CELL_SIZE - CELL_SIZE / 2))


def draw_winner_line(screen):
    global gameover
    if start_x_for_winner != 0 or start_y_for_winner != 0 or finish_x_for_winner != 0 or finish_y_for_winner != 0:
        pygame.draw.line(screen, BLACK, (int(start_x_for_winner), int(start_y_for_winner)),
                         (int(finish_x_for_winner), int(finish_y_for_winner)), 10)
        return True


def simple_bot_move(board):
    available_moves = get_available_moves(board)
    # Сначала проверяем, может ли бот выиграть
    for x, y in available_moves:
        board[x][y] = "O"
        if check_winner_for_move(board, "O"):
            return x, y
        board[x][y] = None
    for x, y in available_moves:
        board[x][y] = "X"
        if check_winner_for_move(board, "X"):
            board[x][y] = None
            return x, y
        board[x][y] = None
    # Блокировка игрока
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if board[x][y] is None:  # Проверяем пустую клетку
                # Проверяем горизонтально
                if (y + 2 < GRID_SIZE and
                        board[x][y + 1] == "X" and
                        board[x][y + 2] == "X"):
                    return (x, y)  # Блокируем горизонтально
                # Проверяем вертикально
                if (x + 2 < GRID_SIZE and
                        board[x + 1][y] == "X" and
                        board[x + 2][y] == "X"):
                    return (x, y)  # Блокируем вертикально
                # Проверяем диагонали
                if (x + 2 < GRID_SIZE and y + 2 < GRID_SIZE and
                        board[x + 1][y + 1] == "X" and
                        board[x + 2][y + 2] == "X"):
                    return (x, y)  # Блокируем диагональ \
                if (x + 2 < GRID_SIZE and y - 2 >= 0 and
                        board[x + 1][y - 1] == "X" and
                        board[x + 2][y - 2] == "X"):
                    return (x, y)  # Блокируем диагональ /

    x = random.randint(0, 14)
    y = random.randint(0, 14)
    if board[x][y] is None:
        return (x, y)  # Возвращаем первую найденную пустую клетку

    return None  # Если нет доступных ходов


def get_available_moves(board):
    return [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) if board[x][y] is None]


# Функция для проверки победителя
def check_winner(board, player):
    global start_x_for_winner, start_y_for_winner, finish_x_for_winner, finish_y_for_winner
    # Проверка горизонталей, вертикалей и диагоналей
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if board[x][y] == player:
                if x + 4 < GRID_SIZE and all(board[x + i][y] == player for i in range(5)):
                    start_x_for_winner = (x + 1) * CELL_SIZE - CELL_SIZE
                    start_y_for_winner = (y + 1) * CELL_SIZE - CELL_SIZE / 2
                    finish_x_for_winner = (x + 5) * CELL_SIZE
                    finish_y_for_winner = (y + 1) * CELL_SIZE - CELL_SIZE / 2
                    return True
                if y + 4 < GRID_SIZE and all(board[x][y + i] == player for i in range(5)):
                    start_x_for_winner = (x + 1) * CELL_SIZE - CELL_SIZE / 2
                    start_y_for_winner = (y + 1) * CELL_SIZE - CELL_SIZE
                    finish_x_for_winner = (x + 1) * CELL_SIZE - CELL_SIZE / 2
                    finish_y_for_winner = (y + 5) * CELL_SIZE
                    return True
                if x + 4 < GRID_SIZE and y + 4 < GRID_SIZE and all(board[x + i][y + i] == player for i in range(5)):
                    start_x_for_winner = (x + 1) * CELL_SIZE - CELL_SIZE / 2
                    start_y_for_winner = (y + 1) * CELL_SIZE - CELL_SIZE / 2
                    finish_x_for_winner = (x + 5) * CELL_SIZE - CELL_SIZE / 2
                    finish_y_for_winner = (y + 5) * CELL_SIZE - CELL_SIZE / 2
                    return True
                if x - 4 >= 0 and y + 4 < GRID_SIZE and all(board[x - i][y + i] == player for i in range(5)):
                    start_x_for_winner = (x + 1) * CELL_SIZE - CELL_SIZE / 2
                    start_y_for_winner = (y + 1) * CELL_SIZE - CELL_SIZE / 2
                    finish_x_for_winner = (x - 5) * CELL_SIZE - CELL_SIZE / 2
                    finish_y_for_winner = (y + 5) * CELL_SIZE - CELL_SIZE / 2
                    return True
    return False


def main():
    screen, font = init_game()
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_player = "X"  # Игрок
    bot_player = "O"      # Бот
    global gameover, start_x_for_winner, start_y_for_winner, finish_x_for_winner, finish_y_for_winner
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and current_player == "X" and not gameover:
                x, y = event.pos
                grid_x = x // CELL_SIZE
                grid_y = y // CELL_SIZE
                if board[grid_x][grid_y] is None:
                    board[grid_x][grid_y] = current_player
                    if check_winner(board, current_player):
                        print("Игрок победил!")
                        pygame.display.update()
                        # pygame.quit()
                        # sys.exit()
                        gameover = True
                    current_player = bot_player

        # Если ход бота
        if current_player == bot_player and not gameover:
            move = simple_bot_move(board)
            if move:
                grid_x, grid_y = move
                board[grid_x][grid_y] = current_player
                if check_winner(board, current_player):
                    print("Бот победил!")
                    # pygame.quit()
                    # sys.exit()
                    gameover = True
                current_player = "X"  # Вернуться к игроку

        screen.fill(WHITE)
        draw_grid(screen)

        # Отрисовка фишек
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if board[x][y] == "X":
                    pygame.draw.circle(screen, RED, (x * CELL_SIZE + CELL_SIZE // 2,
                                                     y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 0.5)
                elif board[x][y] == "O":
                    pygame.draw.circle(screen, BLUE, (x * CELL_SIZE + CELL_SIZE // 2,
                                                     y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 0.5)

        if draw_winner_line(screen):
            draw_winner_line(screen)
            if current_player == '0' and not gameover:
                print('Бот выиграл!')
            elif current_player == 'X' and not gameover:
                print('Игрок выиграл!')
            gameover = True

        pygame.display.flip()


if __name__ == "__main__":
    main()
