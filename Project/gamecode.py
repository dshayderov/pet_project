#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import os


if __name__ == '__main__':
    WIDTH = 800
    HEIGHT = 480
    FPS = 30

    # Задаем цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # настройка папки ассетов
    game_folder = os.path.dirname(__file__)
    img_folder = os.path.join(game_folder, 'img')
    player_img = pygame.image.load(os.path.join(img_folder, 'creature-2.png'))
    mob_img = pygame.image.load(os.path.join(img_folder, 'creature-3.png'))
    sword_img = pygame.image.load(os.path.join(img_folder, 'sword.png'))

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = player_img
            self.rect = self.image.get_rect()
            self.rect.centerx = (WIDTH / 2 - 5)
            self.rect.bottom = (HEIGHT - 1)
            self.speedx = 0
            self.speedy = 0
            self.isJump = False
            self.jumpCount = 10

        def update(self):
            self.speedx = 0
            self.speedy = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
                self.speedx = -8
            if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
                self.speedx = 8
            if keystate[pygame.K_UP] or keystate[pygame.K_w]:
                self.isJump = True

            if self.isJump is True:

                if self.jumpCount >= -10:
                    if self.jumpCount < 0:
                        self.rect.y += (self.jumpCount ** 2) // 2
                    else:
                        self.rect.y -= (self.jumpCount ** 2) // 2
                    self.jumpCount -= 1

                else:
                    self.isJump = False
                    self.jumpCount = 10

            self.rect.x += self.speedx
            self.rect.y += self.speedy
            if self.rect.left > WIDTH:
                self.rect.right = 0
            if self.rect.right < 0:
                self.rect.left = WIDTH

        def fight(self):
            sword = Sword()
            all_sprites.add(sword)

    class Mob(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = mob_img
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(0, HEIGHT)
            self.speedy = 0

        def update(self):
            self.rect.y += self.speedy
            if self.rect.top > HEIGHT + 10:
                self.rect.x = random.randrange(WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(1, 8)

    class Sword(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = sword_img
            self.rect = self.image.get_rect()
            self.rect.y = player.rect.y + 10
            self.rect.x = player.rect.right - 10

        def update(self):
            self.rect.x += player.speedx
            self.rect.y = player.rect.y + 10

        def draw(self):
            screen.blit(self.image, self.rect)

    # Создаем игру и окно
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    for i in range(3):
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    # Цикл игры
    running = True
    while running:
        # Держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # check for closing windowa
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player.fight()
                    pygame.time.set_timer(3, True)

        # Обновление
        all_sprites.update()

        # Проверка, не ударил ли моб игрока
        hits = pygame.sprite.spritecollide(player, mobs, False)
        if hits:
            running = False

        # Рендеринг
        screen.fill(BLUE)
        all_sprites.draw(screen)
        # После отрисовки всего, переворачиваем экран
        pygame.display.flip()

    pygame.quit()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
from player import *
from blocks import *
from enemies import *

# Объявляем переменные
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#000000"

FILE_DIR = os.path.dirname(__file__)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def loadLevel():
    with open('%s/levels/lvl1.txt' % FILE_DIR) as fil:
        levelFile = fil.readlines()
    for line in levelFile:
        level.append(line)


def main():
    loadLevel()
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Project")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

    left = right = False  # по умолчанию - стоим
    up = False

    hero = Player(50, 50)

    timer = pygame.time.Clock()
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "O":
                hero = Player(x, y)
                entities.add(hero)
            if col == "Y":
                mn = Monster(x, y)
                entities.add(mn)
                platforms.append(mn)
                monsters.add(mn)
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                bd = BlockDie(x, y)
                entities.add(bd)
                platforms.append(bd)
            if col == "K":
                pr = Key(x, y)
                entities.add(pr)
                platforms.append(pr)
                animatedEntities.add(pr)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while not hero.winner:  # Основной цикл программы
        timer.tick(60)
        keystate = pygame.key.get_pressed()
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                exit()
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                running = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_LSHIFT:
                running = False

        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        animatedEntities.update()  # показываеaм анимацию
        monsters.update(platforms)  # передвигаем всех монстров
        camera.update(hero)  # центризируем камеру относительно персонажа
        hero.update(left, right, up, platforms)  # передвижение
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()  # обновление и вывод всех изменений на экран


level = []
entities = pygame.sprite.Group()  # Все объекты
animatedEntities = pygame.sprite.Group()  # все анимированные объекты, за исключением героя
monsters = pygame.sprite.Group()  # Все передвигающиеся объекты
platforms = []  # то, во что мы будем врезаться или опираться


if __name__ == "__main__":
    main()