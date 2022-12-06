import pygame
from copy import deepcopy
from random import choice
from database import input_record
from test import check_nickname


def check_border(figure, i, W, H, field):
    if figure[i].x < (W-9) or figure[i].x > W:
        return 0
    if W > 10:
        if figure[i].y > H or field[figure[i].y][figure[i].x]:
            return 1
    else:
        if figure[i].y > H or field[figure[i].y][figure[i].x]:
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


def tetris_classic(TILE, W, H, clock, FPS, screen, menu):
    sc = pygame.display.set_mode((1600, 1000))
    #get name
    font = pygame.font.Font(None, 32)
    input_box = pygame.Rect(500, 500, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    nickname = ''
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        nickname = nickname[:-1]
                    else:
                        nickname += event.unicode
        screen.fill((30, 30, 30))
        # Render the current text.
        txt_surface = font.render(nickname, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        
    #test input nickname
    check_nickname(nickname)
    score = 0
    scores = {0:0, 1:100, 2:300, 3:700, 4:1500}
    lines = 0

    anim_count_1, anim_limit_1 = 0, 2000
    anim_speed_1= 60
    #first grid
    grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(1, W+1) for y in range(1, H+1)]
    
    figures_pos = [[(0, 1), (-1, 1), (1, 1), (2, 1)],
                [(1, 0), (0, 0), (0, 1), (1, 1)],
                [(0, 1), (0, 2), (1, 1), (1, 0)],
                [(1, 1), (0, 1), (1, 2), (0, 0)],
                [(1, 1), (1, 0), (1, 2), (0, 0)],
                [(1, 1), (1, 0), (1, 2), (2, 0)],
                [(1, 1), (1, 0), (1, 2), (0, 1)]]

    figures = [[pygame.Rect(x + (W+1) // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
    figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
    
    figure = deepcopy(choice(figures))
    field = [[0 for i in range(W+1)] for j in range(H+1)]

    flag = 0
    while True:
        rotate_1 = False
        dx_1 = 0
        screen.fill(pygame.Color('black'))
        #control first
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                #menu
                if event.key == pygame.K_ESCAPE:
                    menu.mainloop(screen)
                #control first
                if event.key == pygame.K_LEFT:
                    dx_1 = -1
                if event.key == pygame.K_RIGHT:
                    dx_1 = 1
                if event.key == pygame.K_DOWN:
                    anim_limit_1 = 100
                if event.key == pygame.K_UP:
                    rotate_1 = True
        #move x
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].x += dx_1
            if not check_border(figure, i, W, H, field):
                figure = deepcopy(figure_old)
                anim_limit_1 = 2000
                break
        #move y
        anim_count_1 += anim_speed_1
        if anim_count_1 > anim_limit_1:
            anim_count_1 = 0
            figure_old_1 = deepcopy(figure)
            for i in range(4):
                figure[i].y += 1
                if check_border(figure, i, W, H, field) == 1:
                    for i in range(4):
                        field[figure_old_1[i].y][figure_old_1[i].x] = pygame.Color('white')
                    figure = deepcopy(choice(figures))
                    anim_limit_1 = 2000
                    break
                elif check_border(figure, i, W, H, field) == 0:
                    figure = deepcopy(figure_old_1)
        #wrap/rotate
        rotate(rotate_1, W, H, field, figure)
        #check lines
        line = H
        lines = 0
        for row in range(H, -1, -1):
            count = 0
            for i in range(1, W+1):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < W:
                line -= 1
            else:
                anim_speed_1 += 5
                lines += 1
        score += scores[lines]

        #draw grid
        [pygame.draw.rect(screen, (40, 40, 40), i_rect, 1) for i_rect in grid]
        #draw figure
        for i in range(4):
            figure_rect.x = figure[i].x * TILE
            figure_rect.y = figure[i].y * TILE
            pygame.draw.rect(screen, pygame.Color('white'), figure_rect)
        #draw field
        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * TILE, y * TILE
                    pygame.draw.rect(screen, col, figure_rect)

        font = pygame.font.SysFont(None, 68)
        title_tetris = font.render('TETRIS', True, pygame.Color('white'))
        title_score = font.render('SCORE:', True, pygame.Color('white'))
        result_score = font.render(str(score), True, pygame.Color('white'))

        sc.blit(title_tetris, (510, 50))
        sc.blit(title_score, (510, 800))
        sc.blit(result_score, (510, 850))
        #game over
        for i in range(W+1):
            if field[1][i]:
                flag += 1
                result = "Your score: " + str(score)
                result_score = font.render(str(result), True, pygame.Color('white'))
                screen.fill(pygame.Color('black'))
                sc.blit(result_score, (800, 500))

        if flag == 1:
            input_record(nickname, score)

        pygame.display.flip()
        clock.tick(FPS)


