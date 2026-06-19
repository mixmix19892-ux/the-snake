from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс всех обьектов змейки"""

    def __init__(self, position=SCREEN_CENTER, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Базовый метод отрисовки"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс отвечающий за яблоко на поле змейки"""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color=body_color)
        self.randomize_position(SCREEN_CENTER)

    def randomize_position(self, occupied_positions):
        """Рандомизировать позицию яблока"""
        while True:
            self.position = (
                (randint(0, GRID_WIDTH) * GRID_SIZE) % SCREEN_WIDTH,
                (randint(0, GRID_HEIGHT) * GRID_SIZE) % SCREEN_HEIGHT
            )

            if self.position not in occupied_positions:
                break


class Snake(GameObject):
    """Класс отвечающий за змейку"""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color=body_color)
        self.reset()

    def update_direction(self):
        """Метод обновления направления после нажатии на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод отвечающий за движение змейки"""
        hx, hy = self.get_head_position()
        dx, dy = self.direction
        x_size = dx * GRID_SIZE
        y_size = dy * GRID_SIZE

        x = (hx + x_size) % SCREEN_WIDTH
        y = (hy + y_size) % SCREEN_HEIGHT

        new_position = (x, y)

        self.positions.insert(0, new_position)

        if self.length != len(self.positions):
            self.last = self.positions.pop()

    def draw(self):
        """Метод отвечающий за отрисовку змейки"""
        for position in self.positions:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        self.position = self.get_head_position()
        super().draw()

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            self.last = None

    def get_head_position(self):
        """Метод возсращающий координаты головы змейки"""
        return self.positions[0]

    def reset(self):
        """Метод отвечающий за сбрасывание игры в начальное состояние"""
        self.length = 1
        self.direction = LEFT
        self.next_direction = None
        self.positions = [SCREEN_CENTER]
        self.last = None


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
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


def collision_check(position, position_list) -> bool:
    """Проверка коллизии координаты против списка координат"""
    return position in position_list


def main():
    """Основная функция скрипта"""
    # Инициализация pg:
    pg.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.update_direction()
        snake.move()

        # Столкновение змейки с яблоком
        if collision_check(snake.get_head_position(), [apple.position]):
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Столкновение змейки с самой собой:
        elif (
            snake.length >= 5
            and collision_check(snake.get_head_position(), snake.positions[1:])
        ):
            snake.reset()
            apple.randomize_position(snake.positions)

        handle_keys(snake)

        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
