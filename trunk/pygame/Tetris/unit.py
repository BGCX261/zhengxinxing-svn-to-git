#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import pygame
import common
from block import Block


class Unit(pygame.sprite.RenderUpdates):

    def __init__(self, game_zone):
        pygame.sprite.RenderUpdates.__init__(self)
        self.area = pygame.rect.Rect(game_zone)
        self.x = 0
        self.y = 0
        self.type = common.random_int(7) # 随机选择一种样式
        self._blocks = [Block(), Block(), Block(), Block()]
        self.bottomed = 0
        self.trigger = 1 # 用于 往返式的旋转控制

    def set_pos(self, x=0, y=0):
        self.x = x
        self.y = y
        self.__make_unit()

    def blocks(self):
        return self._blocks

    def isBottomed(self):
        return self.bottomed

    def move_down(self, bottoms):
        for block in self._blocks:
            hitbox = block.rect.inflate(0, 1) # 纵向放大，否则检测不出碰撞
            if hitbox.collidelist(bottoms) != -1 or \
            block.rect.bottom >= self.area.bottom:
                self.bottomed = 1
                return

        for block in self._blocks:
            block.move_down(bottoms)

    def move_left(self, bottoms):
        for block in self._blocks:
            # 如果遇见墙壁挡着，就不让左移
            if block.rect.left <= self.area.left:
                return
            # 如果遇见旧方块们挡着，也不让继续左移
            bottoms_blocks = bottoms.sprites()
            for bottom in bottoms_blocks:
                if block.rect.top == bottom.rect.top and \
                    block.rect.left == bottom.rect.right:
                    return

        for block in self._blocks:
            block.move_left()

    def move_right(self, bottoms):
        # 如果遇见墙壁挡着，就不让右移
        for block in self._blocks:
            if block.rect.right >= self.area.right:
                return
            # # 如果遇见旧方块们挡着，也不让继续右移
            bottoms_blocks = bottoms.sprites()
            for bottom in bottoms_blocks:
                if block.rect.top == bottom.rect.top and \
                    block.rect.right == bottom.rect.left:
                    return
        for block in self._blocks:
            block.move_right()

    def spin_clockwise(self, bottoms):
        # 顺时针旋转，以 _block[1] 为中心
        point = self._blocks[1].rect.topleft

        # 首先计算出旋转后的新位置
        new_rects = []
        for b in (self._blocks[0],self._blocks[2], self._blocks[3]):
            temp = (b.rect.topleft[0] - point[0], b.rect.topleft[1] - point[1])
            if self.type == 4: #O
                return
            elif self.type in (3, 5, 7): # I、Z、anti-Z，往返变化
                if self.trigger:
                    temp = (-temp[1], temp[0])
                else:
                    temp = (temp[1], -temp[0])
            else: # L 、T、anti-L，中心旋转变化
                temp = (-temp[1], temp[0])
            new_rects.append(pygame.rect.Rect((temp[0] + point[0], temp[1] + point[1],
                                               common.SIDE_LENGTH, common.SIDE_LENGTH)))

        # 然后看看新位置是否合法
        for r in new_rects:
            if r.collidelist(bottoms.sprites()) != -1:
                return
            if not self.area.contains(r):
                return

        # 接着再进行实际的旋转
        self._blocks[0].rect.topleft = new_rects[0].topleft
        self._blocks[2].rect.topleft = new_rects[1].topleft
        self._blocks[3].rect.topleft = new_rects[2].topleft

        # 最后将触发器翻转一下
        self.trigger = self.trigger ^ 1 # 进行异或运算，实现0、1交替

    def spin_anticlockwise(self):
        pass

    def __make_unit(self):
        # 组合方块时，要将 _block[1] 设置为中心，方便移动
        if self.type == 1: # T
            self._blocks[0].set_pos(self.x, self.y)
            self._blocks[1].set_pos(self.x+common.SIDE_LENGTH, self.y)
            self._blocks[2].set_pos(self.x+2*common.SIDE_LENGTH, self.y)
            self._blocks[3].set_pos(self.x+common.SIDE_LENGTH, self.y+common.SIDE_LENGTH)
        elif self.type == 2: # L
            self._blocks[0].set_pos(self.x, self.y)
            self._blocks[1].set_pos(self.x+common.SIDE_LENGTH, self.y)
            self._blocks[2].set_pos(self.x+2*common.SIDE_LENGTH, self.y)
            self._blocks[3].set_pos(self.x+2*common.SIDE_LENGTH, self.y+common.SIDE_LENGTH)
        elif self.type == 3: # I
            self._blocks[0].set_pos(self.x, self.y)
            self._blocks[1].set_pos(self.x+common.SIDE_LENGTH, self.y)
            self._blocks[2].set_pos(self.x+2*common.SIDE_LENGTH, self.y)
            self._blocks[3].set_pos(self.x+3*common.SIDE_LENGTH, self.y)
        elif self.type == 4: # O
            self._blocks[0].set_pos(self.x, self.y)
            self._blocks[1].set_pos(self.x+common.SIDE_LENGTH, self.y)
            self._blocks[2].set_pos(self.x, self.y+common.SIDE_LENGTH)
            self._blocks[3].set_pos(self.x+common.SIDE_LENGTH, self.y+common.SIDE_LENGTH)
        elif self.type == 5: # Z
            self._blocks[0].set_pos(self.x, self.y)
            self._blocks[1].set_pos(self.x+common.SIDE_LENGTH, self.y)
            self._blocks[2].set_pos(self.x+common.SIDE_LENGTH, self.y+common.SIDE_LENGTH)
            self._blocks[3].set_pos(self.x+2*common.SIDE_LENGTH, self.y+common.SIDE_LENGTH)
        elif self.type == 6: # anti-L
            self._blocks[0].set_pos(self.x, self.y)
            self._blocks[1].set_pos(self.x+common.SIDE_LENGTH, self.y)
            self._blocks[2].set_pos(self.x, self.y+common.SIDE_LENGTH)
            self._blocks[3].set_pos(self.x+2*common.SIDE_LENGTH, self.y)
        elif self.type == 7: # anti-Z
            self._blocks[0].set_pos(self.x, self.y+common.SIDE_LENGTH)
            self._blocks[1].set_pos(self.x+common.SIDE_LENGTH, self.y)
            self._blocks[2].set_pos(self.x+common.SIDE_LENGTH, self.y+common.SIDE_LENGTH)
            self._blocks[3].set_pos(self.x+2*common.SIDE_LENGTH, self.y)



if __name__ == '__main__':

    pass
