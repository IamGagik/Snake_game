from random import choice, randint
import pygame


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Родительский-базовый класс для змейки и яблока."""

    def __init__(self):
        self.position = [(SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)]
        self.body_color = None

    def draw(self):
        """Метод-заглушка, предназначенная для унаследованных классов."""


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
        return (new_x, new_y)

    def draw(self):
        """Рисует яблоко."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий реализацию змейки."""

    def __init__(self):
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
        if new_x >= SCREEN_WIDTH or new_x < 0:
            new_x = new_x % SCREEN_WIDTH
        elif new_y >= SCREEN_HEIGHT or new_y < 0:
            new_y = new_y % SCREEN_HEIGHT
        new_h_p = (new_x, new_y)

        self.positions.insert(0, new_h_p)
        if len(self.positions) > self.lenght:
            self.last = self.positions[-1]
            self.positions.pop()

    def draw(self):
        """Рисует змейку и затирает хвост."""
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Обнуляет данные, при столкновении змейки с самой собой."""
        self.lenght = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None


def handle_keys(game_object):
    """Меняет направление движения змейки, в зависимости от нажатой кнопки."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
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
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        if handle_keys(snake) is False:
            pygame.quit()
            break
        else:
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
