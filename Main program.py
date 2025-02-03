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
YELLOW = (255, 255, 85)
DARK_GREEN = (71, 161, 44)
player_color = WHITE
bot_color = BLACK
line_color = BLACK
# ----------------------------------------------------------------------------------------------------------------------
WIDTH, HEIGHT = 16 * 33, 600
GRID_SIZE = 15
CELL_SIZE = 33
gameover = False
start_x_for_winner = 0
start_y_for_winner = 0
finish_x_for_winner = 0
finish_y_for_winner = 0
winner = ''
first_player_x = []
first_player_y = []
bot_x = []
bot_y = []
wins = 0
defeats = 0
chips_counter = 0
with open('statistics.txt', 'r+') as file:
    counter = 0
    for i in range(4):
        if counter == 0:
            wins = int(file.readline().strip('\n'))
            counter += 1
        elif counter == 1:
            defeats = int(file.readline().strip('\n'))
            counter += 1
        elif counter == 2:
            player_color = tuple(map(int, file.readline().strip('\n').split()))
            counter += 1
        elif counter == 3:
            bot_color = tuple(map(int, file.readline().strip('\n').split()))
            counter += 1

try:
    win_rate = (100 / (wins + defeats)) * wins
except ZeroDivisionError:
    win_rate = 0
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Гомоку")
screen.fill(WHITE)
font = pygame.font.Font(None, 40)
mini_font = pygame.font.Font(None, 30)



bg = pygame.image.load("data/bg.png")
return_arrow = pygame.image.load("data/return_arrow.png")
player1 = pygame.image.load("data/player1.png")
player2 = pygame.image.load("data/player2.png")
player = pygame.image.load("data/player.png")
bot = pygame.image.load("data/bot.png")
draw = pygame.image.load("data/draw.png")


# ----------------------------------------------------------------------------------------------------------------------

# Функция инициализации игры
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
        pygame.draw.line(screen, line_color,
                         (int(start_x_for_winner) + 0.5 * CELL_SIZE, int(start_y_for_winner) + 3 * CELL_SIZE),
                         (int(finish_x_for_winner) + 0.5 * CELL_SIZE, int(finish_y_for_winner) + 3 * CELL_SIZE), 10)
        return True


# Функция для проверки победителя
def check_winner(board, player):
    global start_x_for_winner, start_y_for_winner, finish_x_for_winner, finish_y_for_winner, chips_counter, gameover
    chips_counter = 0
    # Проверка горизонталей, вертикалей и диагоналей
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if board[x][y] == player:
                chips_counter += 1
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
    if chips_counter == 225:
        gameover = True
        end_game_draw()
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
    # Проверяем, может ли игрок выиграть следующим ходом
    for x, y in available_moves:
        board[x][y] = "X"
        if check_winner_for_move(board, "X"):
            board[x][y] = None
            return x, y
        board[x][y] = None
    # Проверяем, есть ли у игрока 3 фишки, стоящих подряд
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


