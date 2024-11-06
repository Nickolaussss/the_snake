from random import choice, randrange

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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

# Цвет гнилого яблока:
ROTTEN_APPLE = (107, 142, 35)

# Цвет Яда:
POISON = (255, 69, 0)

# Цвет змейки:
SNAKE_COLOR = (250, 128, 114)

# Цвет скина эпической змейки:
EPIC_SNAKE_COLOR = (138, 43, 226)

# Цвет скина мифической змейки:
MYTHICAL_SNAKE_COLOR = (139, 0, 0)

# Цвет камня:
STONE_COLOR = (128, 128, 128)

# Цвет золотой монеты:
GOLDEN_COIN = (255, 215, 0)

# Скорость движения змейки:
speed = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Супер змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Игровое поле"""

    snake_place: list = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
    taken_place: list[tuple] = []

    def __init__(self):
        self.position = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.body_color = None
        self.rendering = None
        self.object = None

    def replenish_taken_place(self, new_coordinates: tuple) -> None:
        """Добавляем новые координаты элементов (кроме тела змейки) \
        в taken_place. В случае поражения обнуляем taken_place"""
        if new_coordinates:
            GameObject.taken_place.append(new_coordinates)
        else:
            GameObject.taken_place = []

    def draw(self) -> None:
        """Шаблон для подклассов"""
        pass

    def random_selection(self):
        """Шаблон для подклассов"""
        pass

    def reset(self):
        """Обнуление self.position и  taken_place"""
        self.position = []
        GameObject.taken_place = []


class Apple(GameObject):
    """Яблоко"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self) -> tuple:
        """Генерируем новое яблоко и добавляем координаты яблока \
        в taken_place"""
        new_apple = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                     randrange(0, SCREEN_HEIGHT, GRID_SIZE))

        while new_apple in GameObject.snake_place \
                or new_apple in GameObject.taken_place:
            new_apple = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                         randrange(0, SCREEN_HEIGHT, GRID_SIZE))

        self.replenish_taken_place(new_apple)

        return new_apple

    def draw(self) -> None:
        """Рисуем яблоко на поле"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Змейка"""

    def __init__(self):
        super().__init__()
        self.positions = self.position
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self) -> None:
        """Рисуем змейку на поле"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки:
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента:
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self) -> None:
        """Передвижение змейки и добавление координатов змеи в snake_place"""
        x, y = self.get_head_position()
        new_head = ((x + (self.direction[0] * GRID_SIZE)) % SCREEN_WIDTH,
                    (y + (self.direction[1] * GRID_SIZE)) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)
        self.last = self.positions[-1]

        if len(self.positions) > self.length:
            self.positions.pop()

        GameObject.snake_place = self.positions

    def get_head_position(self) -> tuple:
        """Берем координаты головы змейки"""
        return self.positions[0]

    def update_direction(self) -> None:
        """Обновляем направление змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def change_speed(self) -> int:
        """Меняет скорость змейки"""
        speed = 5
        if 0 < self.length < 4:
            speed = 5
        elif 3 < self.length < 7:
            speed = 7
        elif 6 < self.length < 11:
            speed = 9
        elif 10 < self.length < 16:
            speed = 14
        elif 15 < self.length < 21:
            self.body_color = SNAKE_COLOR
            speed = 17
        elif 20 < self.length < 31:
            self.body_color = EPIC_SNAKE_COLOR
            speed = 22
        elif 30 < self.length:
            self.body_color = MYTHICAL_SNAKE_COLOR
            speed = 25
        return speed

    def reset(self) -> None:
        """Возвращение змейки в исходное состояние"""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.body_color = SNAKE_COLOR


