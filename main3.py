import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройки окна
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Аркадная игра - Улучшенная версия")

# Загрузка изображений
def load_image(name, scale=1, flip_x=False, flip_y=False):
    try:
        image = pygame.image.load(name)
        if scale != 1:
            size = image.get_size()
            image = pygame.transform.scale(image, (int(size[0] * scale), int(size[1] * scale)))
        if flip_x or flip_y:
            image = pygame.transform.flip(image, flip_x, flip_y)
        return image
    except:
        print(f"Не могу загрузить изображение: {name}")
        # Создаем заглушку
        surf = pygame.Surface((50, 50))
        surf.fill((255, 0, 255))
        return surf

# Загрузка фона
try:
    background = pygame.image.load('fon.png')
    background = pygame.transform.scale(background, (window_width, window_height))
except:
    background = pygame.Surface((window_width, window_height))
    background.fill((135, 206, 235))  # Голубой фон если нет изображения

# Класс игрока (в 3 раза меньше, полное управление)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("character.png", 0.1)  # Уменьшаем в 3 раза
        self.rect = self.image.get_rect()
        self.rect.centerx = window_width // 2
        self.rect.centery = window_height // 2
        self.speed = 8

    def update(self):
        keys = pygame.key.get_pressed()
        
        # Сбрасываем скорость
        dx, dy = 0, 0
        
        # Обработка управления
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed
        
        # Обновляем позицию
        self.rect.x += dx
        self.rect.y += dy
        
        # Ограничение движения в пределах экрана
        self.rect.x = max(0, min(self.rect.x, window_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, window_height - self.rect.height))

# Класс врага (движется справа налево)
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("enemy.png", 0.2)
        self.rect = self.image.get_rect()
        self.rect.x = window_width  # Появляются справа
        self.rect.y = random.randint(0, window_height - self.rect.height)
        self.speed_x = random.randint(-5, -2)  # Движение влево

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right < 0:  # Если ушли за левый край
            self.rect.x = window_width  # Возвращаем справа
            self.rect.y = random.randint(0, window_height - self.rect.height)
            self.speed_x = random.randint(-5, -2)

# Класс стрелы (в 5 раз меньше, направлены вправо, вылетают из центра персонажа)
class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("arrow.png", 0.1, False, False)  # Отражение по горизонтали
        self.rect = self.image.get_rect()
        self.rect.centerx = x  # Центрируем по x
        self.rect.centery = y  # Центрируем по y
        self.speed = 10

    def update(self):
        self.rect.x += self.speed  # Движение вправо
        if self.rect.left > window_width:  # Если ушли за правый край
            self.kill()

# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
arrows = pygame.sprite.Group()

# Создание игрока
player = Player()
all_sprites.add(player)

# Создание врагов (теперь только 3)
for i in range(2):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Игровой цикл
clock = pygame.time.Clock()
running = True

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Стрела вылетает из центра персонажа
                arrow = Arrow(player.rect.centerx, player.rect.centery)
                all_sprites.add(arrow)
                arrows.add(arrow)

    # Обновление
    all_sprites.update()

    # Проверка столкновений
    hits = pygame.sprite.groupcollide(arrows, enemies, True, True)
    
    # Добавляем новых врагов при необходимости (поддерживаем 3 врага)
    while len(enemies) < 2:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Отрисовка
    window.blit(background, (0, 0))
    all_sprites.draw(window)
    pygame.display.flip()

    # Управление FPS
    clock.tick(60)

pygame.quit()
sys.exit()
