import os
import sys
import pygame


os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH = 1280
HEIGHT = WIDTH // 16 * 9
SIZE = WIDTH // 16 // 5

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60


class SnakePart:
    def __init__(self, x=0, y=0):
        self.color = (0, 255, 0)
        self.rect = pygame.Rect(x, y, SIZE, SIZE)

        self.speed = 1
        self.speed_x = self.speed
        self.speed_y = 0
        self.moving = False

    def update(self):
        if self.moving:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

    def draw(self, screen):
        return pygame.draw.rect(screen, self.color, self.rect, border_radius=SIZE // 4)


class Snake:
    def __init__(self):
        self.body = [SnakePart()]
        self.speeds = [(self.body[-1].speed_x, self.body[-1].speed_y)]

        self.new_speed_x = self.body[-1].speed
        self.new_speed_y = 0

    def update(self):
        for part in self.body:
            part.update()

        if self.head.rect.x % SIZE == 0 and self.head.rect.y % SIZE == 0:
            self.speeds = self.speeds[1:] + [(self.new_speed_x, self.new_speed_y)]

            for i in range(len(self.body))[::-1]:
                self.body[i].speed_x, self.body[i].speed_y = self.speeds[i]

        if not self.body[0].moving and self.body[0].rect.collidelist(list(map(lambda x: x.rect, self.body[1:]))) == -1:
            self.body[0].moving = True
            self.body[0].speed_x, self.body[0].speed_y = self.speeds[0]

    def draw(self, screen):
        for part in self.body:
            part.draw(screen)

    @property
    def head(self):
        return self.body[-1]


class Apple:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (255, 0, 0)

    def draw(self, screen):
        return pygame.draw.rect(screen, self.color, (self.x, self.y, SIZE, SIZE), border_radius=SIZE // 2)


def main():
    clock = pygame.time.Clock()
    
    snake = Snake()
    snake.head.moving = True

    apple = Apple(80, 80)

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
                    snake.new_speed_y = -snake.head.speed
                    snake.new_speed_x = 0
                elif event.key == pygame.K_s:
                    snake.new_speed_y = snake.head.speed
                    snake.new_speed_x = 0
                elif event.key == pygame.K_a:
                    snake.new_speed_x = -snake.head.speed
                    snake.new_speed_y = 0
                elif event.key == pygame.K_d:
                    snake.new_speed_x = snake.head.speed
                    snake.new_speed_y = 0

        apple.draw(SCREEN)

        snake.update()

        if snake.head.rect.x == apple.x and snake.head.rect.y == apple.y:
            snake.body.insert(0, SnakePart(snake.head.rect.x // SIZE * SIZE, snake.head.rect.y // SIZE * SIZE))
            snake.speeds.insert(0, (snake.head.speed_x, snake.head.speed_y))

        snake.draw(SCREEN)

        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Змейка")
    main()