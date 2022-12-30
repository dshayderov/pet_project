#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import pyganim
import os

MONSTER_WIDTH = 60
MONSTER_HEIGHT = 37
MONSTER_COLOR = "#2110FF"
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами

ANIMATION_MONSTERHORYSONTAL = [
    ("%s/img/enemies/enemyFlying_1.png" % ICON_DIR),
    ("%s/img/enemies/enemyFlying_2.png" % ICON_DIR),
    ("%s/img/enemies/enemyFlying_3.png" % ICON_DIR),
]


class Monster(sprite.Sprite):
    def __init__(self, x, y, left=2, up=3, maxlengthleft=100, maxlengthup=100):
        sprite.Sprite.__init__(self)
        self.image = Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
        self.image.fill(Color(MONSTER_COLOR))
        self.rect = Rect(x, y, MONSTER_WIDTH, MONSTER_HEIGHT)
        self.image.set_colorkey(Color(MONSTER_COLOR))
        self.startX = x
        self.startY = y
        self.maxLengthLeft = maxlengthleft  # максимальное расстояние, которое может пройти в одну сторону
        self.maxLengthUp = maxlengthup  # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.xvel = left  # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = up  # скорость движения по вертикали, 0 - не двигается
        boltanim = []
        for anim in ANIMATION_MONSTERHORYSONTAL:
            boltanim.append((anim, 1))
        self.boltAnim = pyganim.PygAnimation(boltanim)
        self.boltAnim.play()

    def update(self, platforms):

        self.image.fill(Color(MONSTER_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        self.collide(platforms)

        if abs(self.startX - self.rect.x) > self.maxLengthLeft:
            self.xvel = (
                -self.xvel
            )  # если прошли максимальное растояние, то идеи в обратную сторону
        if abs(self.startY - self.rect.y) > self.maxLengthUp:
            self.yvel = (
                -self.yvel
            )  # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль

    def collide(self, platforms):
        for p in platforms:
            if (
                sprite.collide_rect(self, p) and self != p
            ):  # если с чем-то или кем-то столкнулись
                self.xvel = -self.xvel  # то поворачиваем в обратную сторону
                self.yvel = -self.yvel
