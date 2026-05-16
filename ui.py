import math
from app import App

# ANSI Escape Sequences
CLEAR_SCREEN = "\033[2J"
CURSOR_HOME = "\033[H"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
RESET_COLOR = "\033[0m"
ALT_SCREEN_ON = "\033[?1049h"
ALT_SCREEN_OFF = "\033[?1049l"
DISABLE_WRAP = "\033[7l"
ENABLE_WRAP = "\033[7h"
CLEAR_LINE = "\033[K"

def move_to(row: int, col: int) -> str:
    return f"\033[{row};{col}H"

COLORS = {
    "yellow": "\033[33m",
    "cyan": "\033[36m",
    "magenta": "\033[35m",
    "green": "\033[32m",
    "red": "\033[31m",
    "white": "\033[37m",
    "bold": "\033[1m",
}

def draw_animal(app: App, width: int, height: int) -> str:
    animal_art = app.animal.get_art().copy()
    
    # Add hat if any
    if app.hat == "Top Hat":
        animal_art.insert(0, "      _|_")
        animal_art.insert(1, "     |___|")
    elif app.hat == "Cap":
        animal_art.insert(0, "      ___/")
    elif app.hat == "Flower":
        animal_art.insert(0, "       🌸")

    x = int(app.animal.x)
    bob = math.sin(app.animal.tick * 0.2)
    y = int(app.animal.y + bob)
    
    # Original art height is 4
    hat_height = len(animal_art) - 4
    y = max(0, y - hat_height)
    
    crumbs = set(app.breadcrumbs)
    wave_chars = ["~", "≈", "∽"]
    
    animal_color = COLORS.get(app.color, COLORS["yellow"])
    water_color = COLORS["cyan"]
    
    frame_lines = []
    
    # Use height - 1 to be absolutely safe
    height = height - 1
    anim_height = (height * 3) // 4
    
    wave_surface_base = anim_height // 2

    for row_idx in range(anim_height):
        row_str = ""
        animal_row = None
        if y <= row_idx < y + len(animal_art):
            animal_row = animal_art[row_idx - y]

        for col_idx in range(width):
            # Wave surface undulates per-column
            wave_offset = int(math.sin(col_idx * 0.1 + app.animal.tick * 0.15) * 2)
            is_water = row_idx >= wave_surface_base + wave_offset
            color = water_color if is_water else COLORS["yellow"]

            # Background character
            if (col_idx, row_idx) in crumbs:
                bg_char = "."
            elif is_water:
                bg_char = wave_chars[(col_idx + app.animal.tick) // 5 % len(wave_chars)]
            else:
                bg_char = " "

            # Animal character?
            if animal_row is not None and x <= col_idx < x + len(animal_row):
                animal_char = animal_row[col_idx - x]
                if animal_char == "·":
                    row_str += animal_color + " " + RESET_COLOR
                elif animal_char != " ":
                    row_str += animal_color + animal_char + RESET_COLOR
                else:
                    row_str += color + bg_char + RESET_COLOR
            else:
                row_str += color + bg_char + RESET_COLOR

        frame_lines.append(row_str)

    # Chat area
    chat_height = height - anim_height - 4
    if chat_height < 1:
        anim_height = max(1, height - 5)
        chat_height = 1

    frame_lines.append(COLORS["magenta"] + "─" * width + RESET_COLOR)

    recent_msgs = app.messages[-chat_height:]
    for i in range(chat_height):
        if i < len(recent_msgs):
            sender, msg = recent_msgs[i]
            # Color based on sender
            if sender == "System":
                s_color = COLORS["magenta"]
            elif sender == "You":
                s_color = COLORS["white"]
            else:
                s_color = COLORS["green"] if sender == "Frog" else COLORS["yellow"]
                
            clean_msg = msg[:width - 15]
            line = f"{COLORS['bold']}{s_color}{sender}:{RESET_COLOR} {clean_msg}"
            frame_lines.append(line)
        else:
            frame_lines.append("")

    # Input area
    footer = " (ESC: Quit | TAB: Color | H: Hat | F: Feed | A: Animal) "
    frame_lines.append(COLORS["green"] + "─" * width + RESET_COLOR)

    prompt = f"Talk to {app.animal.name}: "
    max_input = width - len(prompt) - len(footer) - 2
    display_input = app.input_buffer[-max_input:] if len(app.input_buffer) > max_input else app.input_buffer
    input_line = f"{COLORS['white']}{prompt}{footer}{display_input}"
    frame_lines.append(input_line)

    return frame_lines[:height-1]

def render_frame(app: App, width: int, height: int):
    import sys
    sys.stdout.write(HIDE_CURSOR)
    
    lines = draw_animal(app, width, height)
    output = []
    for i, line in enumerate(lines):
        output.append(move_to(i + 1, 1) + line + CLEAR_LINE)
    
    last_line_idx = len(lines)
    footer = " (ESC: Quit | TAB: Color | H: Hat | F: Feed | A: Animal) "
    prompt = f"Talk to {app.animal.name}: "
    max_input = width - len(prompt) - len(footer) - 2
    display_input = app.input_buffer[-max_input:] if len(app.input_buffer) > max_input else app.input_buffer
    
    cursor_col = len(prompt) + len(footer) + len(display_input) + 1
    
    output.append(move_to(last_line_idx, cursor_col))
    output.append(SHOW_CURSOR)
    
    sys.stdout.write("".join(output))
    sys.stdout.flush()
