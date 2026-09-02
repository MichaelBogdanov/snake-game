import sys
from random import randint

import pygame

pygame.init()
pygame.display.set_caption("Змейка")

WIDTH = pygame.display.Info().current_w
HEIGHT = WIDTH // 16 * 9
SIZE = WIDTH // 16 // 5
FPS = 165

BACKGROUND_COLOR = (255, 255, 255)
GRID_COLOR = (235, 235, 235)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)

SCREEN = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.NOFRAME | pygame.SCALED | pygame.RESIZABLE,
)


class SnakePart:
    def __init__(self, x=0, y=0):
        self.color = SNAKE_COLOR
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
        return pygame.draw.rect(
            screen,
            self.color,
            self.rect,
            border_radius=SIZE // 4,
        )


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

        tail = self.body[0]
        other_parts = [part.rect for part in self.body[1:]]
        if not tail.moving and tail.rect.collidelist(other_parts) == -1:
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
        self.color = APPLE_COLOR

    def draw(self, screen):
        return pygame.draw.rect(
            screen,
            self.color,
            (self.x, self.y, SIZE, SIZE),
            border_radius=SIZE // 2,
        )


def quit_game():
    pygame.quit()
    sys.exit()


def handle_input(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

        if event.type != pygame.KEYDOWN:
            continue

        if event.key == pygame.K_ESCAPE:
            quit_game()
        elif event.key in (pygame.K_w, pygame.K_UP):
            if snake.head.speed_y != snake.head.speed:
                snake.new_speed_x = 0
                snake.new_speed_y = -snake.head.speed
        elif event.key in (pygame.K_s, pygame.K_DOWN):
            if snake.head.speed_y != -snake.head.speed:
                snake.new_speed_x = 0
                snake.new_speed_y = snake.head.speed
        elif event.key in (pygame.K_a, pygame.K_LEFT):
            if snake.head.speed_x != snake.head.speed:
                snake.new_speed_x = -snake.head.speed
                snake.new_speed_y = 0
        elif event.key in (pygame.K_d, pygame.K_RIGHT):
            if snake.head.speed_x != -snake.head.speed:
                snake.new_speed_x = snake.head.speed
                snake.new_speed_y = 0


def draw_grid(screen):
    screen.fill(BACKGROUND_COLOR)

    for x in range(0, WIDTH, SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))


def move_apple(apple, snake):
    while True:
        apple.x = SIZE * randint(0, WIDTH // SIZE - 1)
        apple.y = SIZE * randint(0, HEIGHT // SIZE - 1)

        if all(
            (apple.x, apple.y) != (part.rect.x, part.rect.y)
            for part in snake.body
        ):
            return


def main():
    clock = pygame.time.Clock()

    snake = Snake()
    snake.head.moving = True

    apple = Apple(SIZE, SIZE)
    safe_self_collision_cell = None

    while True:
        clock.tick(FPS)

        handle_input(snake)
        draw_grid(SCREEN)

        apple.draw(SCREEN)

        snake.update()

        if snake.head.rect.x == apple.x and snake.head.rect.y == apple.y:
            safe_self_collision_cell = snake.head.rect.topleft

            new_part = SnakePart(
                snake.head.rect.x // SIZE * SIZE,
                snake.head.rect.y // SIZE * SIZE,
            )
            snake.body.insert(0, new_part)
            snake.speeds.insert(0, (snake.head.speed_x, snake.head.speed_y))
            move_apple(apple, snake)

        if (
            snake.head.rect.x < 0
            or snake.head.rect.x >= WIDTH
            or snake.head.rect.y < 0
            or snake.head.rect.y >= HEIGHT
        ):
            quit_game()

        if (
            snake.head.rect.x % SIZE == 0
            and snake.head.rect.y % SIZE == 0
        ):
            collision_parts = snake.body[:-1]

            if safe_self_collision_cell is not None:
                collision_parts = collision_parts[1:]
                safe_self_collision_cell = None

            if (
                snake.head.rect.collidelist(
                    [part.rect for part in collision_parts]
                ) != -1
            ):
                quit_game()

        snake.draw(SCREEN)

        pygame.display.flip()


if __name__ == "__main__":
    main()