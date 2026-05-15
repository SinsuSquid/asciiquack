import sys
import time
import tty
import termios
import select
from contextlib import contextmanager
from rich.live import Live
from rich.console import Console
from app import App
from ui import make_layout, update_layout

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
    layout = make_layout()
    console = Console()
    import random

    with raw_mode(sys.stdin):
        with Live(layout, refresh_per_second=20, screen=True, console=console) as live:
            while app.running:
                # Get actual dimensions of the 'animation' pane
                try:
                    region_map = layout.map(console)
                    animation_pane = layout["animation"]
                    region = region_map[animation_pane]
                    width = region.width - 2
                    height = region.height - 2
                except Exception:
                    width = (console.width * 2) // 3 - 2
                    height = (console.height * 3) // 4 - 2

                width = max(1, width)
                height = max(1, height)

                # Randomly change target to simulate "swimming around"
                if random.random() < 0.01:
                    app.duck.target_x = random.uniform(0, width - app.duck.width)
                    # Stay roughly in the water area (bottom half)
                    app.duck.target_y = random.uniform(height // 2 - 2, height - app.duck.height)

                # Update animation
                app.duck.update(width, height)

                # Handle input (collect all available chars to keep it responsive)
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
                update_layout(layout, app, width, height)
                
                # Small sleep to prevent 100% CPU, but much smaller than before
                # to stay responsive and smooth.
                time.sleep(0.01)

if __name__ == "__main__":
    main()
