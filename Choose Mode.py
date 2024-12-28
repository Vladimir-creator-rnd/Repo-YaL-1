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

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Гомоку")
screen.fill(WHITE)
font = pygame.font.Font(None, 40)
bg = pygame.image.load("bg.jpg")


def main():
    screen.blit(bg, (0, 0))
    while True:
        for event in pygame.event.get():
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and (401 > x > 99) and (281 > y > 199):
                print('With bot')
            elif event.type == pygame.MOUSEBUTTONDOWN and (401 > x > 99) and (401 > y > 319):
                print('1 vs 1')
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


if __name__ == "__main__":
    main()
