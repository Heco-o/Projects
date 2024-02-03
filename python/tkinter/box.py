import tkinter as tk

class MovingBoxApp:
	def __init__(self, master):
		self.master = master
		self.master.title("Moving Box App")

		# Set initial box position
		self.box_x = 50
		self.box_y = 50

		# Create canvas
		self.canvas = tk.Canvas(master, width=400, height=300, bg="white")
		self.canvas.pack()

		# Create box
		self.box = self.canvas.create_rectangle(
			self.box_x, self.box_y, self.box_x + 50, self.box_y + 50, fill="blue"
		)

		# Bind arrow key events
		master.bind("<Left>", self.move_left)
		master.bind("<Right>", self.move_right)
		master.bind("<Up>", self.move_up)
		master.bind("<Down>", self.move_down)

	def move_left(self, event):
		self.move_box(-10, 0)

	def move_right(self, event):
		self.move_box(10, 0)

	def move_up(self, event):
		self.move_box(0, -10)

	def move_down(self, event):
		self.move_box(0, 10)

	def move_box(self, dx, dy):
		self.box_x += dx
		self.box_y += dy
		self.canvas.coords(self.box, self.box_x, self.box_y, self.box_x + 50, self.box_y + 50)

if __name__ == "__main__":
	root = tk.Tk()
	app = MovingBoxApp(root)
	root.mainloop()