class Stone(GameObject):
    """Камень"""

    def __init__(self):
        super().__init__()
        self.position = self.randomize_position()
        self.body_color = STONE_COLOR

    def randomize_position(self) -> list[tuple]:
        """Генерируем камни и добавляем координаты камней в taken_place"""
        new_list: list[tuple] = []
        for _ in range(3):
            new_place = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                         randrange(0, SCREEN_HEIGHT, GRID_SIZE))
            while new_place in GameObject.snake_place:
                new_place = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                             randrange(0, SCREEN_HEIGHT, GRID_SIZE))

            new_list.insert(0, new_place)

            self.replenish_taken_place(new_place)

        return new_list

    def draw(self) -> None:
        """Рисуем камни на поле"""
        for position in self.position:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Rotten(GameObject):
    """Гнилое яблоко"""

    def __init__(self):
        super().__init__()
        self.position = []
        self.body_color = ROTTEN_APPLE

    def randomize_position(self) -> list[tuple]:
        """Генерируем гнилое яблоко и добавляем координаты гнилого яблока \
        в taken_place"""
        new_place = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                     randrange(0, SCREEN_HEIGHT, GRID_SIZE))
        while new_place in GameObject.taken_place \
                or new_place in GameObject.snake_place:
            new_place = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                         randrange(0, SCREEN_HEIGHT, GRID_SIZE))
        self.position.append(new_place)
        self.replenish_taken_place(new_place)
        self.rendering = new_place

        return self.position

    def draw(self) -> None:
        """Рисуем гнилое яблоко на поле"""
        rect = (pygame.Rect(self.rendering, (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.object:
            last_rect = pygame.Rect(self.object, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


class Poison(GameObject):
    """Яд"""

    def __init__(self):
        super().__init__()
        self.position = []
        self.body_color = POISON

    def randomize_position(self) -> list[tuple]:
        """Генерируем яд и добавляем координаты яда в taken_place"""
        new_place = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                     randrange(0, SCREEN_HEIGHT, GRID_SIZE))
        while new_place in GameObject.taken_place \
                or new_place in GameObject.snake_place:
            new_place = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                         randrange(0, SCREEN_HEIGHT, GRID_SIZE))
        self.position.append(new_place)
        self.replenish_taken_place(new_place)
        self.rendering = new_place

        return self.position

    def draw(self) -> None:
        """Рисуем яд на поле"""
        rect = (pygame.Rect(self.rendering, (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.object:
            for poison in self.object:
                last_rect = pygame.Rect(poison, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


class Coin(GameObject):
    """Золотая монета"""

    def __init__(self):
        super().__init__()
        self.position = []
        self.body_color = GOLDEN_COIN

    def randomize_position(self) -> list[tuple]:
        """Генерируем золотую монету и добавляем координаты золотой монеты \
        в taken_place"""
        new_place = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                     randrange(0, SCREEN_HEIGHT, GRID_SIZE))
        while new_place in GameObject.taken_place \
                or new_place in GameObject.snake_place:
            new_place = (randrange(0, SCREEN_WIDTH, GRID_SIZE),
                         randrange(0, SCREEN_HEIGHT, GRID_SIZE))
        self.position.append(new_place)
        self.replenish_taken_place(new_place)
        self.rendering = new_place

        return self.position

    def draw(self) -> None:
        """Рисуем золотую монету на поле"""
        rect = (pygame.Rect(self.rendering, (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def random_selection(self, is_bool=None) -> None:
        """Лотерея"""
        if is_bool:
            if randrange(0, 300) == randrange(0, 300):
                self.randomize_position()
                self.draw()
        else:
            self.randomize_position()
            self.draw()


def handle_keys(game_object) -> None:
    """Регулировка направления движения змейки и функция выхода"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def random_generator(golden_coin, poison, rotten):
    """Функция выбирает случайный элемент"""
    if randrange(0, 30) == randrange(0, 30):
        golden_coin.random_selection(False)
    elif randrange(0, 7) == randrange(0, 7):
        poison.randomize_position()
        poison.draw()
    elif randrange(0, 3) == randrange(0, 3):
        rotten.randomize_position()
        rotten.draw()


def main() -> None:
    """Main - есть Main"""
    global speed

    pygame.init()

    snake = Snake()
    stone = Stone()
    apple = Apple()
    poison = Poison()
    rotten = Rotten()
    golden_coin = Coin()

    while True:
        clock.tick(speed)
        snake.draw()
        stone.draw()
        apple.draw()

        golden_coin.random_selection(True)

        snake.move()

        handle_keys(snake)
        snake.update_direction()

        if snake.positions[0] == apple.position:
            value = snake.positions[0]
            GameObject.taken_place.remove(value)
            snake.length += 1
            apple.position = apple.randomize_position()

            random_generator(golden_coin, poison, rotten)

            speed = snake.change_speed()

        if snake.positions[0] in snake.positions[1:]:
            snake.reset()
            rotten.reset()
            poison.reset()
            golden_coin.reset()
            speed = 5
            apple.position = apple.randomize_position()
            stone.position = stone.randomize_position()

        if snake.positions[0] in stone.position:
            snake.reset()
            rotten.reset()
            poison.reset()
            golden_coin.reset()
            speed = 5
            apple.position = apple.randomize_position()
            stone.position = stone.randomize_position()

        if snake.positions[0] in rotten.position:
            value = snake.positions[0]
            rotten.position.remove(value)
            GameObject.taken_place.remove(value)

            if len(snake.positions) > 1:
                rotten.object = snake.positions[-1]
                snake.positions.pop(-1)
                snake.length -= 1
                rotten.draw()

                speed = snake.change_speed()
            else:
                snake.reset()
                rotten.reset()
                poison.reset()
                golden_coin.reset()
                speed = 5
                apple.position = apple.randomize_position()
                stone.position = stone.randomize_position()

        if snake.positions[0] in poison.position:
            value = snake.positions[0]
            poison.position.remove(value)
            GameObject.taken_place.remove(value)

            if len(snake.positions) > 3:
                poison.object = snake.positions[-3:]
                del snake.positions[-3:]
                snake.length -= 3
                poison.draw()

                speed = snake.change_speed()

            else:
                snake.reset()
                rotten.reset()
                poison.reset()
                golden_coin.reset()
                speed = 5
                apple.position = apple.randomize_position()
                stone.position = stone.randomize_position()

        if snake.positions[0] in golden_coin.position:
            golden_coin.position.remove(snake.positions[0])
            GameObject.taken_place.remove(snake.positions[0])

            digit = randrange(1, 10)
            snake.length += digit

            speed = snake.change_speed()

        pygame.display.update()


if __name__ == '__main__':
    main()
