import pygame
from copy import deepcopy
from random import choice
from random import randint
import pygame_menu
import ai


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


def bot(TILE, W, H, clock, FPS, screen, bot_user, menu):
    sc = pygame.display.set_mode((1600, 1000))
    score_1, score_2 = 0, 0
    scores = {0:0, 1:100, 2:300, 3:700, 4:1500}
    lines = 0

    anim_count_1, anim_count_2, anim_limit_1, anim_limit_2 = 0, 0, 2000, 2000
    anim_speed_1, anim_speed_2 = 60, 60
    #first grid
    grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(1, W+1) for y in range(1, H+1)]
    #second grid
    grid_2 = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W+6, 2*W+6) for y in range(1, H+1)]
    
    figures_pos = [[(0, 1), (-1, 1), (1, 1), (2, 1)],
                [(1, 0), (0, 0), (0, 1), (1, 1)],
                [(0, 1), (0, 2), (1, 1), (1, 0)],
                [(1, 1), (0, 1), (1, 2), (0, 0)],
                [(1, 1), (1, 0), (1, 2), (0, 0)],
                [(1, 1), (1, 0), (1, 2), (2, 0)],
                [(1, 1), (1, 0), (1, 2), (0, 1)]]

    figures = [[pygame.Rect(x + (W+1) // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
    figures_2 = [[pygame.Rect(x + W+10, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
    figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
    
    figure = deepcopy(choice(figures))
    figure_2 = deepcopy(choice(figures_2))
    field_1 = [[0 for i in range(W+1)] for j in range(H+1)]
    field_2 = [[0 for i in range(2*W+7)] for j in range(H+1)]
    flag, input, lock = 0, 0, 0


    while True:
        rotate_1, rotate_2 = False, False
        dx_1 = 0
        dx_2 = 0
        screen.fill(pygame.Color('black'))
        #control first
        for event in list(pygame.event.get()) + ai.run_ai(
            field_1, figure, W, H):
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
                if bot_user == 0:
                #control second
                    if event.key == pygame.K_a:
                        dx_2 = -1
                    if event.key == pygame.K_d:
                        dx_2 = 1
                    if event.key == pygame.K_s:
                        anim_limit_2 = 100
                    if event.key == pygame.K_w:
                        rotate_2 = True
        
        if bot_user == 1:
            if input % 51 == 0:
                temp = randint(0, 20)
                if lock == 1:
                    temp = -1
            else:
                temp = -1
            if temp in [0, 1, 19, 20]:
                dx_2 = -1
            if temp in [5, 2, 3, 18]:
                dx_2 = 1
            if temp in [4]:
                anim_limit_2 = 100
            if temp in [6, 7, 16, 17]:
                rotate_2 = True
            if temp in [8, 9, 10, 11, 12, 13, 14, 15]:
                pass
            input += 1
        #move x
        figure_old_1 = deepcopy(figure)
        for i in range(4):
            figure[i].x += dx_1
            if not check_border(figure, i, W, H, field_1):
                figure = deepcopy(figure_old_1)
                anim_limit_1 = 2000
                break

        ai.get_dx(figure[2].x)
        figure_old_2 = deepcopy(figure_2)
        for i in range(4):
            figure_2[i].x += dx_2
            if not check_border(figure_2, i, W+15, H, field_2):
                figure_2 = deepcopy(figure_old_2)
                anim_limit_2 = 2000
                break
        #move y
        anim_count_1 += anim_speed_1
        anim_count_2 += anim_speed_2
        if anim_count_1 > anim_limit_1:
            anim_count_1 = 0
            figure_old_1 = deepcopy(figure)
            for i in range(4):
                figure[i].y += 1
                if check_border(figure, i, W, H, field_1) == 1:
                    for i in range(4):
                        field_1[figure_old_1[i].y][figure_old_1[i].x] = pygame.Color('white')
                    figure = deepcopy(choice(figures))
                    anim_limit_1 = 2000
                    break
                elif check_border(figure, i, W, H, field_1) == 0:
                    figure = deepcopy(figure_old_1)
        if anim_count_2 > anim_limit_2:
            anim_count_2 = 0
            figure_old_2 = deepcopy(figure_2)
            for i in range(4):
                figure_2[i].y += 1
                if check_border(figure_2, i, W+15, H, field_2) == 1:
                    for i in range(4):
                        try:
                            field_2[figure_old_2[i].y][figure_old_2[i].x] = pygame.Color('white')
                        except:
                            pass
                    figure_2 = deepcopy(choice(figures_2))
                    anim_limit_2 = 2000
                    break
                elif check_border(figure_2, i, W+15, H, field_2) == 0:
                    figure_2 = deepcopy(figure_old_2)
                    break
        #wrap/rotate
        rotate(rotate_1, W, H, field_1, figure)
        rotate(rotate_2, W+15, H, field_2, figure_2)
        #check lines
        line = H
        lines = 0
        for row in range(H, -1, -1):
            count = 0
            for i in range(1, W+1):
                if field_1[row][i]:
                    count += 1
                field_1[line][i] = field_1[row][i]
            if count < W:
                line -= 1
            else:
                anim_speed_1 += 5
                lines += 1
        score_1 += scores[lines]

        lines = 0
        line = H
        for row in range(H, -1, -1):
            count = 0
            for i in range(1, W+1):
                i += 15
                if field_2[row][i]:
                    count += 1
                field_2[line][i] = field_2[row][i]
            if count < W:
                line -= 1
            else:
                anim_speed_2 += 5
                lines += 1

        score_2 += scores[lines]

        #draw grid
        [pygame.draw.rect(screen, (40, 40, 40), i_rect, 1) for i_rect in grid]
        #draw second grid
        [pygame.draw.rect(screen, (40, 40, 40), i_rect, 1) for i_rect in grid_2]
        #draw figure
        for i in range(4):
            figure_rect.x = figure[i].x * TILE
            figure_rect.y = figure[i].y * TILE
            pygame.draw.rect(screen, pygame.Color('white'), figure_rect)

            figure_rect.x = figure_2[i].x * TILE
            figure_rect.y = figure_2[i].y * TILE
            pygame.draw.rect(screen, pygame.Color('white'), figure_rect)
        #draw field
        for y, raw in enumerate(field_1):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * TILE, y * TILE
                    pygame.draw.rect(screen, col, figure_rect)

        for y, raw in enumerate(field_2):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * TILE, y * TILE
                    pygame.draw.rect(screen, col, figure_rect)

        font = pygame.font.SysFont(None, 68)
        title_tetris = font.render('TETRIS', True, pygame.Color('white'))
        title_score = font.render('SCORE:', True, pygame.Color('white'))
        result_score_1 = font.render(str(score_1), True, pygame.Color('white'))
        result_score_2 = font.render(str(score_2), True, pygame.Color('white'))

        sc.blit(title_tetris, (510, 50))
        sc.blit(title_tetris, (1180, 50))

        sc.blit(title_score, (510, 800))
        sc.blit(title_score, (1180, 800))

        sc.blit(result_score_1, (510, 850))
        sc.blit(result_score_2, (1180, 850))

        #game over
        for i in range(W+1):
            if field_1[1][i]:
                field_1 = [[0 for i in range(W+1)] for j in range(H+1)]
                anim_count_1, anim_speed_1, anim_limit_1 = 0, 0, 0
                pygame.display.flip()
                flag += 1
            
        
        for i in range(2*W+7-11, 2*W+7):
            if field_2[1][i]:
                field_2 = [[0 for i in range(2*W+7)] for j in range(H+1)]
                anim_count_2, anim_speed_2, anim_limit_2 = 0, 0, 0
                pygame.display.flip()
                flag += 1
                lock = 1

        if flag == 2:
            if score_1 > score_2:
                result = "Bot 1 WIN"
            elif score_1 < score_2:
                if bot_user == 1:
                    result = "Bot 2 WIN"
                if bot_user == 0:
                    result = "Player 2 WIN"
            elif score_1 == score_2:
                result = "DRAW"

            screen.fill(pygame.Color('black'))
            title_result = font.render(result, True, pygame.Color('white'))
            sc.blit(title_result, (800, 500))

        pygame.display.flip()
        clock.tick(FPS)


def main():
    pygame.init()
    clock = pygame.time.Clock()

    RES = 1600, 1000
    screen = pygame.display.set_mode(RES)
    W, H = 10, 20 
    TILE = 45
    FPS = 60
    menu = pygame_menu.Menu('Welcome', 400, 310)

    bot(TILE, W, H, clock, FPS, screen, 0, menu)


if __name__=='__main__':
    main()