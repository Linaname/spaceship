import time
import curses
import random
import animations


TIC_TIMEOUT = 0.1


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
    spaceship_coroutine = animations.animate_spaceship(
        canvas,
        (max_y - spaceship_height)//2,
        (max_x - spaceship_width)//2,
    )
    coroutines.append(spaceship_coroutine)
    while True:
        exhausted_coroutines = set()
        for i, cor in enumerate(coroutines):
            try:
                cor.send(None)
            except StopIteration as e:
                exhausted_coroutines.add(i)
        canvas.border()
        canvas.refresh()
        n_coroutines = len(coroutines)
        coroutines = [coroutines[i] for i in range(n_coroutines)
                      if i not in exhausted_coroutines]
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
