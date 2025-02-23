import threading
import curses
import time
import os

columns, lines = os.get_terminal_size()
ACTIVE = True
uniRender = []

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.curs_set(0)

def render():
	stdscr.clear()
	try:
		for priority in reversed(uniRender):
			for toRender in priority:
				toRender[3](toRender[0], toRender[1], toRender[2])
	except curses.error:
		pass
	time.sleep(0.01)
	stdscr.refresh()
	
def arRender(posY, posX, context, cType=0, priority=0, state=0):
	if state == 0:
		while priority >= len(uniRender):
			uniRender.append([])
		if cType == 0 and len(context) <= 1:
			uniRender[priority].append([posY, posX, context, stdscr.addch, state])
		elif cType == 1 or len(context) > 1:
			uniRender[priority].append([posY, posX, context, stdscr.addstr, state])

arRender(lines // 2, columns // 2, "New Game")
arRender(lines // 2 + 1, columns // 2, "Continue")
arRender(lines // 2 + 2, columns // 2, "Settings")
try:
	while ACTIVE:
		render()
except Exception as e:
	curses.echo()
	curses.nocbreak()
	stdscr.keypad(False)
	curses.endwin()
	curses.curs_set(1)
	raise e