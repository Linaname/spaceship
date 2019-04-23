import time
import curses
import random
import animations


TIC_TIMEOUT = 0.1

'''
def draw(canvas):
    row, column = (5, 20)
    star_blink_cycle = [
        (curses.A_DIM, 2),
        (curses.A_NORMAL, 0.3),
        (curses.A_BOLD, 0.5),
        (curses.A_NORMAL, 0.3)
    ]
    curses.curs_set(False)
    canvas.border()
    while True:
      for mode, delay in star_blink_cycle:
        canvas.addstr(row, column, '*', mode)
        canvas.refresh()
        time.sleep(delay)
'''


def draw(canvas):
    n = 100
    max_y, max_x = canvas.getmaxyx()
    coroutines = []
    # coroutines.append(animations.fire(canvas, max_y // 2, max_x // 2))
    canvas.nodelay(True)
    curses.curs_set(False)
    for i in range(n):
        row = random.randint(1, max_y - 2)
        column = random.randint(1, max_x - 2)
        symbol = random.choice('+*.:')
        initial_state = random.randint(0, 30)
        star = animations.blink(canvas, row, column, symbol, initial_state)
        coroutines.append(star)
    coroutines.append(animations.animate_spaceship(
        canvas,
        max_y//2-4,
        max_x//2-1,
    ))
    while True:
        awaited_coroutines = set()
        for i, cor in enumerate(coroutines):
            try:
                cor.send(None)
            except StopIteration as e:
                awaited_coroutines.add(i)
        canvas.border()
        canvas.refresh()
        for i in awaited_coroutines:
            del coroutines[i]
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
