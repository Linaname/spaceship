import asyncio
import curses


async def blink(canvas, row, column, symbol='*', initial_state=0):
    i = initial_state%31
    while True:
        if i < 20:
            canvas.addstr(row, column, symbol, curses.A_DIM)
        elif i < 23:
            canvas.addstr(row, column, symbol)
        elif i < 28:
            canvas.addstr(row, column, symbol, curses.A_BOLD)
        elif i < 31:
            canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)
        i = (i + 1)%31