def redrawing_stat():  # Перерисовка окна статистики, благодаря которой работает сброс статистики
    screen.blit(bg, (0, 0))
    stat_vs_bot = font.render("Ваша статистика", True, BLACK)
    stat_vs_bot1 = font.render("игр против бота", True, BLACK)
    screen.blit(stat_vs_bot, (150, 60))
    screen.blit(stat_vs_bot1, (155, 90))
    victory = font.render("Победы", True, BLACK)
    defeat = font.render("Поражения", True, BLACK)
    winrate = font.render("Процент побед", True, BLACK)
    victory_number = font.render(str(wins), True, BLACK)
    defeat_number = font.render(str(defeats), True, BLACK)
    data_reset = font.render("Сбросить данные", True, WHITE)
    try:
        win_rate_number = font.render(str(int((100 / (wins + defeats)) * wins)) + ' %', True, BLACK)
    except ZeroDivisionError:
        win_rate_number = font.render("0 %", True, BLACK)
    # Таблица
    screen.blit(victory, (35, 188))
    screen.blit(defeat, (35, 248))
    screen.blit(winrate, (35, 308))
    screen.blit(victory_number, (equalization(len(str(wins))), 188))
    screen.blit(defeat_number, (equalization(len(str(defeats))), 248))
    screen.blit(win_rate_number, (equalization(len(str(int(win_rate))), True), 308))
    pygame.draw.line(screen, BLACK, (30, 170), (30, 350), 5)
    pygame.draw.line(screen, BLACK, (498, 170), (498, 350), 5)
    pygame.draw.line(screen, BLACK, (264, 170), (264, 350), 5)
    pygame.draw.line(screen, BLACK, (30, 170), (498, 170), 5)
    pygame.draw.line(screen, BLACK, (30, 230), (498, 230), 5)
    pygame.draw.line(screen, BLACK, (30, 290), (498, 290), 5)
    pygame.draw.line(screen, BLACK, (30, 350), (498, 350), 5)
    # Стрелка
    pygame.draw.line(screen, BLACK, (10, 20), (50, 20), 5)
    pygame.draw.line(screen, BLACK, (10, 20), (30, 5), 5)
    pygame.draw.line(screen, BLACK, (10, 20), (30, 35), 5)
    # Сброс данных
    pygame.draw.rect(screen, (204, 44, 31), pygame.Rect(130, 400, 268, 60))
    # pygame.draw.rect(screen, BLACK, pygame.Rect(130, 400, 268, 60), width=5)
    screen.blit(data_reset, (143, 417))
    pygame.display.flip()


def equalization(arg, arg2=False):
    if arg == 1 and not arg2:
        return 373
    elif arg == 2 and not arg2:
        return 365
    elif arg == 3 and not arg2:
        return 356
    elif arg == 1 and arg2:
        return 361
    elif arg == 2 and arg2:
        return 357
    elif arg == 3 and arg2:
        return 340



