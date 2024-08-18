from random import choice, randint
import pygame
from typing import Optional


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
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Родительский-базовый класс для змейки и яблока."""

    def __init__(self) -> None:
        self.position = [(SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)]
        self.body_color = Optional[tuple]

    def draw(self):
        """Метод-заглушка, предназначенная для унаследованных классов."""
        pass


class Apple(GameObject):
    """Класс, описывающий реализацию яблока в игре."""

    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Создает рандомные координаты для яблока."""
        new_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        new_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        position = (new_x, new_y)
        return position

    # def randomize_position(self, coordinates):
    #     """Метод, устанавливающий случайное положение яблока на поле."""
    #     self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
    #                      randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
    #     while self.position in coordinates:
    #         self.position = (
    #             randint(0, GRID_WIDTH - 1) * GRID_SIZE,
    #             randint(0, GRID_HEIGHT - 1) * GRID_SIZE
    #         )

    def draw(self):
        """Рисует яблоко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий реализацию змейки."""

    def __init__(self) -> None:
        super().__init__()
        self.lenght = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Реализует движение змейки."""
        head_position = self.get_head_position()
        new_x = list(head_position)[0] + (list(self.direction)[0] * GRID_SIZE)
        new_y = list(head_position)[1] + (list(self.direction)[1] * GRID_SIZE)
        if new_x > SCREEN_WIDTH:
            new_x = 0
        elif new_x < 0:
            new_x = SCREEN_WIDTH
        elif new_y > SCREEN_HEIGHT:
            new_y = 0
        elif new_y < 0:
            new_y = SCREEN_HEIGHT
        new_h_p = (new_x, new_y)

        self.positions.insert(0, new_h_p)
        if len(self.positions) > self.lenght:
            self.last = self.positions[-1]
            self.positions.pop()

    def draw(self):
        """Рисует змейку и затирает хвост."""
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Обнуляет данные, при столкновении змейки с самой собой."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.lenght = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """Меняет направление движения змейки, в зависимости от нажатой кнопки."""
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
    """Главная функция."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            apple.position = apple.randomize_position()
            apple.draw()
            snake.lenght += 1
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
