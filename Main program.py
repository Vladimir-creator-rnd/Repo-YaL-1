import random
import pygame
import sys

# ----------------------------------------------------------------------------------------------------------------------
# Настройка Pygame
pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
AQUA = (0, 255, 255)
ORANGE = (255, 167, 29)
# ----------------------------------------------------------------------------------------------------------------------

WIDTH, HEIGHT = 16 * 33, 600
GRID_SIZE = 15
CELL_SIZE = 33
gameover = False
start_x_for_winner = 0
start_y_for_winner = 0
finish_x_for_winner = 0
finish_y_for_winner = 0

first_player_x = []
first_player_y = []
bot_x = []
bot_y = []
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Гомоку")
screen.fill(WHITE)
font = pygame.font.Font(None, 40)
bg = pygame.image.load("bg.png")
return_arrow = pygame.image.load("return_arrow.png")


# ----------------------------------------------------------------------------------------------------------------------


def init_game():
    pygame.init()
    return pygame.display.set_mode((WIDTH, HEIGHT)), pygame.font.Font(None, 36)


# Функция для отрисовки сетки
def draw_grid(screen):
    for x in range(GRID_SIZE + 2):
        pygame.draw.line(screen, BLACK, (x * CELL_SIZE, 77), (x * CELL_SIZE, HEIGHT))  # Vertical
        pygame.draw.line(screen, BLACK, (0, (x * CELL_SIZE) + 77), (WIDTH, (x * CELL_SIZE) + 77))


def draw_winner_line(screen):
    if start_x_for_winner != 0 or start_y_for_winner != 0 or finish_x_for_winner != 0 or finish_y_for_winner != 0:
        pygame.draw.line(screen, BLACK,
                         (int(start_x_for_winner) + 0.5 * CELL_SIZE, int(start_y_for_winner) + 3 * CELL_SIZE),
                         (int(finish_x_for_winner) + 0.5 * CELL_SIZE, int(finish_y_for_winner) + 3 * CELL_SIZE), 10)
        return True


# Функция для проверки победителя
def check_winner(board, player):
    global start_x_for_winner, start_y_for_winner, finish_x_for_winner, finish_y_for_winner
    # Проверка горизонталей, вертикалей и диагоналей
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if board[x][y] == player:
                if x + 4 < GRID_SIZE and all(board[x + i][y] == player for i in range(5)):
                    start_x_for_winner = (x + 1) * CELL_SIZE - CELL_SIZE / 2
                    start_y_for_winner = (y + 1) * CELL_SIZE - CELL_SIZE / 2
                    finish_x_for_winner = (x + 5) * CELL_SIZE - CELL_SIZE / 2
                    finish_y_for_winner = (y + 1) * CELL_SIZE - CELL_SIZE / 2
                    return True
                if y + 4 < GRID_SIZE and all(board[x][y + i] == player for i in range(5)):
                    start_x_for_winner = (x + 1) * CELL_SIZE - CELL_SIZE / 2
                    start_y_for_winner = (y + 1) * CELL_SIZE - CELL_SIZE / 2
                    finish_x_for_winner = (x + 1) * CELL_SIZE - CELL_SIZE / 2
                    finish_y_for_winner = (y + 5) * CELL_SIZE - CELL_SIZE / 2
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
                    finish_x_for_winner = (x - 5) * CELL_SIZE - CELL_SIZE / 2 + CELL_SIZE * 2
                    finish_y_for_winner = (y + 5) * CELL_SIZE - CELL_SIZE / 2
                    return True
    return False


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
                    return x, y  # Блокируем горизонтально
                # Проверяем вертикально
                if (x + 2 < GRID_SIZE and
                        board[x + 1][y] == "X" and
                        board[x + 2][y] == "X"):
                    return x, y  # Блокируем вертикально
                # Проверяем диагонали
                if (x + 2 < GRID_SIZE and y + 2 < GRID_SIZE and
                        board[x + 1][y + 1] == "X" and
                        board[x + 2][y + 2] == "X"):
                    return x, y  # Блокируем диагональ \
                if (x + 2 < GRID_SIZE and y - 2 >= 0 and
                        board[x + 1][y - 1] == "X" and
                        board[x + 2][y - 2] == "X"):
                    return x, y  # Блокируем диагональ /

    x = random.randint(0, 14)
    y = random.randint(0, 14)
    if board[x][y] is None:
        return x, y  # Возвращаем первую найденную пустую клетку

    return None  # Если нет доступных ходов