def redrawing():  # Перерисовка окна кастомизации, чтобы был отображен текущий цвет
    screen.blit(bg, (0, 0))
    title1 = font.render(f"Цвет игрока 1", True, BLACK)
    title2 = font.render(f"Цвет игрока 2 (бота)", True, BLACK)
    red = mini_font.render(f"Красный", True, BLACK)
    yellow = mini_font.render(f"Жёлтый", True, BLACK)
    white = mini_font.render(f"Белый", True, BLACK)
    blue = mini_font.render(f"Синий", True, WHITE)
    green = mini_font.render(f"Зелёный", True, BLACK)
    black = mini_font.render(f"Чёрный", True, WHITE)
    screen.blit(title1, (170, 30))
    screen.blit(title2, (130, 330))
    pygame.draw.rect(screen, RED, pygame.Rect(28, 125, 120, 50))
    pygame.draw.rect(screen, YELLOW, pygame.Rect(204, 125, 120, 50))
    pygame.draw.rect(screen, WHITE, pygame.Rect(380, 125, 120, 50))
    pygame.draw.rect(screen, BLUE, pygame.Rect(28, 225, 120, 50))
    pygame.draw.rect(screen, GREEN, pygame.Rect(204, 225, 120, 50))
    pygame.draw.rect(screen, BLACK, pygame.Rect(380, 225, 120, 50))
    pygame.draw.rect(screen, RED, pygame.Rect(28, 425, 120, 50))
    pygame.draw.rect(screen, YELLOW, pygame.Rect(204, 425, 120, 50))
    pygame.draw.rect(screen, WHITE, pygame.Rect(380, 425, 120, 50))
    pygame.draw.rect(screen, BLUE, pygame.Rect(28, 525, 120, 50))
    pygame.draw.rect(screen, GREEN, pygame.Rect(204, 525, 120, 50))
    pygame.draw.rect(screen, BLACK, pygame.Rect(380, 525, 120, 50))
    pygame.draw.line(screen, BLACK, (10, 20), (50, 20), 5)
    pygame.draw.line(screen, BLACK, (10, 20), (30, 5), 5)
    pygame.draw.line(screen, BLACK, (10, 20), (30, 35), 5)
    pygame.draw.line(screen, BLACK, (0, 300), (WIDTH, 300), 5)
    screen.blit(red, (44, 142))
    screen.blit(yellow, (223, 142))
    screen.blit(white, (407, 142))
    screen.blit(blue, (56, 242))
    screen.blit(green, (220, 242))
    screen.blit(black, (400, 242))
    screen.blit(red, (44, 442))
    screen.blit(yellow, (223, 442))
    screen.blit(white, (407, 442))
    screen.blit(blue, (56, 542))
    screen.blit(green, (220, 542))
    screen.blit(black, (400, 542))
    if player_color == RED:
        pygame.draw.circle(screen, DARK_GREEN, (148, 175), 10)
    if player_color == YELLOW:
        pygame.draw.circle(screen, DARK_GREEN, (324, 175), 10)
    if player_color == WHITE:
        pygame.draw.circle(screen, DARK_GREEN, (500, 175), 10)
    if player_color == BLUE:
        pygame.draw.circle(screen, DARK_GREEN, (148, 275), 10)
    if player_color == GREEN:
        pygame.draw.circle(screen, DARK_GREEN, (324, 275), 10)
    if player_color == BLACK:
        pygame.draw.circle(screen, DARK_GREEN, (500, 275), 10)
    if bot_color == RED:
        pygame.draw.circle(screen, DARK_GREEN, (148, 475), 10)
    if bot_color == YELLOW:
        pygame.draw.circle(screen, DARK_GREEN, (324, 475), 10)
    if bot_color == WHITE:
        pygame.draw.circle(screen, DARK_GREEN, (500, 475), 10)
    if bot_color == BLUE:
        pygame.draw.circle(screen, DARK_GREEN, (148, 575), 10)
    if bot_color == GREEN:
        pygame.draw.circle(screen, DARK_GREEN, (324, 575), 10)
    if bot_color == BLACK:
        pygame.draw.circle(screen, DARK_GREEN, (500, 575), 10)
    pygame.display.flip()


def rewriting():  # Запись всех необходимых данных в файл statistics.txt
    with open('statistics.txt', 'r+') as file1:
        file1.truncate(0)
        file1.write(str(wins))
        file1.write('\n')
        file1.write(str(defeats))
        file1.write('\n')
        b = str(player_color)[1:-1].split(', ')
        d = ''
        for elem in b:
            d += elem + ' '
        file1.write(d[:-1])
        file1.write('\n')
        b = str(bot_color)[1:-1].split(', ')
        d = ''
        for elem in b:
            d += elem + ' '
        file1.write(d[:-1])


def choose_next_step():
    global gameover, winner, start_x_for_winner, start_y_for_winner, finish_x_for_winner, finish_y_for_winner
    while True:
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 41 286
            # 480 391 - верхняя кнопка
            # 41 425
            # 480 530 - нижняя кнопка
            elif event.type == pygame.MOUSEBUTTONDOWN and (41 < x < 480) and (286 < y < 391):
                if winner == 'player1' or winner == 'player2':
                    winner = ''
                    start_x_for_winner, start_y_for_winner, finish_x_for_winner, finish_y_for_winner = 0, 0, 0, 0
                    gameover = False
                    one_by_one()
                elif winner == 'bot' or winner == 'player':
                    winner = ''
                    start_x_for_winner, start_y_for_winner, finish_x_for_winner, finish_y_for_winner = 0, 0, 0, 0
                    gameover = False
                    vs_bot()
            elif event.type == pygame.MOUSEBUTTONDOWN and (41 < x < 480) and (425 < y < 530):
                start_screen()


