import sys
import time
import tty
import termios
import select
import os
import random
from contextlib import contextmanager
from app import App
from ui import render_frame, CLEAR_SCREEN, HIDE_CURSOR, SHOW_CURSOR, CURSOR_HOME

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
    
    # Initial setup
    sys.stdout.write(CLEAR_SCREEN + HIDE_CURSOR + CURSOR_HOME)
    sys.stdout.flush()

    try:
        with raw_mode(sys.stdin):
            while app.running:
                # Get terminal size
                size = os.get_terminal_size()
                width, height = size.columns, size.lines

                # Randomly change target
                if random.random() < 0.01:
                    app.duck.target_x = random.uniform(0, width - app.duck.width)
                    anim_height = (height * 3) // 4
                    app.duck.target_y = random.uniform(anim_height // 2 - 2, anim_height - app.duck.height)

                # Update animation
                app.duck.update(width, height)

                # Handle input
                while True:
                    char = get_char_non_blocking()
                    if char is None:
                        break
                    if char == "\x1b":  # ESC
                        app.running = False
                        break
                    else:
                        app.handle_input(char)
                
                # Update UI
                render_frame(app, width, height)
                
                time.sleep(0.05)
    finally:
        # Cleanup
        sys.stdout.write(SHOW_CURSOR + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
