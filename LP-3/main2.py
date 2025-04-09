import pygame
class Player(pygame.sprite.Sprite):
    def __init__(self, filename, hero_x=100, hero_y=250, x_speed=0, y_speed=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename) # загрузка героя из файла
        self.rect = self.image.get_rect()
        self.hero_x = hero_x
        self.hero_y = hero_y
        # ставим персонажа в переданную точку (x, y):
        self.rect.x = hero_x
        self.rect.y = hero_y
        # создаем скорость движения спрайта:
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        ''' перемещает персонажа,
        применяя текущую горизонтальную и вертикальную скорость''' 
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

filename = 'character.png'
hero = Player(filename)
print(hero.__dict__)
