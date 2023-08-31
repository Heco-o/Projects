import time
import threading
from contextlib import contextmanager

class LoadingAnimation:
	def __init__(self):
		self.animation = ["Please wait	", "Please wait.   ", "Please wait..  ", "Please wait... ", "Please wait...."]
		self.index = 0
		self._running = threading.Event()

	def _animate(self):
		while self._running.is_set():
			print(self.animation[self.index % 5], end="\r")
			self.index += 1
			time.sleep(0.2)

	@contextmanager
	def start(self):
		self._running.set()
		animation_thread = threading.Thread(target=self._animate)
		animation_thread.start()
		sTime = time.time()
		try:
			yield
		finally:
			eTime = time.time()
			self._running.clear()
			animation_thread.join()
			print("\rSuccessfully Imported! " + str(eTime - sTime) + "s")

with LoadingAnimation().start():
	try:
		import sympyi
	except ModuleNotFoundError:
		print("sympy module is required\nrun 'pip3 install sympy' to download the module")
		exit()
	import decimal