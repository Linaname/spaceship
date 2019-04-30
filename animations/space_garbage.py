from curses_tools import draw_frame, get_frame_size
from obstacles import Obstacle
import game_state
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
    game_state.obstacles.append(obstacle)
    try:
        while row < rows_number:
            if obstacle in game_state.obstacles_in_last_collisions:
                game_state.obstacles_in_last_collisions.remove(obstacle)
                return
            draw_frame(canvas, row, column, garbage_frame)
            await asyncio.sleep(0)
            draw_frame(canvas, row, column, garbage_frame, negative=True)
            row += speed
            obstacle.row = row
    finally:
        game_state.obstacles.remove(obstacle)