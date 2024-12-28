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
            elif event.type == pygame.MOUSEBUTTONDOWN and (401 > x > 99) and (221 > y > 149):
                print('Play')
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


if __name__ == "__main__":
    main()