def end_game(picture):
    clock = pygame.time.Clock()
    is_running = True
    current_position = -528
    speed = 8
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if current_position < 0:
            current_position += speed
        else:
            choose_next_step()
        screen.blit(picture, (current_position, 0))
        pygame.display.flip()
        clock.tick(60)


def end_game_draw():
    clock = pygame.time.Clock()
    is_running = True
    current_position = -528
    speed = 8
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if current_position < 0:
            current_position += speed
        else:
            choose_next_step()
        screen.blit(draw, (current_position, 0))
        pygame.display.flip()
        clock.tick(60)



def start_screen():  # Стартовый экран
    screen.blit(bg, (0, 0))
    while True:
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                rewriting()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and (401 > x > 99) and (221 > y > 149):
                choose_mode()
            elif event.type == pygame.MOUSEBUTTONDOWN and (401 > x > 99) and (341 > y > 269):
                customization()
            elif event.type == pygame.MOUSEBUTTONDOWN and (401 > x > 99) and (461 > y > 389):
                statistics()
            # print("Mouse position: ({}, {})".format(x, y))
            # Если не комментировать предыдущую строку, в консоль будут выводиться координаты мыши при каждом event
        hello = font.render(f"Лучший на свете", True, BLACK)
        hello1 = font.render(f'"ГОМОКУ"!', True, BLACK)
        screen.blit(hello, (154, 30))
        screen.blit(hello1, (189, 60))
        pygame.draw.rect(screen, BLACK, pygame.Rect(114, 150, 300, 70))
        play = font.render(f"Играть", True, WHITE)
        screen.blit(play, (220, 172))
        pygame.draw.rect(screen, BLACK, pygame.Rect(114, 270, 300, 70))
        custom = font.render(f"Кастомизация", True, WHITE)
        screen.blit(custom, (167, 292))
        pygame.draw.rect(screen, BLACK, pygame.Rect(114, 390, 300, 70))
        statistic = font.render(f"Статистика", True, WHITE)
        screen.blit(statistic, (192, 412))
        pygame.display.flip()


def choose_mode():  # Выбор режима игры
    global gameover, start_x_for_winner, start_y_for_winner, finish_x_for_winner, finish_y_for_winner
    screen.blit(bg, (0, 0))
    while True:
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                rewriting()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and (401 > x > 99) and (281 > y > 199):
                if player_color != bot_color:
                    start_x_for_winner, start_y_for_winner = 0, 0
                    finish_x_for_winner, finish_y_for_winner = 0, 0
                    gameover = False
                    vs_bot()
            elif event.type == pygame.MOUSEBUTTONDOWN and (401 > x > 99) and (401 > y > 319):
                if player_color != bot_color:
                    start_x_for_winner, start_y_for_winner = 0, 0
                    finish_x_for_winner, finish_y_for_winner = 0, 0
                    gameover = False
                    one_by_one()
            elif event.type == pygame.MOUSEBUTTONDOWN and (51 > x > 9) and (36 > y > 4):
                start_screen()
            # print("Mouse position: ({}, {})".format(x, y))
            # Если не комментировать предыдущую строку, в консоль будут выводиться координаты мыши при каждом event
        hello = font.render(f"Выберите режим:", True, BLACK)
        screen.blit(hello, (144, 40))
        pygame.draw.rect(screen, BLACK, pygame.Rect(114, 200, 300, 80))
        with_bot = font.render(f"С компьютером", True, WHITE)
        screen.blit(with_bot, (154, 227))
        pygame.draw.rect(screen, BLACK, pygame.Rect(114, 320, 300, 80))
        player_vs_player = font.render(f"1 на 1", True, WHITE)
        screen.blit(player_vs_player, (229, 347))
        if player_color == bot_color:
            warning1 = font.render(f'Выбраны одинаковые цвета фишек!', True, RED)
            warning2 = mini_font.render(f'Вернитесь в меню "Кастомизация" и смените их!', True, RED)
            screen.blit(warning1, (15, 500))
            screen.blit(warning2, (15, 550))
        pygame.draw.line(screen, BLACK, (10, 20), (50, 20), 5)
        pygame.draw.line(screen, BLACK, (10, 20), (30, 5), 5)
        pygame.draw.line(screen, BLACK, (10, 20), (30, 35), 5)
        pygame.display.flip()


