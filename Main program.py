import pygame
import sys

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


WIDTH, HEIGHT = 500, 500
GRID_SIZE = 15
CELL_SIZE = WIDTH // GRID_SIZE
gameover = False
start_x_for_winner = 0
start_y_for_winner = 0
finish_x_for_winner = 0
finish_y_for_winner = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Гомоку")
screen.fill(WHITE)
font = pygame.font.Font(None, 40)
bg = pygame.image.load("bg.jpg")


def init_game():
    pygame.init()
    return pygame.display.set_mode((WIDTH, HEIGHT)), pygame.font.Font(None, 36)


# Функция для отрисовки сетки
def draw_grid(screen):
    for x in range(GRID_SIZE + 1):
        pygame.draw.line(screen, BLACK, (x * CELL_SIZE - 20, 0), (x * CELL_SIZE - 20, HEIGHT))
        pygame.draw.line(screen, BLACK, (0, x * CELL_SIZE - 20), (WIDTH, x * CELL_SIZE - 20))


def draw_winner_line(screen):
    if start_x_for_winner != 0 or start_y_for_winner != 0 or finish_x_for_winner != 0 or finish_y_for_winner != 0:
        pygame.draw.line(screen, BLACK, (int(start_x_for_winner), int(start_y_for_winner)),
                         (int(finish_x_for_winner), int(finish_y_for_winner)), 10)
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
    screen.blit(bg, (0, 0))
    while True:
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and (401 > x > 99) and (281 > y > 199):
                start_screen()
            elif event.type == pygame.MOUSEBUTTONDOWN and (401 > x > 99) and (401 > y > 319):
                one_by_one()
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
        pygame.display.flip()


def one_by_one():
    global gameover
    screen, font = init_game()
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_player = "X"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not gameover:
                x, y = event.pos
                grid_x = x // CELL_SIZE
                grid_y = y // CELL_SIZE
                if board[grid_x][grid_y] is None:
                    board[grid_x][grid_y] = current_player
                    if check_winner(board, current_player):
                        print(f"Игрок {current_player} победил!")
                        # pygame.quit()
                        # sys.exit()
                        game_over = True
                    current_player = "O" if current_player == "X" else "X"

        screen.fill(WHITE)
        draw_grid(screen)

        # Отрисовка фишек
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if board[x][y] == "X":
                    pygame.draw.circle(screen, RED, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2),
                                       CELL_SIZE // 2 - 0.1)
                elif board[x][y] == "O":
                    pygame.draw.circle(screen, BLUE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2),
                                       CELL_SIZE // 2 - 0.1)

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
