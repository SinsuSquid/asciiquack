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

# Background colors for solid-fill placeholders
BG_COLORS = {k: v.replace("[3", "[4") for k, v in COLORS.items() if k != "bold"}

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

    ax = int(app.animal.x)
    bob = math.sin(app.animal.tick * 0.2)
    ay = int(app.animal.y + bob)
    
    # Original art height is 4
    hat_height = len(animal_art) - 4
    ay = max(0, ay - hat_height)
    
    crumbs = set(app.breadcrumbs)
    wave_chars = ["~", "≈", "∽"]
    
    animal_color = COLORS.get(app.color, COLORS["yellow"])
    animal_bg = BG_COLORS.get(app.color, BG_COLORS["yellow"])
    water_color = COLORS["cyan"]
    cloud_color = COLORS["white"]
    cloud_bg = BG_COLORS["white"]
    sun_color = COLORS["yellow"]
    sun_bg = BG_COLORS["yellow"]
    
    frame_lines = []
    
    # Use height - 1 to be absolutely safe
    height = height - 1
    anim_height = (height * 3) // 4
    
    wave_surface_base = anim_height // 2

    for row_idx in range(anim_height):
        row_str = ""
        animal_row = None
        if ay <= row_idx < ay + len(animal_art):
            animal_row = animal_art[row_idx - ay]

        for col_idx in range(width):
            # 1. Animal character takes precedence
            if animal_row is not None and ax <= col_idx < ax + len(animal_row):
                animal_char = animal_row[col_idx - ax]
                if animal_char == "·":
                    row_str += animal_bg + " " + RESET_COLOR
                    continue
                elif animal_char != " ":
                    row_str += animal_color + animal_char + RESET_COLOR
                    continue

            # 2. Sun rendering
            sx, sy = app.sun.x, app.sun.y
            sart = app.sun.get_art()
            if sy <= row_idx < sy + len(sart) and sx <= col_idx < sx + len(sart[0]):
                sun_char = sart[row_idx - sy][col_idx - sx]
                if sun_char == "·":
                    row_str += sun_bg + " " + RESET_COLOR
                    continue
                elif sun_char != " ":
                    row_str += sun_color + sun_char + RESET_COLOR
                    continue

            # 3. Wave surface logic
            wave_offset = int(math.sin(col_idx * 0.1 + app.animal.tick * 0.15) * 2)
            is_water = row_idx >= wave_surface_base + wave_offset
            
            # 4. Cloud character
            cloud_char = None
            for cloud in app.clouds:
                cx = int(cloud.x)
                cy = int(cloud.y)
                cart = cloud.get_art()
                if cy <= row_idx < cy + len(cart) and cx <= col_idx < cx + len(cart[0]):
                    char = cart[row_idx - cy][col_idx - cx]
                    if char != " ":
                        cloud_char = char
                        break
            
            if cloud_char:
                if cloud_char == "·":
                    row_str += cloud_bg + " " + RESET_COLOR
                else:
                    row_str += cloud_color + cloud_char + RESET_COLOR
                continue

            # 5. Default background
            color = water_color if is_water else COLORS["yellow"]
            if (col_idx, row_idx) in crumbs:
                bg_char = "."
            elif is_water:
                bg_char = wave_chars[(col_idx + app.animal.tick) // 5 % len(wave_chars)]
            else:
                bg_char = " "
            
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