def customization():  # Окно кастомизации
    global player_color, bot_color
    screen.blit(bg, (0, 0))
    while True:
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                rewriting()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and (51 > x > 9) and (36 > y > 4):
                start_screen()
            elif event.type == pygame.MOUSEBUTTONDOWN and (28 <= x <= 148) and (125 <= y <= 175):
                player_color = RED
            elif event.type == pygame.MOUSEBUTTONDOWN and (204 <= x <= 324) and (125 <= y <= 175):
                player_color = YELLOW
            elif event.type == pygame.MOUSEBUTTONDOWN and (380 <= x <= 500) and (125 <= y <= 175):
                player_color = WHITE
            elif event.type == pygame.MOUSEBUTTONDOWN and (28 <= x <= 148) and (225 <= y <= 275):
                player_color = BLUE
            elif event.type == pygame.MOUSEBUTTONDOWN and (204 <= x <= 324) and (225 <= y <= 275):
                player_color = GREEN
            elif event.type == pygame.MOUSEBUTTONDOWN and (380 <= x <= 500) and (225 <= y <= 275):
                player_color = BLACK
            elif event.type == pygame.MOUSEBUTTONDOWN and (28 <= x <= 148) and (425 <= y <= 475):
                bot_color = RED
            elif event.type == pygame.MOUSEBUTTONDOWN and (204 <= x <= 324) and (425 <= y <= 475):
                bot_color = YELLOW
            elif event.type == pygame.MOUSEBUTTONDOWN and (380 <= x <= 500) and (425 <= y <= 475):
                bot_color = WHITE
            elif event.type == pygame.MOUSEBUTTONDOWN and (28 <= x <= 148) and (525 <= y <= 575):
                bot_color = BLUE
            elif event.type == pygame.MOUSEBUTTONDOWN and (204 <= x <= 324) and (525 <= y <= 575):
                bot_color = GREEN
            elif event.type == pygame.MOUSEBUTTONDOWN and (380 <= x <= 500) and (525 <= y <= 575):
                bot_color = BLACK
        redrawing()


def statistics():  # Окно статистики
    global wins, defeats, win_rate
    screen.blit(bg, (0, 0))
    while True:
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                rewriting()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and (51 > x > 9) and (36 > y > 4):
                start_screen()
            elif event.type == pygame.MOUSEBUTTONDOWN and (130 < x < 398) and (400 < y < 460):
                wins = 0
                defeats = 0
        redrawing_stat()


