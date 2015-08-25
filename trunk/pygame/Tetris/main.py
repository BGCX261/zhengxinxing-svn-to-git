#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import pygame
import common
from pygame.locals import *
from block import Block
from unit import Unit
from bottoms import Bottoms

def main():
    # 将游戏运行环境设置到正确的目录下
    if os.path.dirname( __file__ ):
        os.chdir( os.path.dirname(__file__) )

    # 初始化
    pygame.init()
    screen_size = (common.SIDE_LENGTH * 21, common.SIDE_LENGTH * 23)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_icon(common.load_image('block_icon.GIF'))
    pygame.display.set_caption('Tetris, by zhengxinxing@gmail.com, 2008')# 这儿如何实现中文显示？

    # background
    background = pygame.Surface(screen.get_size()).convert()
    background.fill((0,0,0))
    background.blit(common.load_image('border.PNG', -1).convert(), (0,0))
    screen.blit(background, (0,0))
    pygame.display.flip()

    # game objects
    clock = pygame.time.Clock()
    game_zone = (14, 80, common.SIDE_LENGTH*common.COL, common.SIDE_LENGTH*common.ROW)
    pygame.time.set_timer(USEREVENT, 1000)
    unit = Unit(game_zone) # 本句用于测试
    unit.set_pos(game_zone[0]+game_zone[2]/2, game_zone[1])
    blocks = pygame.sprite.RenderUpdates() # 落下的方块们
    blocks.add(unit.blocks())
    bottoms = Bottoms(game_zone) # 已落地的方块们

    pause = 0

    # main loop
    while 1:
        clock.tick(common.FRAME_PER_SECOND)

        # 按 p 键将暂停游戏，再按则恢复游戏
        while pause:
            for e in pygame.event.get():
                if e.type == QUIT:
                    return
                elif e.type == KEYDOWN and e.key == K_ESCAPE:
                    return
                elif e.type == KEYDOWN and e.key == K_p:
                    pause = 0

        if unit.isBottomed():
            for b in blocks:
                bottoms.my_add(b)
                blocks.remove(b)

            bottoms.check_linefull()

            # 新生成一个方块
            # 新出来的方块，需要先检查位置，如果没位置出来，则需要结束游戏？
            unit = Unit(game_zone)
            unit.set_pos(game_zone[0]+game_zone[2]/2, game_zone[1])
            blocks.add(unit.blocks())

        #检查方块顶格了没有，如果顶格了，就结束游戏
        if bottoms.full():
            pass

        for e in pygame.event.get():
            if e.type == QUIT:
                return
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                return
            elif e.type == USEREVENT:
                unit.move_down(bottoms.sprites())
            elif e.type == KEYDOWN and e.key == K_j:
                unit.spin_clockwise(bottoms)
            elif e.type == KEYDOWN and e.key == K_k:
                unit.spin_anticlockwise()
            elif e.type == KEYDOWN and e.key == K_0:
                bottoms.empty()
            elif e.type == KEYDOWN and e.key == K_p:
                #pause the game
                pause = 1

        keystates = pygame.key.get_pressed()
        if keystates[K_a]:
            unit.move_left(bottoms)
        elif keystates[K_d]:
            unit.move_right(bottoms)
        elif keystates[K_s]:
            unit.move_down(bottoms.sprites())
        elif keystates[K_j]:
            #unit.spin_clockwise()
            pass
        elif keystates[K_k]:
            #unit.spin_anticlockwise()
            pass


        blocks.update()
        bottoms.update()

        screen.blit(background, (0,0))# 这句将来要改成局部blit，以便加强效率
        blocks.draw(screen)
        bottoms.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()
