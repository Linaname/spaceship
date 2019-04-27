import time
import curses
import random
import animations
import curses_tools

TIC_TIMEOUT = 0.1
GARBAGE_FRAME_FILENAMES = ('duck.txt', 'hubble.txt', 'lamp.txt',
                           'trash_large.txt', 'trash_small.txt',
                           'trash_xl.txt')


def draw(canvas):
    n = 100
    max_y, max_x = canvas.getmaxyx()
    coroutines = []
    canvas.nodelay(True)
    curses.curs_set(False)
    border_width = 1
    spaceship_width, spaceship_height = animations.get_spaceship_size()
    for i in range(n):
        row = random.randint(border_width, max_y - border_width - 1)
        column = random.randint(border_width, max_x - border_width - 1)
        symbol = random.choice('+*.:')
        initial_state = random.randint(0, 30)
        star = animations.blink(canvas, row, column, symbol, initial_state)
        coroutines.append(star)
    garbage_frames = curses_tools.load_frames(GARBAGE_FRAME_FILENAMES)
    garbage_coroutine = animations.fly_garbage(canvas, random.randint(0, max_x-1), random.choice(garbage_frames))
    coroutines.append(garbage_coroutine)
    spaceship_coroutine = animations.animate_spaceship(
        canvas,
        (max_y - spaceship_height)//2,
        (max_x - spaceship_width)//2,
    )
    coroutines.append(spaceship_coroutine)
    while True:
        exhausted_coroutines = set()
        for cor in coroutines:
            try:
                cor.send(None)
            except StopIteration as e:
                exhausted_coroutines.add(cor)
        canvas.border()
        canvas.refresh()
        coroutines = [cor for cor in coroutines
                      if cor not in exhausted_coroutines]
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
