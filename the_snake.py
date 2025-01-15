from random import randint

import pygame as pg

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки
SPEED = 20

# Настройка игрового окна
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


class GameObject:
    """Родительский класс."""

    def __init__(self, position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                 body_color=None):
        """Инициализируем объект."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Рисуем объект на экране."""
        raise NotImplementedError(f"{self.__class__.__name__}")


class Apple(GameObject):
    """Обозначаем яблоко."""

    def __init__(self, body_color=APPLE_COLOR):
        """Инициализируем яблоко и определяем местоположение яблока."""
        super().__init__(body_color=body_color)
        self.randomize_position()

    def randomize_position(self, snake_positions=None):
        """Определяем местоположение яблока случайным образом."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        if snake_positions and self.position in snake_positions:
            self.randomize_position(snake_positions)

    def draw(self):
        """Рисуем яблоко на экране."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Обозначаем змейку в игре."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализируем змейку по умолчанию."""
        super().__init__(body_color=body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.last = None

    def update_direction(self, new_direction):
        """Обновляет направление движения змеи на основе данных."""
        if new_direction and (
            (new_direction == UP and self.direction != DOWN) or
            (new_direction == DOWN and self.direction != UP) or
            (new_direction == LEFT and self.direction != RIGHT) or
            (new_direction == RIGHT and self.direction != LEFT)
        ):
            self.direction = new_direction

    def move(self):
        """Двигаем змейку в текущем направлении."""
        head = self.get_head_position()
        x, y = self.direction
        new_head = ((head[0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
                    (head[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)

        self.last = (self.positions[-1] if len(self.positions) > self.length
                     else None)
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Рисуем змейку на экране."""
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращаем позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасываем змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.last = None


def handle_keys(snake):
    """Обрабатываем нажатия клавиш, чтобы изменить движения змейки."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()
            elif event.key == pg.K_UP:
                snake.update_direction(UP)
            elif event.key == pg.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pg.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pg.K_RIGHT:
                snake.update_direction(RIGHT)


def main():
    """Основная функция для запуска игры."""
    pg.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        snake.move()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