def get_available_moves(board):
    return [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) if board[x][y] is None]


# ----------------------------------------------------------------------------------------------------------------------


def start_screen():
    screen.blit(bg, (0, 0))
    while True:
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and (401 > x > 99) and (221 > y > 149):
                choose_mode()
            elif event.type == pygame.MOUSEBUTTONDOWN and (401 > x > 99) and (341 > y > 269):
                print('Custom')
            elif event.type == pygame.MOUSEBUTTONDOWN and (401 > x > 99) and (461 > y > 389):
                print('Statistics')
            # print("Mouse position: ({}, {})".format(x, y))
            # Если не комментировать предыдущую строку, в консоль будут выводиться координаты мыши при каждом event
        hello = font.render(f"Лучший на свете", True, BLACK)
        hello1 = font.render(f'"ГОМОКУ"!', True, BLACK)
        screen.blit(hello, (140, 30))
        screen.blit(hello1, (175, 60))
        pygame.draw.rect(screen, BLACK, pygame.Rect(100, 150, 300, 70))
        play = font.render(f"Играть", True, WHITE)
        screen.blit(play, (206, 172))
        pygame.draw.rect(screen, BLACK, pygame.Rect(100, 270, 300, 70))
        custom = font.render(f"Кастомизация", True, WHITE)
        screen.blit(custom, (153, 292))
        pygame.draw.rect(screen, BLACK, pygame.Rect(100, 390, 300, 70))
        statistic = font.render(f"Статистика", True, WHITE)
        screen.blit(statistic, (178, 412))
        pygame.display.flip()


def choose_mode():
    global gameover, start_x_for_winner, start_y_for_winner, finish_x_for_winner, finish_y_for_winner
    screen.blit(bg, (0, 0))
    while True:
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and (401 > x > 99) and (281 > y > 199):
                start_x_for_winner, start_y_for_winner = 0, 0
                finish_x_for_winner, finish_y_for_winner = 0, 0
                gameover = False
                vs_bot()
            elif event.type == pygame.MOUSEBUTTONDOWN and (401 > x > 99) and (401 > y > 319):
                start_x_for_winner, start_y_for_winner = 0, 0
                finish_x_for_winner, finish_y_for_winner = 0, 0
                gameover = False
                one_by_one()
            elif event.type == pygame.MOUSEBUTTONDOWN and (51 > x > 9) and (36 > y > 4):
                start_screen()
            # print("Mouse position: ({}, {})".format(x, y))
            # Если не комментировать предыдущую строку, в консоль будут выводиться координаты мыши при каждом event
        hello = font.render(f"Выберите режим:", True, BLACK)
        screen.blit(hello, (130, 40))
        pygame.draw.rect(screen, BLACK, pygame.Rect(100, 200, 300, 80))
        with_bot = font.render(f"С компьютером", True, WHITE)
        screen.blit(with_bot, (140, 227))
        pygame.draw.rect(screen, BLACK, pygame.Rect(100, 320, 300, 80))
        custom = font.render(f"1 на 1", True, WHITE)
        screen.blit(custom, (215, 347))
        pygame.draw.line(screen, BLACK, (10, 20), (50, 20), 5)
        pygame.draw.line(screen, BLACK, (10, 20), (30, 5), 5)
        pygame.draw.line(screen, BLACK, (10, 20), (30, 35), 5)
        pygame.display.flip()


