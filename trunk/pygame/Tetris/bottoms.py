#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import common

class Bottoms(pygame.sprite.RenderUpdates):

    def __init__(self, game_zone):
        pygame.sprite.RenderUpdates.__init__(self)
        # 这个2维数组用于标识小方块
        self.lines = [[0 for a in range(common.COL)] for b in range(common.ROW)]
        self.area = pygame.rect.Rect(game_zone)
        self._full = 0

    ##
    # 这里本来应该用 def add(self, *blocks) 这样的语法，可是由于 pygame.sprite 的
    # AbstractGroup.add() 的实现里面，使用了 self.add(str) 的语句，会导致调用的
    # 混乱，所以必须改名。解决办法：将其改为 AbstractGroup.add(self, str)
    ##
    def my_add(self, *blocks):
        pygame.sprite.RenderUpdates.add(self, blocks)

        # 计算小方块坐标，给相应的数组位置赋值
        for block in blocks:
            x, y = common.get_coordinates(self.area, block)
            self.lines[x][y] = block.get_id()
            if x==0:
                self._full = 1

    def check_linefull(self):
        '''Checks the bottom blocks and eliminates the full line.
        '''
        marks = [0] * common.ROW # 记录各行状态

        # 看看是否有满行出现，如果没有满行，本函数不做任何处理
        for i in range(common.ROW):
            marks[i] = common.check_list(self.lines[i])
        if common.ALL_NOT_ZERO not in marks:
            return

        # 有满行，则首先计算各行需下移的距离
        moves = self.__calculate_down_steps(marks)

        # 然后，删除block、移动各行
        for ii in range(common.ROW):
            i = -ii - 1     # 从最后一行开始处理
            if moves[i] == 0: pass  # 什么都不做
            elif moves[i] == -1:
                #delete the line
                line_blocks = self.__get_blocks_from_id(self.lines[i])
                for index in range(len(self.lines[i])):
                    self.lines[i][index] = 0
                pygame.sprite.RenderUpdates.remove(self, line_blocks)
            else:
                #move down the lines!
                line_blocks = self.__get_blocks_from_id(self.lines[i])
                for index in range(len(self.lines[i])):
                    self.lines[i + moves[i]][index] = self.lines[i][index]
                    self.lines[i][index] = 0
                for block in line_blocks:
                    block.move_down(self, moves[i])

    def __calculate_down_steps(self, marks):
        # [0,0,2,2,1,2,1,2] --> [0,0,2,2,-1,1,-1,0]
        moves = [0] * len(marks)
        step = 0
        for i in range(len(marks)):
            mark = marks[-i-1]
            if mark is common.ALL_ZERO:
                break
            elif mark is common.ALL_NOT_ZERO:
                moves[-i-1] = -1
                step += 1
            elif mark is common.MIX_ZERO:
                moves[-i-1] = step
        return moves

    def __get_blocks_from_id(self, indexes):
        blocks = []  # 存放本行对应的 block
        all_blocks = self.sprites()
        for block in all_blocks:
            if block.get_id() in indexes:
                blocks.append(block)
        return blocks

    def full(self):
        """Return True if blocks touch the top of game_zone.
        """
        return self._full

if __name__ == '__main__':
    pass
