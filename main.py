import sys
import time
import tty
import termios
import select
from rich.live import Live
from rich.console import Console
from app import App
from ui import make_layout, update_layout

def get_char():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        if select.select([sys.stdin], [], [], 0.05)[0]:
            return sys.stdin.read(1)
        return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def main():
    app = App()
    layout = make_layout()
    console = Console()

    with Live(layout, refresh_per_second=20, screen=True, console=console) as live:
        while app.running:
            # Estimate bounds (animation is 2/3 width, 3/4 height)
            width = (console.width * 2) // 3 - 2 # -2 for borders
            height = (console.height * 3) // 4 - 2

            # Update animation
            app.duck.update(width, height)

            # Handle input
            char = get_char()
            if char:
                if char == "\x1b":  # ESC
                    app.running = False
                else:
                    app.handle_input(char)
            
            # Update UI
            update_layout(layout, app)
            time.sleep(0.05)

if __name__ == "__main__":
    main()
