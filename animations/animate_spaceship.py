from curses_tools import draw_frame, read_controls, get_max_frame_size
import asyncio
import itertools
import os


FRAMES_LIST = []
DEFAULT_FRAMES_DIR = 'frames'
DEFAULT_FRAME_FILENAMES = ('rocket_frame_1.txt', 'rocket_frame_2.txt')


def load_frames(frame_filenames=DEFAULT_FRAME_FILENAMES,
                frames_dir=DEFAULT_FRAMES_DIR):
    frames_list = []
    paths_list = [os.path.join(frames_dir, filename) for filename in
                  frame_filenames]
    for path in paths_list:
        with open(path, 'r') as f:
            frame = f.read()
        frames_list.append(frame)
    return frames_list


async def animate_spaceship(canvas, row, column, border_width=1):
    frames_list = load_frames()
    canvas_height, canvas_width = canvas.getmaxyx()
    max_frame_height, max_frame_width = get_spaceship_size()
    min_row = border_width
    min_column = border_width
    max_row = canvas_height - max_frame_height - border_width
    max_column = canvas_width - max_frame_width - border_width
    previous_frame = ''
    for frame in itertools.cycle(frames_list):
        draw_frame(canvas, row, column, previous_frame, negative=True)
        d_row, d_column, _ = read_controls(canvas)
        new_row, new_column = row + d_row, column + d_column
        if min_row <= new_row <= max_row:
            row = new_row
        if min_column <= new_column <= max_column:
            column = new_column
        draw_frame(canvas, row, column, frame)
        previous_frame = frame
        await asyncio.sleep(0)


def get_spaceship_size():
    frames_list = load_frames()
    return get_max_frame_size(frames_list)
