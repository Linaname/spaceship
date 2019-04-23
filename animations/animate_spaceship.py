from curses_tools import draw_frame, read_controls, get_frame_size
import asyncio
import itertools
import os


def load_frames(paths_list):
    frames_list = []
    for path in paths_list:
        with open(path, 'r') as f:
            frame = f.read()
        frames_list.append(frame)
    return frames_list


async def loop_animation(canvas, row, column, frames_list):
    canvas_height, canwas_width = canvas.getmaxyx()
    frame_height, frame_width = map(max, zip(*map(get_frame_size, frames_list)))
    min_row = 1
    min_column = 1
    max_row = canvas_height - frame_height - 1
    max_column = canwas_width - frame_width - 1
    previous_frame = ''
    for frame in itertools.cycle(frames_list):
        draw_frame(canvas, row, column, previous_frame, negative=True)
        d_row, d_column, _ = read_controls(canvas)
        new_row, new_column = row + d_row, column + d_column
        if (min_row <= new_row <= max_row and
                min_column <= new_column <= max_column):
            row, column = new_row, new_column
        draw_frame(canvas, row, column, frame)
        previous_frame = frame
        await asyncio.sleep(0)


def animate_spaceship(canvas, row, column, frames_dir='frames'):
    frame_filenames = ['rocket_frame_1.txt', 'rocket_frame_2.txt']
    paths_list = [os.path.join(frames_dir, filename) for filename in frame_filenames]
    frames_list = load_frames(paths_list)
    return loop_animation(canvas, row, column, frames_list)
