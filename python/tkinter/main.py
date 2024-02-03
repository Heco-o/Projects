import tkinter as tk

def move_ball():
    global x, y, x_speed, y_speed

    # Move the ball
    canvas.move(ball, x_speed, y_speed)

    # Get the current position of the ball
    x1, y1, x2, y2 = canvas.coords(ball)

    # Bounce off the walls
    if x1 <= 0 or x2 >= canvas_width:
        x_speed = -x_speed

    if y1 <= 0 or y2 >= canvas_height:
        y_speed = -y_speed

    # Call this function again after 10 milliseconds
    root.after(10, move_ball)

# Create the main window
root = tk.Tk()
root.title("Bouncing Ball")

# Create a Canvas widget
canvas_width = 400
canvas_height = 300
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

# Initial position and speed of the ball
x = 50
y = 50
x_speed = 2
y_speed = 2

# Create a ball on the canvas
ball_radius = 20
ball = canvas.create_oval(x, y, x + ball_radius*2, y + ball_radius*2, fill="blue")

# Start the ball animation
move_ball()

# Start the Tkinter event loop
root.mainloop()