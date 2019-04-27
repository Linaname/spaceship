import time
import curses
import random
import animations
import curses_tools
import asyncio
import config
from game_scenario import get_garbage_delay_tics, PHRASES


async def fill_orbit_with_garbage(canvas):
    garbage_frames = curses_tools.load_frames(config.GARBAGE_FRAMES_DIR)
    max_y, max_x = canvas.getmaxyx()
    while True:
        garbage_delay = get_garbage_delay_tics(config.YEAR)
        if garbage_delay is None:
            await asyncio.sleep(0)
            continue
        await sleep(get_garbage_delay_tics(config.YEAR))
        frame = random.choice(garbage_frames)
        frame_height, frame_width = curses_tools.get_frame_size(frame)
        column = random.randint(0, max_x - frame_width)
        garbage_coroutine = animations.fly_garbage(canvas, column, frame)
        config.COROUTINES.append(garbage_coroutine)


async def sleep(tics=1):
    for i in range(tics):
        await asyncio.sleep(0)


def draw(canvas):
    n = 100
    max_y, max_x = canvas.getmaxyx()
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
        config.COROUTINES.append(star)
    spaceship_animation = animations.animate_spaceship(canvas)
    spaceship_drawing = animations.run_spaceship(canvas,
                                                 (max_y-spaceship_width)//2,
                                                 (max_x-spaceship_height)//2)
    config.COROUTINES.append(spaceship_animation)
    config.COROUTINES.append(spaceship_drawing)
    config.COROUTINES.append(fill_orbit_with_garbage(canvas))
    info_subwin_size = (1, 62)
    message_template = 'Year: {} {:<50}'
    info_subwin = canvas.derwin(*info_subwin_size, border_width, border_width)
    while True:
        exhausted_coroutines = set()
        for cor in config.COROUTINES:
            try:
                cor.send(None)
            except StopIteration as e:
                exhausted_coroutines.add(cor)
        canvas.border()
        year = int(config.YEAR)
        message = message_template.format(year, PHRASES.get(year, ''))
        info_subwin.addstr(0, 0, message)
        canvas.refresh()
        config.COROUTINES = [cor for cor in config.COROUTINES
                             if cor not in exhausted_coroutines]
        time.sleep(config.TIC_TIMEOUT)
        config.YEAR += 1/config.TICS_PER_YEAR


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
