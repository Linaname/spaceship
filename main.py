import time
import curses
import random
import animations
import curses_tools
import asyncio
import config
import game_state
from game_scenario import get_garbage_delay_tics, PHRASES


async def fill_orbit_with_garbage(canvas):
    garbage_frames = curses_tools.load_frames(config.GARBAGE_FRAMES_DIR)
    max_y, max_x = canvas.getmaxyx()
    while True:
        garbage_delay = get_garbage_delay_tics(game_state.current_year)
        if garbage_delay is None:
            await asyncio.sleep(0)
            continue
        await sleep(get_garbage_delay_tics(game_state.current_year))
        frame = random.choice(garbage_frames)
        frame_height, frame_width = curses_tools.get_frame_size(frame)
        column = random.randint(0, max_x - frame_width)
        garbage_coroutine = animations.fly_garbage(canvas, column, frame)
        game_state.coroutines.append(garbage_coroutine)


async def sleep(tics=1):
    for i in range(tics):
        await asyncio.sleep(0)


def draw(canvas):
    n_stars = 100
    max_y, max_x = canvas.getmaxyx()
    canvas.nodelay(True)
    curses.curs_set(False)
    border_width = 1
    spaceship_width, spaceship_height = animations.get_spaceship_size()
    for i in range(n_stars):
        row = random.randint(border_width, max_y - border_width - 1)
        column = random.randint(border_width, max_x - border_width - 1)
        symbol = random.choice('+*.:')
        initial_state = random.randint(0, 30)
        star = animations.blink(canvas, row, column, symbol, initial_state)
        game_state.coroutines.append(star)
    spaceship_animation = animations.animate_spaceship(canvas)
    spaceship_drawing = animations.run_spaceship(canvas,
                                                 (max_y-spaceship_width)//2,
                                                 (max_x-spaceship_height)//2)
    game_state.coroutines.append(spaceship_animation)
    game_state.coroutines.append(spaceship_drawing)
    game_state.coroutines.append(fill_orbit_with_garbage(canvas))
    info_subwin_size = (1, 62)
    message_template = 'Year: {} {:<50}'
    info_subwin = canvas.derwin(*info_subwin_size, border_width, border_width)
    try:
        while True:
            exhausted_coroutines = set()
            for cor in game_state.coroutines:
                try:
                    cor.send(None)
                except StopIteration as e:
                    exhausted_coroutines.add(cor)
            canvas.border()
            year = int(game_state.current_year)
            message = message_template.format(year, PHRASES.get(year, ''))
            info_subwin.addstr(0, 0, message)
            canvas.refresh()
            game_state.coroutines = [cor for cor in game_state.coroutines
                                 if cor not in exhausted_coroutines]
            time.sleep(config.TIC_TIMEOUT)
            game_state.current_year += 1/config.TICS_PER_YEAR
    except KeyboardInterrupt:
        exit()


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
