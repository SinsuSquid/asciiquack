import sys
import time
import tty
import termios
import select
import os
import random
from contextlib import contextmanager
from app import App
from ui import render_frame, CLEAR_SCREEN, HIDE_CURSOR, SHOW_CURSOR, CURSOR_HOME, ALT_SCREEN_ON, ALT_SCREEN_OFF, DISABLE_WRAP, ENABLE_WRAP

@contextmanager
def raw_mode(file):
    old_attrs = termios.tcgetattr(file.fileno())
    try:
        tty.setraw(file.fileno())
        yield
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)

def get_char_non_blocking():
    if select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.read(1)
    return None

def main():
    app = App()
    
    # Initial setup: Use Alternate Screen, Hide Cursor, Disable Wrap, and Clear!
    sys.stdout.write(ALT_SCREEN_ON + HIDE_CURSOR + DISABLE_WRAP + CLEAR_SCREEN + CURSOR_HOME)
    sys.stdout.flush()

    try:
        with raw_mode(sys.stdin):
            while app.running:
                # Get terminal size
                size = os.get_terminal_size()
                width, height = size.columns, size.lines

                # Randomly change target to simulate "swimming around"
                if random.random() < 0.01:
                    app.duck.target_x = random.uniform(0, width - app.duck.width)
                    anim_height = (height * 3) // 4
                    # Duck is 4 rows high. anim_height // 2 is water line.
                    # We want at least the bottom 2 rows (index 2, 3) in water.
                    # So y + 2 >= anim_height // 2  => y >= anim_height // 2 - 2
                    min_y = anim_height // 2 - 2
                    max_y = anim_height - app.duck.height
                    app.duck.target_y = random.uniform(min_y, max_y)


                # Update animation and logic
                app.update(width, height)

                # Handle input
                while True:
                    char = get_char_non_blocking()
                    if char is None:
                        break
                    if char == "\x1b":  # ESC
                        app.running = False
                        break
                    else:
                        app.handle_input(char, width, height)
                
                # Update UI
                render_frame(app, width, height)
                
                # Use a slightly more precise sleep
                time.sleep(0.04)
    finally:
        # Cleanup: Re-enable wrap, show cursor, exit alternate screen
        sys.stdout.write(ENABLE_WRAP + SHOW_CURSOR + ALT_SCREEN_OFF)
        sys.stdout.flush()

if __name__ == "__main__":
    main()
