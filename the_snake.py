from random import choice, randint

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
    """Базовый класс для всех объектов игры. 
    У него будет позиция и цвет тела."""

    def __init__(self, position=(0, 0)):
        self.position = position
        self.body_color = None
    
    def draw(self):
        pass


class Apple(GameObject):
    '''Класс для яблока. Он наследуется 
    от GameObject и имеет метод 
    для случайного размещения на поле.'''
    
    def __init__(self, position=(0, 0)):
        super().__init__(position)
        self.body_color = APPLE_COLOR
        self.randomize_position()
                
    def randomize_position(self):
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
    
    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class Snake(GameObject):
    '''Класс для змейки. Он наследуется от GameObject
    и имеет методы для движения и управления направлением.'''

    def __init__(self, position=(0, 0)):
        super().__init__(position)
        self.length = 1
        self.body_color = SNAKE_COLOR
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = self.positions[-1]

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
            
    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        new_head = ((head[0] + x * GRID_SIZE) % SCREEN_WIDTH, (head[1] + y * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head)
        
        if len(self.positions) > self.length + 1:
            self.last = self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def get_head_position(self):
        return self.positions[0]
            
    def draw(self):
        for position in self.positions[:-1]:
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


def handle_keys(game_object):
    '''Функция для обработки нажатий клавиш. Она изменяет направление движения змейки в зависимости от нажатых клавиш.'''
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
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake((GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE))
    apple = Apple((0, 0))
    
        # Основной цикл игры:

    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            while apple.position in snake.positions:
                apple.randomize_position()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
        # Тут нужно отрисовать все объекты на игровом поле.
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()
        
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            raise SystemExit

if __name__ == '__main__':
    main()


