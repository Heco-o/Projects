import curses
import time

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.timeout(100)  # Set the delay for getch() in milliseconds

    # Set up the initial positions
    paddle_height, paddle_width = 1, 5
    paddle1_y, paddle2_y = 0, 0
    ball_y, ball_x = 5, 10
    ball_speed_y, ball_speed_x = 1, 1

    while True:
        # Get screen dimensions
        max_y, max_x = stdscr.getmaxyx()

        # Clear the screen
        stdscr.clear()

        # Draw paddles
        stdscr.addch(paddle1_y, 0, '|')
        stdscr.addch(paddle1_y, paddle_width - 1, '|')

        stdscr.addch(paddle2_y, max_x - 1, '|')
        stdscr.addch(paddle2_y, max_x - 1 - paddle_width + 1, '|')

        # Draw ball
        stdscr.addch(ball_y, ball_x, '*')

        # Move paddles
        key = stdscr.getch()
        if key == curses.KEY_UP and paddle2_y > 0:
            paddle2_y -= 1
        elif key == curses.KEY_DOWN and paddle2_y < max_y - 1:
            paddle2_y += 1

        if ball_y + ball_speed_y > 0 and ball_y + ball_speed_y < max_y - 1:
            ball_y += ball_speed_y
        else:
            ball_speed_y *= -1

        if ball_x + ball_speed_x > 0 and ball_x + ball_speed_x < max_x - 1:
            ball_x += ball_speed_x
        else:
            ball_speed_x *= -1

        # Check collision with paddles
        if ball_y == paddle1_y and 0 < ball_x < paddle_width - 1:
            ball_speed_x *= -1

        if ball_y == paddle2_y and max_x - 1 - paddle_width + 1 < ball_x < max_x - 1:
            ball_speed_x *= -1

        # Refresh the screen
        stdscr.refresh()

        time.sleep(0.1)

if __name__ == "__main__":
    curses.wrapper(main)
