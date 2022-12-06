from database import get_record
import pygame_menu
from database import get_record


def table(menu: pygame_menu.Menu, screen, back_menu):
    result = get_record()
    result.reverse()
    number = 0
    for i in result[0:10]:
        number += 1
        row = str(number) + " " + i[0] + " " + str(i[1])
        menu.add.label(row)
    menu.add.button('Back', back_menu)
    menu.mainloop(screen)



if __name__=="__main__":
    table()