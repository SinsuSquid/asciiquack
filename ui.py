import math
from app import App

# ANSI Escape Sequences
CLEAR_SCREEN = "\033[2J"
CURSOR_HOME = "\033[H"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
RESET_COLOR = "\033[0m"

COLORS = {
    "yellow": "\033[33m",
    "cyan": "\033[36m",
    "magenta": "\033[35m",
    "green": "\033[32m",
    "red": "\033[31m",
    "white": "\033[37m",
    "bold": "\033[1m",
}

def draw_duck(app: App, width: int, height: int) -> str:
    duck_art = app.duck.get_art().copy()
    
    # Add hat if any
    if app.hat == "Top Hat":
        duck_art.insert(0, "      _|_")
        duck_art.insert(1, "     |___|")
    elif app.hat == "Cap":
        duck_art.insert(0, "      ___/")
    elif app.hat == "Flower":
        duck_art.insert(0, "       🌸")

    x = int(app.duck.x)
    bob = math.sin(app.duck.tick * 0.2)
    y = int(app.duck.y + bob)
    
    hat_height = len(duck_art) - 4
    y = max(0, y - hat_height)
    
    crumbs = set(app.breadcrumbs)
    wave_chars = ["~", "≈", "∽"]
    
    duck_color = COLORS.get(app.color, COLORS["yellow"])
    water_color = COLORS["cyan"]
    
    frame_lines = []
    
    # Layout Split: Animation (2/3 height), Chat/Input (1/3 height)
    anim_height = (height * 3) // 4
    
    for row_idx in range(anim_height):
        is_water = row_idx >= (anim_height // 2)
        color = water_color if is_water else COLORS["yellow"]
        
        row_str = ""
        
        if y <= row_idx < y + len(duck_art):
            duck_row = duck_art[row_idx - y]
            
            # Clipping/Positioning
            display_x = max(0, x)
            if x < 0:
                duck_row = duck_row[-x:]
            if display_x + len(duck_row) > width:
                duck_row = duck_row[:width - display_x]
            
            # Prefix (background/water/crumbs)
            prefix_chars = []
            for col_idx in range(display_x):
                if (col_idx, row_idx) in crumbs:
                    prefix_chars.append(".")
                elif is_water:
                    phase = (col_idx + app.duck.tick) // 5
                    prefix_chars.append(wave_chars[phase % len(wave_chars)])
                else:
                    prefix_chars.append(" ")
            
            row_str += color + "".join(prefix_chars) + RESET_COLOR
            row_str += duck_color + duck_row + RESET_COLOR
            
            # Suffix
            suffix_start = display_x + len(duck_row)
            suffix_chars = []
            for col_idx in range(suffix_start, width):
                if (col_idx, row_idx) in crumbs:
                    suffix_chars.append(".")
                elif is_water:
                    phase = (col_idx + app.duck.tick) // 5
                    suffix_chars.append(wave_chars[phase % len(wave_chars)])
                else:
                    suffix_chars.append(" ")
            row_str += color + "".join(suffix_chars) + RESET_COLOR
        else:
            row_chars = []
            for col_idx in range(width):
                if (col_idx, row_idx) in crumbs:
                    row_chars.append(".")
                elif is_water:
                    phase = (col_idx + app.duck.tick) // 5
                    row_chars.append(wave_chars[phase % len(wave_chars)])
                else:
                    row_chars.append(" ")
            row_str += color + "".join(row_chars) + RESET_COLOR
        
        frame_lines.append(row_str)

    # Chat area
    chat_height = height - anim_height - 2 # -2 for input box
    frame_lines.append(COLORS["magenta"] + "─" * width + RESET_COLOR)
    
    recent_msgs = app.messages[-chat_height:]
    for i in range(chat_height):
        if i < len(recent_msgs):
            sender, msg = recent_msgs[i]
            s_color = COLORS["yellow"] if sender == "Duck" else COLORS["green"]
            line = f"{COLORS['bold']}{s_color}{sender}:{RESET_COLOR} {msg}"
            # Truncate if too long
            frame_lines.append(line[:width + 10]) # +10 for ANSI codes
        else:
            frame_lines.append("")

    # Input area
    footer = " (ESC: Quit | TAB: Color | H: Hat | F: Feed)"
    frame_lines.append(COLORS["green"] + "─" * width + RESET_COLOR)
    input_line = f"{COLORS['white']}Talk to Duck{footer}: {app.input_buffer}█"
    frame_lines.append(input_line[:width + 20])

    return "\n".join(frame_lines)

def render_frame(app: App, width: int, height: int):
    frame = draw_duck(app, width, height)
    # Move cursor to home and print the entire frame at once
    sys.stdout.write(CURSOR_HOME + frame)
    sys.stdout.flush()

import sys
