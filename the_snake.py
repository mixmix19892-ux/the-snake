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

GRID_COLOR = (0, 125, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    def __init__(self, position=SCREEN_CENTER, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        pass


class Grid(GameObject):
    def __init__(self, body_color, grid_width, grid_height, grid_size):
        super().__init__((0, 0), body_color)
        self.grid = self.init_grid(grid_width, grid_height, grid_size)
        self.grid_size = grid_size

    def init_grid(self, grid_width, grid_height, grid_size):
        out = []
        for width in range(0, grid_width):
            x = width * grid_size
            for height in range(0, grid_height):
                y = height * grid_size

                out.append((x, y))

        return out

    def draw(self):
        for position in self.grid:
            rect = pygame.Rect(position, (self.grid_size, self.grid_size))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color=body_color)
        self.randomize_position()

    def randomize_position(self):
        x = randint(0, GRID_WIDTH) * GRID_SIZE
        y = randint(0, GRID_HEIGHT) * GRID_SIZE

        x = x % SCREEN_WIDTH
        y = y % SCREEN_HEIGHT

        self.position = (x, y)

    """Метод draw класса Apple"""

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color=body_color)
        self.reset()

    """Метод обновления направления после нажатия на кнопку"""

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def collision(self, object: GameObject) -> bool:
        position1 = self.positions[0]
        position2 = object.position

        if position1 == position2:
            return True

        return False

    def self_collision(self) -> bool:
        head = self.get_head_position()
        body = self.positions

        for segment in body[1:]:
            if head == segment:
                return True

        return False

    def move(self):
        """
        move — обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions и удаляя последний элемент,
        если длина змейки не увеличилась.
        """
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

    """Метод draw класса Snake"""

    def draw(self):
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
        return self.positions[0]

    def reset(self):
        """reset — сбрасывает змейку в начальное состояние."""
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


def main():
    """Основная функция скрипта"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    grid = Grid(BOARD_BACKGROUND_COLOR, GRID_WIDTH, GRID_HEIGHT, GRID_SIZE)

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        #grid.draw()

        apple.draw()

        snake.update_direction()
        snake.move()
        hit = snake.collision(apple)

        if hit:
            snake.length += 1
            apple.randomize_position()

        hit = snake.self_collision()

        if hit:
            snake.reset()
            apple.randomize_position()

        snake.draw()

        handle_keys(snake)

        pygame.display.update()


if __name__ == "__main__":
    main()
