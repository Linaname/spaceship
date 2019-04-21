from curses_tools import draw_frame, read_controls, get_frame_size
import asyncio
import os


frames_directory = os.path.join(os.path.dirname(__file__), 'frames')

with open(os.path.join(frames_directory, 'rocket_frame_1.txt'), 'r') as f:
    frame_1 = f.read()
with open(os.path.join(frames_directory, 'rocket_frame_2.txt'), 'r') as f:
    frame_2 = f.read()


async def animate_spaceship(canvas, row, column):
    canvas_height, canwas_width = canvas.getmaxyx()
    frame_height, frame_width = map(max, zip(get_frame_size(frame_1),
                                             get_frame_size(frame_2)))
    min_row = 1
    min_column = 1
    max_row = canvas_height - frame_height - 1
    max_column = canwas_width - frame_width -1
    draw_frame(canvas, row, column, frame_1)
    await asyncio.sleep(0)
    while True:
        draw_frame(canvas, row, column, frame_1, negative=True)
        d_row, d_column, _ = read_controls(canvas)
        new_row, new_column = row + d_row, column + d_column
        if (min_row <= new_row <= max_row and
                min_column <= new_column <= max_column):
            row, column = new_row, new_column
        draw_frame(canvas, row, column, frame_2)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame_2, negative=True)
        d_row, d_column, _ = read_controls(canvas)
        new_row, new_column = row + d_row, column + d_column
        if (min_row <= new_row <= max_row and
                min_column <= new_column <= max_column):
            row, column = new_row, new_column
        draw_frame(canvas, row, column, frame_1)
        await asyncio.sleep(0)
