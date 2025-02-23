import curses
print(curses.KEY_UP)
scr = curses.initscr()
curses.noecho()
curses.cbreak()
scr.keypad(True)
curses.endwin()
import os
print(os.get_terminal_size())