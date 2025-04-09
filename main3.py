import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройки окна
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Аркадная игра")


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


# Загрузка фона и финального изображения
try:
    background = pygame.image.load('cosmos.jpg')
    background = pygame.transform.scale(background, (window_width, window_height))
    game_over_image = pygame.image.load('game_over.jpg')  # Финальное изображение
    game_over_image = pygame.transform.scale(game_over_image, (window_width, window_height))
except:
    background = pygame.Surface((window_width, window_height))
    background.fill((135, 206, 235))
    game_over_image = pygame.Surface((window_width, window_height))
    game_over_image.fill((255, 0, 0))
    font = pygame.font.SysFont(None, 72)
    game_over_image.blit(font.render("GAME OVER", True, (255, 255, 255)), (250, 250))


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("character.png", 0.1)
        self.rect = self.image.get_rect()
        self.rect.centerx = window_width // 2
        self.rect.centery = window_height // 2
        self.speed = 8
        self.alive = True  # Флаг жизни игрока

    def update(self):
        if not self.alive:
            return

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed

        self.rect.x += dx
        self.rect.y += dy
        self.rect.x = max(0, min(self.rect.x, window_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, window_height - self.rect.height))


# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("enemy.png", 0.2)
        self.rect = self.image.get_rect()
        self.rect.x = window_width
        self.rect.y = random.randint(0, window_height - self.rect.height)
        self.speed_x = random.randint(-5, -2)
        self.hitbox = pygame.Rect(0, 0, self.rect.width * 0.2, self.rect.height * 0.2)
        self.update_hitbox()

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.right < 0:
            self.rect.x = window_width
            self.rect.y = random.randint(0, window_height - self.rect.height)
            self.speed_x = random.randint(-5, -2)
        self.update_hitbox()

    def update_hitbox(self):
        self.hitbox.center = self.rect.center


# Класс стрелы
class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = load_image("arrow.png", 0.1, False, False)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > window_width:
            self.kill()


# Инициализация игры
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
arrows = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(2):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Игровой цикл
clock = pygame.time.Clock()
running = True
game_over = False

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                arrow = Arrow(player.rect.centerx, player.rect.centery)
                all_sprites.add(arrow)
                arrows.add(arrow)
            if event.key == pygame.K_r and game_over:  # Перезапуск игры по нажатию R
                # Сброс игры
                all_sprites.empty()
                enemies.empty()
                arrows.empty()

                player = Player()
                all_sprites.add(player)

                for i in range(2):
                    enemy = Enemy()
                    all_sprites.add(enemy)
                    enemies.add(enemy)

                game_over = False

    if not game_over:
        # Обновление
        all_sprites.update()

        # Проверка столкновений
        hits = []
        for arrow in arrows:
            for enemy in enemies:
                if arrow.rect.colliderect(enemy.hitbox):
                    hits.append((arrow, enemy))

        for arrow, enemy in hits:
            arrow.kill()
            enemy.kill()

        # Проверка столкновения игрока с врагом
        for enemy in enemies:
            if player.rect.colliderect(enemy.hitbox) and player.alive:
                player.alive = False
                game_over = True

        # Добавление новых врагов
        while len(enemies) < 2:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

    # Отрисовка
    window.blit(background, (0, 0))
    all_sprites.draw(window)

    if game_over:
        window.blit(game_over_image, (0, 0))
        # Отображение текста для перезапуска
        font = pygame.font.SysFont(None, 36)
        text = font.render("Нажмите R для перезапуска", True, (255, 255, 255))
        window.blit(text, (window_width // 2 - 150, window_height - 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()