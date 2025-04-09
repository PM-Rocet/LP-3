import pygame
import time

pygame.init()

# Глобальные переменные (настройки)
window_width = 800
window_height = 600
fon = 'cosmos.jpg'  # изображение должно быть в том же каталоге, что и код

# Запуск
window = pygame.display.set_mode([window_width, window_height])  # создание окна указанных размеров
pygame.display.set_caption("Игра v1.0")  # установка заголовка окна

speed = 0  # текущая скорость перемещения
sdvig_fona = 0  # сдвиг фона

img1 = pygame.image.load(fon)  # загрузка фона игры из файла
back_fon = pygame.transform.scale(img1, (window_width, window_height))  # подгоняем под размер окна

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Закрытие окна
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:  # Двигаем фон влево при нажатии "Вправо"
                speed = -5
            if event.key == pygame.K_LEFT:  # Останавливаем фон при нажатии "Влево"
                speed = 0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                speed = 0

    # Обновление позиции фона
    sdvig_fona += speed

    # Зацикливание фона
    if sdvig_fona <= -window_width:
        sdvig_fona = 0

    # Рисуем два изображения, чтобы создать эффект бесконечного фона
    window.blit(back_fon, (sdvig_fona, 0))
    window.blit(back_fon, (sdvig_fona + window_width, 0))

    pygame.display.update()  # Обновляем экран
    time.sleep(0.02)  # Небольшая задержка для плавности

pygame.quit()  # Закрытие Pygame
