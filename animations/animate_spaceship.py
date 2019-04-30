from curses_tools import draw_frame, read_controls, get_max_frame_size, load_frames
import config
import game_state
from . import fire
from .game_over import game_over
import physics
import asyncio
import itertools


async def animate_spaceship(canvas,
                            frames_dir=config.SPACESHIP_FRAMES_DIR):
    frames_list = load_frames(frames_dir)
    for frame in itertools.cycle(frames_list):
        game_state.spaceship_frame= frame
        await asyncio.sleep(0)


async def run_spaceship(canvas, row, column,
                        border_width=1,
                        row_speed=0,
                        column_speed=0,
                        gun_position=(0, 2),
                        frames_dir=config.SPACESHIP_FRAMES_DIR):
    previous_frame = ''
    canvas_height, canvas_width = canvas.getmaxyx()
    max_frame_height, max_frame_width = get_spaceship_size(frames_dir)
    min_row = border_width
    min_column = border_width
    max_row = canvas_height - max_frame_height - border_width
    max_column = canvas_width - max_frame_width - border_width
    while True:
        draw_frame(canvas, row, column, previous_frame, negative=True)
        d_row, d_column, shot = read_controls(canvas)
        row_speed, column_speed = physics.update_speed(row_speed, column_speed,
                                                       d_row, d_column)
        new_row, new_column = row + row_speed, column + column_speed
        row = min(max_row, max(min_row, new_row))
        column = min(max_column, max(min_column, new_column))
        if shot and game_state.current_year >= config.PLASMA_GUN_YEAR:
            d_y, d_x = gun_position
            game_state.coroutines.append(fire(canvas, int(row + d_y), int(column + d_x)))
        spaceship_height, spaceship_width = get_max_frame_size([game_state.spaceship_frame])
        for obstacle in game_state.obstacles:
            if obstacle.has_collision(row, column, spaceship_height, spaceship_width):
                game_state.coroutines.append(game_over(canvas))
                return
        draw_frame(canvas, row, column, game_state.spaceship_frame)
        previous_frame = game_state.spaceship_frame
        await asyncio.sleep(0)


def get_spaceship_size(frames_dir=config.SPACESHIP_FRAMES_DIR):
    frames_list = load_frames(frames_dir)
    return get_max_frame_size(frames_list)
