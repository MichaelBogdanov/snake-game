import os
import sys
import pygame


os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH = 1280
HEIGHT = WIDTH // 16 * 9
SIZE = WIDTH // 16 // 5

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 240


class Snake:
    def __init__(self):
        self.x, self.y = 0, 0
        self.speed = 1
        self.color = (0, 255, 0)
        self.speed_x = self.speed
        self.speed_y = 0
        self.new_speed_x = self.speed_x
        self.new_speed_y = self.speed_y

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self, screen):
        return pygame.draw.rect(screen, self.color, (self.x, self.y, SIZE, SIZE))


def main():
    clock = pygame.time.Clock()
    
    snake = Snake()

    while True:
        clock.tick(FPS)

        SCREEN.fill((255, 255, 255))

        for i in range(0, WIDTH, SIZE):
            pygame.draw.line(SCREEN, (235, 235, 235), (i, 0), (i, HEIGHT))
        for i in range(0, HEIGHT, SIZE):
            pygame.draw.line(SCREEN, (235, 235, 235), (0, i), (WIDTH, i))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_w:
                    snake.new_speed_y = -snake.speed
                    snake.new_speed_x = 0
                elif event.key == pygame.K_s:
                    snake.new_speed_y = snake.speed
                    snake.new_speed_x = 0
                elif event.key == pygame.K_a:
                    snake.new_speed_x = -snake.speed
                    snake.new_speed_y = 0
                elif event.key == pygame.K_d:
                    snake.new_speed_x = snake.speed
                    snake.new_speed_y = 0

        snake.update()
        if snake.x % SIZE == 0 and snake.y % SIZE == 0:
            snake.speed_x = snake.new_speed_x
            snake.speed_y = snake.new_speed_y
        snake.draw(SCREEN)

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Змейка")
    main()