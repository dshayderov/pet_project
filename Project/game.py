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
BACKGROUND_COLOR = "#AFEEEE"

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


def load_level():
    with open("%s/levels/lvl1.txt" % FILE_DIR) as fil:
        levelfile = fil.readlines()
    for line in levelfile:
        level.append(line)


def main():
    load_level()
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окно
    pygame.display.set_caption("Project")
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    bg.fill(Color(BACKGROUND_COLOR))

    left = right = False
    up = False

    hero = Player(50, 50)

    timer = pygame.time.Clock()
    x = y = 0  # координаты
    for row in level:
        for col in row:
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
                animatedEntities.add(bd)
            if col == "K":
                pr = Key(x, y)
                entities.add(pr)
                platforms.append(pr)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = (
        len(level[0]) * PLATFORM_WIDTH
    )  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while not hero.winner:
        timer.tick(60)
        for e in pygame.event.get():
            if e.type == QUIT:
                exit()
            if e.type == KEYDOWN and (e.key == K_UP or e.key == K_w):
                up = True
            if e.type == KEYDOWN and (e.key == K_LEFT or e.key == K_a):
                left = True
            if e.type == KEYDOWN and (e.key == K_RIGHT or e.key == K_d):
                right = True

            if e.type == KEYUP and (e.key == K_UP or e.key == K_w):
                up = False
            if e.type == KEYUP and (e.key == K_RIGHT or e.key == K_d):
                right = False
            if e.type == KEYUP and (e.key == K_LEFT or e.key == K_a):
                left = False

        screen.blit(bg, (0, 0))

        animatedEntities.update()
        monsters.update(platforms)
        camera.update(hero)
        hero.update(left, right, up, platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        pygame.display.update()


level = []
entities = pygame.sprite.Group()
animatedEntities = pygame.sprite.Group()
monsters = pygame.sprite.Group()
platforms = []


if __name__ == "__main__":
    main()
