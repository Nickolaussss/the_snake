"""Модуль: the_snake."""

from random import choice, randrange

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]

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
pg.display.set_caption('Супер змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Отрисовывает игровое поле."""

    def __init__(self):
        """Инициализирует объект на игровом поле."""
        self.position = CENTER_POSITION
        self.body_color = None

    def draw(self) -> None:
        """Шаблон для подклассов."""
        raise NotImplementedError('Метод draw ещё не реализован')

    def reset(self):
        """Обнуление self.position."""
        self.position = []


class Apple(GameObject):
    """Яблоко."""

    def __init__(self, positions=CENTER_POSITION):
        """Инициализирует яблоко на игровом поле."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(positions)

    def randomize_position(self, positions=CENTER_POSITION) -> None:
        """Генерируем новое яблоко."""
        while True:
            new_apple = (
                randrange(0, SCREEN_WIDTH, GRID_SIZE),
                randrange(0, SCREEN_HEIGHT, GRID_SIZE)
            )
            if new_apple not in positions:
                break
        self.position = new_apple

    def draw(self) -> None:
        """Рисуем яблоко на поле."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Змейка."""

    def __init__(self):
        """Инициализирует змейку на игровом поле."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.positions = self.position

    def draw(self) -> None:
        """Рисуем змейку на поле."""
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки:
        head_rect = pg.Rect(
            self.get_head_position(), (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента:
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self) -> None:
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
        self.last = self.positions[-1]

        if len(self.positions) > self.length:
            self.positions.pop()
        else:
            self.last = None

    def get_head_position(self) -> tuple:
        """Берем координаты головы змейки."""
        return self.positions[0]

    def update_direction(self) -> None:
        """Обновляем направление змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self) -> None:
        """Возвращение змейки в исходное состояние."""
        self.length = 1
        self.positions = CENTER_POSITION
        self.direction = choice((UP, DOWN, LEFT, RIGHT))
        self.last = None


def handle_keys(game_object) -> None:
    """Регулировка направления движения змейки и функция выхода."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Main - есть Main."""
    pg.init()

    snake = Snake()
    apple = Apple(snake.positions)

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
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.position)

        snake.draw()
        apple.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
