import numpy as np
import os
import random
import time
from turtle import *

# 定义场地
HEIGHT = 4
WIDTH = 4
FIELD_SIZE = HEIGHT * WIDTH
# 创建场地
ground = np.zeros((WIDTH, HEIGHT), dtype=np.int)

# 辅助列表，详见num_d函数
stop_list = [0 for i in range(len(ground))]

# 生成新数字时，按顺序从new_num中选取
new_c = 0
new_num = [4, 2, 2, 2]

# 方向变量
LEFT = np.array((0, -1))
RIGHT = np.array((0, 1))
UP = np.array((-1, 0))
DOWN = np.array((1, 0))
# 方向数组
mov = [LEFT, RIGHT, UP, DOWN]


def square(x, y, size, color_name):
    # 以（x，y）为左下顶点，画一个边长为size，颜色为color_name的正方形
    up()
    goto(x, y)
    down()
    color(color_name)
    begin_fill()
    for i in range(4):
        forward(size)
        left(90)
    end_fill()

def rectangle(x, y, width, height, color_name='black'):
    # 以（x，y）为左下顶点，画一个边宽为width，高为height，颜色为color_name的长方形
    up()
    goto(x, y)
    color(color_name)
    begin_fill()
    for i in range(2):
        forward(width)
        left(90)
        forward(height)
        left(90)
    end_fill()

def line(x, y, a, b, line_width=1, pen_color='red'):
    # 画一条从（x，y）到（a，b）的线
    up()
    goto(x, y)
    down()
    width(line_width)
    color(pen_color)
    goto(a, b)

def add_num(ground):  # 产生新的数字，new_c是[4,2,2,2]的索引
    global new_c
    cell_free = False
    while not cell_free:
        num_idx = (random.randint(0, HEIGHT - 1), random.randint(0, WIDTH - 1))
        cell_free = is_cell_free(ground, num_idx)
    ground[num_idx] = new_num[new_c]
    new_c = (new_c + 1) % 4


def make_move(ground_, move):  # 移动，给出场地和方向，移动场地
    global stop_list
    ground_ = array_T0(ground_, move)  # 标准化
    for i in range(len(ground_)):  # 遍历，得到一维数组分别处理
        stop_list = [0 for i in range(len(ground_))]  # 每处理一个新的一维数组，重置stop_list
        ground_[i] = array_move(ground_[i])
    ground_ = array_T1(ground_, move)  # 去标准化


def is_move_possible(groundf, move):  # 是否可以向一个方向移动
    ground_p = groundf.copy()
    make_move(ground_p, move)
    return False if np.all(ground_p == groundf) else True
    # 如果移动后场地与原来一样，则不能移动，注意在numpy中判断两个数组完全相等要加一个all


def num_d(array, idx, stop_list):
    '''场地是一个二维数组，把它按照不同的情况分成四个一维数组，分别处理四个一位数组之后再合并成完整的场地，
    给出一个数组array如[4,2,0,2]，给出一个索引值idx如3，给出一个控制合并的数组stop_list如[1,0,0,0]，
    此函数将array中索引为3的元素向左移动，如果可以合并则合并，直到不能移动，结果是[4,4,0,0]'''
    if stop_list[idx - 1] == 1 or idx == 0 or array[idx] == 0:
        # stop_list[idx - 1] == 1 表示目标位置拒绝合并
        return array
    if not (array[idx - 1] == array[idx] or array[idx - 1] == 0):
        # 如果当前位置与目标位置值不相等，并且目标位置值不为0，结束递归
        return array
    falg = True if array[idx - 1] == array[idx] else False
    # 如果发生一次合并，则本次调用函数结束，stop_list似乎失去意义，但是此函数会连续调用四次，遍历元素，
    # stop_list的意义在于在这四次调用中一个位置只发生一次合并
    array[idx - 1] += array[idx]
    stop_list[idx - 1] = 1 if falg else 0
    array[idx] = 0
    idx -= 1
    return array if falg else num_d(array, idx, stop_list)


def array_move(array):  # 用于处理数组
    global stop_list
    for i in range(len(array)):
        array = num_d(array, i, stop_list)
    return array


def array_T0(groundf, move):  # 将场地化为标准形式，以便遍历后使用array_move处理
    if move[1] == 0:  # 如果上下移动
        groundf = groundf.T  # 转置
        if move[0] == 1:  # 如果向下移动
            groundf = groundf[:, ::-1]  # 倒序
    if move[1] == 1:  # 如果向右移动
        groundf = groundf[:, ::-1]  # 倒序
    return groundf


def array_T1(groundf, move):  # 在处理完之后将场地变成原来的样子
    if move[1] == 1:
        groundf = groundf[:, ::-1]
    if move[1] == 0:
        if move[0] == 1:
            groundf = groundf[:, ::-1].T
        else:
            groundf = groundf.T
    return groundf


def is_cell_free(ground, idx):  # 判断当前位置元素是否为空
    return True if ground[idx] == 0 else False


def input_move():  # 玩家输入方向
    try:  # 输入时直接按回车会报错，索引超过3会报错，如果玩了好长时间，因为按错了导致游戏结束，那非常操蛋
        move = int(input('请输入方向~~'))
        while not move in (0, 1, 2, 3, 8848, 9999):  # 输入8848游戏结束，9999排行榜
            move = int(input('请重新输入~~'))
        return move
    except:
        return input_move()  # 报错就重新输入


def save_base(score):
    name = input('请输入你的名字（短一点）')
    while len(name) > 5:
        name = input('请输入你的名字（短一点）')
    with open('BANG', 'a+', encoding='utf-8') as BB:
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        BB.write(f'{name}\t{score}\t{localtime}\n')
    return
