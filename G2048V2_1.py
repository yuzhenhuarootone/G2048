import os
import time
from turtle import up, down, textinput, goto, color, write, update, clear, ontimer, onkey, setup, hideturtle, tracer, listen, done
from gamebase import add_num, is_move_possible, make_move, rectangle, line

import numpy as np

# numpy用来处理二维数组，os用来管理排行榜,time读取时间，turtle绘制画面

dirname, basename = os.path.split(__file__)
BANG = dirname + '/paiming.txt'
# 排行榜的文件名

# 游戏场地长4，宽4，面积16
HEIGHT = 4
WIDTH = 4
FIELD_SIZE = HEIGHT * WIDTH

# 生成初始场地，数字0代表空
ground = np.zeros((WIDTH, HEIGHT), dtype=np.int)


# 定义方向数组
LEFT = np.array((0, -1))
RIGHT = np.array((0, 1))
UP = np.array((-1, 0))
DOWN = np.array((1, 0))

mov = [LEFT, RIGHT, UP, DOWN]

# 初始化场地
ground[1, 1] = 4
ground[1, 2] = 2
ground[2, 2] = 2
ground[1, 3] = 2

# 将ground中的索引与screen中坐标对应
ground_indexes = [(x, y) for x in range(4) for y in range(4)]
ground_coordinate = [(x, y) for y in [195 - n / 8 * 380 for n in (1, 3, 5, 7)]
                     for x in [i / 8 * 380 - 345 for i in (1, 3, 5, 7)]]
idx_to_coo = {ground_indexes[i]: ground_coordinate[i]
              for i in range(len(ground_coordinate))}

# 记录每一个数字的颜色，应该不会有人超过8192吧
num_color = {2: 'greenyellow', 4: 'deepskyblue', 8: 'orangered', 16: 'tan', 32: 'limegreen', 64: 'violet',
             128: 'pink', 256: 'grey', 512: 'gold', 1024: 'blue', 2048: 'red', 4096: 'midnightblue', 8192: 'darkred'}

# changed为TRUE则表示ground发生了改变，此时刷新屏幕
changed = True


def load_base():
    # 读取排行榜
    with open(BANG, 'r', encoding='utf-8') as BB:
        text = BB.readlines()[0:10]
        text = ''.join(text)
        return text


def save_base():
    # 向排行榜中写入记录
    player_name = textinput('走无可走', '请输入你的名字！（短一些）')
    try:
        while len(player_name) > 5 or (len(player_name) > 3 and is_contains_chinese(player_name)):
            player_name = textinput('走无可走', '请输入你的名字！（短一些）')
        if not len(player_name) : player_name = '无名氏'
    except:
        player_name = '无名氏'
    with open(BANG, 'a+', encoding='utf-8') as BB:
        localtime = time.strftime("%Y-%m-%d--%H:%M:%S", time.localtime())
        BB.write(f'{player_name}\t{np.sum(ground)}\t{localtime}\n')
    return


def is_contains_chinese(strs):
    #检验是否含有中文字符
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

def reset_base():
    # 整理排行榜，进行排序
    with open(BANG, 'r', encoding='utf-8') as BB:
        record = BB.readlines()
    with open(BANG, 'w', encoding='utf-8') as BB:
        head = record.pop(0)
        BB.write(head)
        a_list = [i.split('\t') for i in record]
        a_list.sort(key=lambda x: int(x[1]), reverse=True)
        record = ['\t'.join(a_list[i]) for i in range(len(a_list))]
        for i in record[0:21]:
            BB.write(i)


def show_a_num(x, y, num, pencolor='black'):
    # 画出一个数字
    up()
    goto(x, y)
    color(pencolor)
    font_zise = 32
    write(num, align='center', font=('Arial', font_zise, 'bold'))


def show_nums():
    # 画出所有数字
    for hang in range(WIDTH):
        for lei in range(HEIGHT):
            x, y = idx_to_coo[(hang, lei)]
            if ground[hang][lei]:
                try:
                    rectangle(x-47.5, y-47.5, 95, 95, num_color[ground[hang][lei]])
                except:
                    pass
            show_a_num(x, y-22, ground[hang][lei], 'white')
    up()


def show_gird():
    # 画出网格线
    for dow in [(x, -185) for x in [95 * i - 345 for i in range(1, 4)]]:
        x, y = dow
        line(x, y, x, y+380, 3)
    for lef in [(-345, y) for y in [195 - 95 * i for i in range(1, 4)]]:
        x, y = lef
        line(x, y, x+380, y, 3)
    up()


def show_work():
    # 画出非游戏区
    up()
    goto(200, 165)
    color('black')
    write('使用wasd移动', align='center', font=('Arial Nova', 28, 'bold'))
    goto(200, 120)
    color('black')
    write('按B键重新开始', align='center', font=('Arial Nova', 24, 'normal'))
    goto(200, 30)
    color('black')
    write('排行榜', align='center', font=('Arial Nova', 26, 'bold'))
    line(50, 25, 350, 25, 2, 'black')
    up()
    goto(200, 90)
    color('black')
    write(f'当前分数是{np.sum(ground)}', align='center',
          font=('Arial Nova', 24, 'normal'))
    goto(200, -170)
    color('black')
    write(load_base(), align='center', font=('Arial Nova', 12, 'normal'))
    up()
    update()


def new_game():
    # 重置游戏
    global ground, changed
    ground = np.zeros((WIDTH, HEIGHT), dtype=np.int)
    ground[1, 1] = 4
    ground[1, 2] = 2
    ground[2, 2] = 2
    ground[1, 3] = 2
    changed = True
    onkey(lambda: change(0), 'a')
    onkey(lambda: change(1), 'd')
    onkey(lambda: change(2), 'w')
    onkey(lambda: change(3), 's')


def draw():
    # 绘制
    clear()
    rectangle(-370, -210, 730, 430)
    rectangle(-360, -200, 710, 410, 'white')
    rectangle(-345, -185, 380, 380)
    line(50, 210, 50, -200, 2, 'black')
    show_work()
    show_nums()
    show_gird()
    update()


def change(idx):
    # 更新ground
    global changed
    move = mov[idx]
    changed = True
    if is_move_possible(ground, move):
        # 如果可以移动，则移动，添加新数字
        make_move(ground, move)
        add_num(ground)
    elif not any([is_move_possible(ground, mov[i]) for i in range(4)]):
        # 如果四个方向都不能移动
        gameover()
    if np.max(ground) > 10000:
        gameover()
    

def gameover():
    # 游戏结束
    global changed
    onkey(None, 'a')
    onkey(None, 'd')
    onkey(None, 'w')
    onkey(None, 's')
    draw()
    changed = False
    save_base()
    reset_base()
    draw()
    listen()

def gameloop():
    # 主循环
    global changed
    if changed:
        changed = False
        draw()
    ontimer(gameloop, 70)


if __name__ == "__main__":
    if not os.path.exists(BANG):
        # 找不到排行榜文件就新建一个
        with open(BANG, 'w', encoding='utf-8') as bang:
            bang.write('姓名\t分数\t时间\n')
            bang.write('余振华\t1610\t2020-05-04--20:53:03\n')
    setup(740, 440, 0, 0)
    hideturtle()
    tracer(False)
    listen()
    new_game()
    onkey(new_game, 'b')
    gameloop()
    done()

# 20180447