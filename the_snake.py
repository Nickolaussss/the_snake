"""Модуль: the_snake."""

from random import randint, choice

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Центральная позиция:
CENTRAL_POSITION = (GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR = (0, 255, 0)

# Цвет змейки:
SNAKE_COLOR = (250, 128, 114)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption("Супер Змейка")

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Отрисовывает игровое поле."""

    def __init__(self, body_color=None, position=CENTRAL_POSITION):
        """Инициализирует объект на игровом поле."""
        self.position = position
        self.body_color = body_color

    def draw(self) -> str:
        """Шаблон для подклассов."""
        raise NotImplementedError('Метод draw ещё не реализован')

    def draw_cell(self, position, body_color):
        """Отрисовывает ячейки"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Яблоко."""

    def __init__(self, body_color=APPLE_COLOR):
        """Инициализирует яблоко на игровом поле."""
        super().__init__(body_color)

    def randomize_position(self, positions=CENTRAL_POSITION):
        """Генерируем новое яблоко."""
        while True:
            new_apple = (
                randint(0, GRID_WIDTH - 1) * (GRID_SIZE),
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if new_apple not in positions:
                break
        self.position = new_apple

    def draw(self):
        """Рисуем яблоко на поле."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Змейка."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализирует змейку на игровом поле."""
        super().__init__(body_color)
        self.reset()

    def draw(self):
        """Рисуем змейку на поле."""
        for position in self.positions:
            self.draw_cell(position, self.body_color)

    def move(self):
        """Передвижение змейки."""
        head_x, head_y = self.get_head_position()
        coordinate_x, coordinate_y = self.direction
        step_x = coordinate_x * GRID_SIZE
        step_y = coordinate_y * GRID_SIZE
        new_head = (
            (head_x + step_x) % SCREEN_WIDTH,
            (head_y + step_y) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        self.delete_last()

    def get_head_position(self) -> tuple:
        """Берем координаты головы змейки."""
        return self.positions[0]

    def delete_last(self):
        """Избавление от ненужных элементов змеи."""
        if len(self.positions) > self.length:
            self.positions.pop()

    def update_direction(self):
        """Обновляем направление змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Возвращение змейки в исходное состояние."""
        self.direction = choice([UP, RIGHT, DOWN, LEFT])
        self.length = 1
        self.next_direction = None
        self.positions = [self.position]


def handle_keys(game_object):
    """Регулировка направления движения змейки и функция выхода."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Main - есть Main."""
    pg.init()

    snake = Snake()
    apple = Apple()

    apple.randomize_position()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            apple.randomize_position(snake.position)
            snake.length += 1

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.position)

        apple.draw()
        snake.draw()

        pg.display.update()

        screen.fill(BOARD_BACKGROUND_COLOR)


if __name__ == "__main__":
    main()