def one_by_one():
    global gameover
    screen, font = init_game()
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_player = "X"
    global winner
    while True:
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                rewriting()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and (51 > x > 9) and (36 > y > 4):
                choose_mode()
            if event.type == pygame.MOUSEBUTTONDOWN and (147 > x > 99) and (47 > y) and not gameover:
                if len(first_player_x) != 0:
                    delete_player_x = first_player_x[-1]
                    delete_player_y = first_player_y[-1]
                    board[delete_player_x][delete_player_y] = None
                    del first_player_x[-1]
                    del first_player_y[-1]
            elif event.type == pygame.MOUSEBUTTONDOWN and not gameover and 0 <= x <= 500 and 100 <= y <= 600:
                x, y = event.pos
                grid_x = int((x - 16.5) // CELL_SIZE)
                grid_y = int(y // CELL_SIZE - 3)
                if board[grid_x][grid_y] is None:
                    first_player_x.append(grid_x)
                    first_player_y.append(grid_y)
                    board[grid_x][grid_y] = current_player
                    if check_winner(board, current_player):
                        if current_player == '0':
                            winner = 'player2'
                        elif current_player == 'X':
                            winner = 'player1'
                        pygame.display.update()
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
                    pygame.draw.circle(screen, player_color, (x * CELL_SIZE + CELL_SIZE,
                                                              y * CELL_SIZE + CELL_SIZE // 2 + 3 * CELL_SIZE),
                                       CELL_SIZE // 2 - 0.5)
                elif board[x][y] == "O":
                    pygame.draw.circle(screen, bot_color, (x * CELL_SIZE + CELL_SIZE,
                                                           y * CELL_SIZE + CELL_SIZE // 2 + 3 * CELL_SIZE),
                                       CELL_SIZE // 2 - 0.5)

        if draw_winner_line(screen) and not gameover:
            draw_winner_line(screen)
            if winner == 'player1':
                end_game(player1)
            else:
                end_game(player2)
            gameover = True
        pygame.display.flip()


def vs_bot():
    screen, font = init_game()
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_player = "X"  # Игрок
    bot_player = "O"  # Бот
    global gameover, start_x_for_winner, start_y_for_winner, finish_x_for_winner, finish_y_for_winner, first_player_x, \
        first_player_y, bot_x, bot_y, wins, defeats, winner
    while True:
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rewriting()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and (51 > x > 9) and (36 > y > 4):
                choose_mode()
            if event.type == pygame.MOUSEBUTTONDOWN and (147 > x > 99) and (47 > y) and not gameover:
                if len(first_player_x) != 0:
                    delete_player_x = first_player_x[-1]
                    delete_player_y = first_player_y[-1]
                    delete_bot_x = bot_x[-1]
                    delete_bot_y = bot_y[-1]
                    board[delete_player_x][delete_player_y] = None
                    board[delete_bot_x][delete_bot_y] = None
                    del first_player_x[-1]
                    del first_player_y[-1]
                    del bot_x[-1]
                    del bot_y[-1]
            elif (event.type == pygame.MOUSEBUTTONDOWN and current_player == "X" and not gameover and 0 <= x <= 500
                  and 100 <= y <= 600):
                # x, y = event.pos
                grid_x = int((x - 16.5) // CELL_SIZE)
                grid_y = int(y // CELL_SIZE - 3)
                if board[grid_x][grid_y] is None:
                    board[grid_x][grid_y] = current_player
                    first_player_x.append(grid_x)
                    first_player_y.append(grid_y)
                    if check_winner(board, current_player):
                        print("Игрок победил!")
                        wins += 1
                        winner = 'player'
                        pygame.display.update()
                        gameover = True
                        first_player_x = []
                        first_player_y = []
                        bot_x = []
                        bot_y = []
                    current_player = bot_player

        # Если ход бота
        if current_player == bot_player and not gameover:
            move = simple_bot_move(board)
            if move:
                grid_x, grid_y = move
                board[grid_x][grid_y] = current_player
                bot_x.append(grid_x)
                bot_y.append(grid_y)
                if check_winner(board, current_player):
                    print("Бот победил!")
                    defeats += 1
                    winner = 'bot'
                    gameover = True
                    first_player_x, first_player_y = [], []
                    bot_x, bot_y = [], []
                current_player = "X"

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
                    pygame.draw.circle(screen, player_color, (x * CELL_SIZE + CELL_SIZE,
                                                              y * CELL_SIZE + CELL_SIZE // 2 + 3 * CELL_SIZE),
                                       CELL_SIZE // 2 - 0.5)
                elif board[x][y] == "O":
                    pygame.draw.circle(screen, bot_color, (x * CELL_SIZE + CELL_SIZE,
                                                           y * CELL_SIZE + CELL_SIZE // 2 + 3 * CELL_SIZE),
                                       CELL_SIZE // 2 - 0.5)

        if draw_winner_line(screen):
            draw_winner_line(screen)
            gameover = True
            if winner == 'player':
                end_game(player)
            else:
                end_game(bot)

        pygame.display.flip()


if __name__ == "__main__":
    start_screen()
