import pygame
import sys

# Константы
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 15
CELL_SIZE = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
game_over = False


# Функция для инициализации Pygame
def init_game():
    pygame.init()
    return pygame.display.set_mode((WIDTH, HEIGHT)), pygame.font.Font(None, 36)


# Функция для отрисовки сетки
def draw_grid(screen):
    for x in range(GRID_SIZE + 1):
        pygame.draw.line(screen, BLACK, (x * CELL_SIZE - 20, 0), (x * CELL_SIZE - 20, HEIGHT))
        pygame.draw.line(screen, BLACK, (0, x * CELL_SIZE - 20), (WIDTH, x * CELL_SIZE - 20))


# Функция для проверки победителя
def check_winner(board, player):
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


# Главная функция
def main():
    global game_over
    screen, font = init_game()
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    current_player = "X"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
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
                                       CELL_SIZE // 2 - 5)
                elif board[x][y] == "O":
                    pygame.draw.circle(screen, BLUE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2),
                                       CELL_SIZE // 2 - 5)

        pygame.display.flip()


if __name__ == "__main__":
    main()