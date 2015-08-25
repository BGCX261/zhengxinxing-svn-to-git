#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pygame
import random

SIDE_LENGTH  = 23 # 小方块的边像素点数，每次移动这么多
ROW = 19 # 主游戏界面的方块行数
COL = 14 # 主游戏界面的方块列数
FRAME_PER_SECOND = 20 # 每秒帧数
ALL_ZERO = 0  # 用于 check_list() 函数的输出
ALL_NOT_ZERO = 1 # 用于 check_list() 函数的输出
MIX_ZERO = 2 # 用于 check_list() 函数的输出

def load_image(name, colorkey=None, alpha=False):
    # 本项目所有的图片文件都放在 data 目录下
    fullname = os.path.join('data', name)

    ## 企图加载图片
    try:
        image = pygame.image.load(fullname)
    except pygame.error , msg:
        print 'Cannot load image:', fullname
        raise SystemExit, msg

    ## 进行格式转换，以便提高后期图片处理速度
    if alpha :
        # 如果打算使用 alpha 格式的图片，就这么来做
        # alpha是干嘛用的，现在我还不知道 :-)
        image = image.convert_alpha()
    else:
        image = image.convert()

    ## 设置图片的透明样式
    ## colorkey是用于标识某一种颜色，该颜色将会被透明化处理
    if colorkey is not None:
        if colorkey is -1:
            # 取出最左上角那个像素点的颜色，作为 colorkey
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey)

    return image


def load_sound(name):
    ## 定义一个空的 Sound 对象，用于没有声音的时候
    class DummySound:
        def play(): pass

    if not pygame.mixer: return DummySound

    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
        return sound
    except pygame.error, msg:
        # 对于没有声音，只是作为“警告”处理
        print 'Warning: cannot load sound', fullname

    return DummySound


def check_list(the_list):
    """Check a list to see if the elements are zero or not.

    Return 0 for all zero,  1 for all not zero,  2 for others.
    """
    zero_list = [0] * len(the_list)
    if zero_list == the_list:
        return ALL_ZERO

    for element in the_list:
        if element is 0:
            return MIX_ZERO

    return ALL_NOT_ZERO

def get_coordinates(zone, block):
    """Get the block coordinates in zone .

    Return a tuple like (x, y)
    """
    x, y = block.get_rect().topleft
    a = (y - zone.top)/SIDE_LENGTH
    b = (x - zone.left)/SIDE_LENGTH
    return (a, b)

def random_int(max_int):
    """Return 1 - max_int interger randomly,  max_int must be integer.
    """
    num = random.random()
    num = int(round((num * 100) % max_int)) + 1
    if num == max_int + 1:
        num = 1
    return num

if __name__ == '__main__':
    sum = [0] * 22
    for i in range(1000):
        a = random_int(22)
        #print a
        sum[a-1] += 1
    print sum
