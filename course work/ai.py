import pygame
from copy import deepcopy

class Event():
    type = None
    key = None

    def __init__(self, type, key):
        self.type = type
        self.key = key


def check_border(figure, i, W, H, field):
    if figure[i].x < (W-9) or figure[i].x > W:
        return 0
    if W > 10:
        if figure[i].y > H-1 or field[figure[i].y][figure[i].x]:
            return 1
    else:
        if figure[i].y > H-1 or field[figure[i].y][figure[i].x]:
            return 1
    return 2


def rotate(rotate_1, W, H, field_1, figure):
    center_1 = figure[0]
    figure_old_1 = deepcopy(figure)
    if rotate_1:
        for i in range(4):
            x = figure[i].y - center_1.y
            y = figure[i].x - center_1.x
            figure[i].x = center_1.x - x
            figure[i].y = center_1.y + y
            if not check_border(figure, i, W, H, field_1):
                figure = deepcopy(figure_old_1)
                break


def add_figure(figure, field_1, W, H):
    for i in range(4):
        figure[i].y = 0
    while True:
        for i in range(4):
            figure[i].y += 1
        if check_border(figure, i, W, H, field_1) == 1:
            for j in range(4):
                field_1[figure[j].y][figure[j].x] = pygame.Color('white')
            break




def get_height(field, W, H, figure):
    height = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    temp_height = 0
    for i in field:
        temp = 0
        for j in i:
            if j != 0:
                if height[temp] == 0:
                    height[temp] = H - temp_height + 1
            temp += 1
        temp_height += 1
    return height


def simulation(field, W, H, figure):
    copy_figure = deepcopy(figure)
    temp_field = deepcopy(field)
    new = []
    for i in range(4):
        rotate(True, W, H, temp_field, copy_figure)
        add_figure(copy_figure, temp_field, W, H)
        temp = get_height(temp_field, W, H, copy_figure)
        temp = temp[1:]
        new.append(sum(temp))
        temp_field = deepcopy(field)
    temp = min(new)
    rot_n = new.index(temp)
    return rot_n


def best_position(x, height: list, field, W, H, figure):
    e = []
    for i in range(simulation(field, W, H, figure)):
        e.append(e.append(Event(pygame.KEYDOWN, pygame.K_UP)))
    height = height[1:]
    new_x = min(height)
    find_x = height.index(new_x)
    e = []
    if find_x == x-1:
        e.append(Event(pygame.KEYDOWN, pygame.K_DOWN))
    if find_x > x:
        e.append(Event(pygame.KEYDOWN, pygame.K_RIGHT))
    elif find_x < x:
        e.append(Event(pygame.KEYDOWN, pygame.K_LEFT))
    return e

dx = 0
def get_dx(x):
    global dx
    dx = x - 1


counter = 0
def run_ai(field, figure, width, heig):
    height = get_height(field, width, heig, figure)
    global dx
    global counter
    counter += 1
    e = best_position(dx, height, field, width, heig, figure)
    return e