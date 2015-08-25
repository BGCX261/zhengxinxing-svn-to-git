#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import common

LEFT = 0
RIGHT = 1
DOWN = 2

class Block(pygame.sprite.Sprite):

    number = 0 # 每个block都要有一个唯一的id号，该号码从1开始无限递增

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        Block.number += 1 # 每次生成一个block，都将该号码递增
        self.id = Block.number
        self.image = common.load_image('block.bmp')
        self.rect = self.image.get_rect()
        self.move = common.SIDE_LENGTH
        self.move_direction = [0, 0, 0] # 左、右、下

    def update(self):
        self._move()

    def _move(self):
        # 现在开始移动
        if self.move_direction[LEFT]:
            self.rect = self.rect.move((-self.move, 0))
            self.move_direction[LEFT] = 0
        elif self.move_direction[RIGHT]:
            self.rect = self.rect.move((self.move, 0))
            self.move_direction[RIGHT] = 0
        elif self.move_direction[DOWN]:
            self.rect = self.rect.move((0, self.move*self.move_direction[DOWN]))
            self.move_direction[DOWN] = 0

    def move_left(self):
        self.move_direction[LEFT] = 1
        #self.right = 0

    def move_right(self):
        self.move_direction[RIGHT] = 1
        #self.left = 0

    def move_down(self, bottoms, steps=1):
        self.move_direction[DOWN] = steps

    def set_pos(self, x=0, y=0):
        self.rect.topleft = (x, y)

    def get_rect(self):
        return self.rect

    def get_id(self):
        return self.id

    def __str__(self):
        return 'Block(%d-%s%s)' % (self.id, self.rect.topleft, self.rect.size)
