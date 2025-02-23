import curses

def main(stdscr):
    # Clear screen
    stdscr.clear()
    
    # Define the prompt and input positions
    max_y, max_x = stdscr.getmaxyx()
    prompt_y = max_y // 2 - 1
    prompt_x = max_x // 2 - 10
    input_y = prompt_y + 1
    input_x = prompt_x
    
    # Display the prompt
    stdscr.addstr(prompt_y, prompt_x, "Enter your name:")
    
    # Define the default text and set initial values
    default_text = "alan"
    max_length = 20
    stdscr.addstr(input_y, input_x, default_text)
    current_text = list(default_text)
    cursor_pos = len(default_text)  # Start cursor after the default text

    # Main loop to handle character-by-character input
    while True:
        stdscr.move(input_y, input_x + cursor_pos)  # Move cursor to current position
        stdscr.refresh()
        
        key = stdscr.getch()  # Get the next character entered by the user

        if key == curses.KEY_BACKSPACE or key == 127:  # Handle backspace
            if cursor_pos > 0:
                del current_text[cursor_pos - 1]  # Remove character to the left
                cursor_pos -= 1
        elif key == curses.KEY_LEFT:  # Move cursor left
            if cursor_pos > 0:
                cursor_pos -= 1
        elif key == curses.KEY_RIGHT:  # Move cursor right
            if cursor_pos < len(current_text):
                cursor_pos += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:  # Handle Enter
            break
        elif 32 <= key <= 126 and len(current_text) < max_length:  # Handle printable characters
            current_text.insert(cursor_pos, chr(key))
            cursor_pos += 1

        # Redraw the input line with current text and clear any excess
        stdscr.addstr(input_y, input_x, "".join(current_text) + " " * (max_length - len(current_text)))
    
    # Final input
    user_input = "".join(current_text)
    
    # Display the input back to the user for confirmation
    stdscr.addstr(input_y + 2, input_x, f"You entered: {user_input}")
    stdscr.refresh()
    stdscr.getch()  # Wait for user to see the result

# Run the curses application
curses.wrapper(main)
