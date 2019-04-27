from curses_tools import get_frame_size, draw_frame
import asyncio


async def game_over(canvas):
    with open('frames/game_over.txt') as f:
        frame = f.read()
    canvas_height, canvas_width = canvas.getmaxyx()
    frame_height, frame_width = get_frame_size(frame)
    row = (canvas_height - frame_height)//2
    column = (canvas_width - canvas_height)//2
    while True:
        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