def one_by_one():
    global gameover
    screen, font = init_game()
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_player = "X"

    while True:
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and (51 > x > 9) and (36 > y > 4):
                choose_mode()
            elif event.type == pygame.MOUSEBUTTONDOWN and not gameover and 0 <= x <= 500 and 100 <= y <= 600:
                x, y = event.pos
                grid_x = int((x - 16.5) // CELL_SIZE)
                grid_y = int(y // CELL_SIZE - 3)
                if board[grid_x][grid_y] is None:
                    board[grid_x][grid_y] = current_player
                    if check_winner(board, current_player):
                        pygame.display.update()
                        # pygame.quit()
                        # sys.exit()
                    current_player = "O" if current_player == "X" else "X"

        screen.blit(bg, (0, 0))
        draw_grid(screen)
        pygame.draw.line(screen, BLACK, (10, 20), (50, 20), 5)
        pygame.draw.line(screen, BLACK, (10, 20), (30, 5), 5)
        pygame.draw.line(screen, BLACK, (10, 20), (30, 35), 5)
        screen.blit(return_arrow, (100, 0))

        # Отрисовка фишек
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if board[x][y] == "X":
                    pygame.draw.circle(screen, RED, (x * CELL_SIZE + CELL_SIZE,
                                                     y * CELL_SIZE + CELL_SIZE // 2 + 3 * CELL_SIZE),
                                       CELL_SIZE // 2 - 0.5)
                elif board[x][y] == "O":
                    pygame.draw.circle(screen, BLUE, (x * CELL_SIZE + CELL_SIZE,
                                                      y * CELL_SIZE + CELL_SIZE // 2 + 3 * CELL_SIZE),
                                       CELL_SIZE // 2 - 0.5)

        if draw_winner_line(screen) and not gameover:
            draw_winner_line(screen)
            if current_player == 'O':
                print('Игрок X выиграл!')
            elif current_player == 'X':
                print('Игрок O выиграл!')
            gameover = True
        pygame.display.flip()


def vs_bot():
    screen, font = init_game()
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_player = "X"  # Игрок
    bot_player = "O"  # Бот
    global gameover, start_x_for_winner, start_y_for_winner, finish_x_for_winner, finish_y_for_winner
    while True:
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and (51 > x > 9) and (36 > y > 4):
                choose_mode()
            elif (event.type == pygame.MOUSEBUTTONDOWN and current_player == "X" and not gameover and 0 <= x <= 500
                  and 100 <= y <= 600):
                # x, y = event.pos
                grid_x = int((x - 16.5) // CELL_SIZE)
                grid_y = int(y // CELL_SIZE - 3)
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

        screen.blit(bg, (0, 0))
        draw_grid(screen)
        pygame.draw.line(screen, BLACK, (10, 20), (50, 20), 5)
        pygame.draw.line(screen, BLACK, (10, 20), (30, 5), 5)
        pygame.draw.line(screen, BLACK, (10, 20), (30, 35), 5)
        screen.blit(return_arrow, (100, 0))

        # Отрисовка фишек
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if board[x][y] == "X":
                    pygame.draw.circle(screen, RED, (x * CELL_SIZE + CELL_SIZE,
                                                     y * CELL_SIZE + CELL_SIZE // 2 + 3 * CELL_SIZE),
                                       CELL_SIZE // 2 - 0.5)
                elif board[x][y] == "O":
                    pygame.draw.circle(screen, BLUE, (x * CELL_SIZE + CELL_SIZE,
                                                      y * CELL_SIZE + CELL_SIZE // 2 + 3 * CELL_SIZE),
                                       CELL_SIZE // 2 - 0.5)

        if draw_winner_line(screen):
            draw_winner_line(screen)
            if current_player == '0' and not gameover:
                print('Бот выиграл!')
            elif current_player == 'X' and not gameover:
                print('Игрок выиграл!')
            gameover = True

        pygame.display.flip()


if __name__ == "__main__":
    start_screen()
