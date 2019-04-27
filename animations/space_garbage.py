from curses_tools import draw_frame, get_frame_size
from obstacles import Obstacle
import config
import uuid
import asyncio


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    uid = uuid.uuid4()
    rows_size, columns_size = get_frame_size(garbage_frame)
    obstacle = Obstacle(row, column, rows_size, columns_size, uid)
    config.OBSTACLES.append(obstacle)
    try:
        while row < rows_number:
            if obstacle in config.OBSTACLES_IN_LAST_COLLISIONS:
                config.OBSTACLES_IN_LAST_COLLISIONS.remove(obstacle)
                return
            draw_frame(canvas, row, column, garbage_frame)
            await asyncio.sleep(0)
            draw_frame(canvas, row, column, garbage_frame, negative=True)
            row += speed
            obstacle.row = row
    finally:
        config.OBSTACLES.remove(obstacle)