from random import randint

import pygame

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс всех обьектов змейки"""

    def __init__(self, position=SCREEN_CENTER, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки"""
        pass


class Apple(GameObject):
    """Класс отвечающий за яблоко на поле змейки"""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color=body_color)
        self.randomize_position()

    def randomize_position(self):
        """Рандомизировать позицию яблока"""
        x = randint(0, GRID_WIDTH) * GRID_SIZE
        y = randint(0, GRID_HEIGHT) * GRID_SIZE

        x = x % SCREEN_WIDTH
        y = y % SCREEN_HEIGHT

        self.position = (x, y)

    def draw(self):
        """Отрисовка яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


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
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

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


def collision_check(position, position_list) -> bool:
    """Проверка коллизии координаты против списка координат"""
    for pos in position_list:
        if position == pos:
            return True
    return False


def main():
    """Основная функция скрипта"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()

        snake.update_direction()
        snake.move()

        # Столкновение змейки с яблоком
        snake_head = snake.get_head_position()
        apple_position = apple.position

        if collision_check(snake_head, [apple_position]):
            snake.length += 1
            apple.randomize_position()

        # Столкновение змейки с самой собой:
        snake_head = snake.get_head_position()
        snake_body = snake.positions

        if collision_check(snake_head, snake_body[1:]):
            snake.reset()
            apple.randomize_position()

        snake.draw()

        handle_keys(snake)

        pygame.display.update()


if __name__ == "__main__":
    main()
