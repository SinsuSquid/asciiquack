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
    hat_width_bonus = 0
    if app.hat == "Top Hat":
        duck_art.insert(0, "      _|_")
        duck_art.insert(1, "     |___|")
    elif app.hat == "Cap":
        duck_art.insert(0, "      ___/")
    elif app.hat == "Flower":
        duck_art.insert(0, "       🌸")
        # 🌸 is a wide char (2 columns), but len() is 1. We need to account for it!
        hat_width_bonus = 1

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
    
    # Use height - 1 to be absolutely safe
    height = height - 1
    anim_height = (height * 3) // 4
    
    for row_idx in range(anim_height):
        is_water = row_idx >= (anim_height // 2)
        color = water_color if is_water else COLORS["yellow"]
        
        row_str = ""
        
        if y <= row_idx < y + len(duck_art):
            duck_row = duck_art[row_idx - y]
            
            # Actual display width of the duck row
            display_width = len(duck_row) + (hat_width_bonus if row_idx == y and app.hat == "Flower" else 0)
            
            display_x = max(0, x)
            # Clip if needed (simplified)
            if display_x + display_width > width:
                duck_row = duck_row[:width - display_x - hat_width_bonus]
            
            # Fill before duck
            prefix = []
            for col_idx in range(display_x):
                if (col_idx, row_idx) in crumbs: prefix.append(".")
                elif is_water: prefix.append(wave_chars[(col_idx + app.duck.tick) // 5 % len(wave_chars)])
                else: prefix.append(" ")
            
            row_str += color + "".join(prefix) + RESET_COLOR
            row_str += duck_color + duck_row + RESET_COLOR
            
            # Fill after duck
            suffix_start = display_x + display_width
            suffix = []
            for col_idx in range(suffix_start, width):
                if (col_idx, row_idx) in crumbs: suffix.append(".")
                elif is_water: suffix.append(wave_chars[(col_idx + app.duck.tick) // 5 % len(wave_chars)])
                else: suffix.append(" ")
            row_str += color + "".join(suffix) + RESET_COLOR
        else:
            row = []
            for col_idx in range(width):
                if (col_idx, row_idx) in crumbs: row.append(".")
                elif is_water: row.append(wave_chars[(col_idx + app.duck.tick) // 5 % len(wave_chars)])
                else: row.append(" ")
            row_str += color + "".join(row) + RESET_COLOR
        
        frame_lines.append(row_str)

    # Chat area
    # Chat area
    # Subtracting 4: 2 for borders, 1 for input, 1 to avoid the very last terminal line
    chat_height = height - anim_height - 4
    if chat_height < 1:
        anim_height = max(1, height - 5)
        chat_height = 1

    frame_lines.append(COLORS["magenta"] + "─" * width + RESET_COLOR)

    recent_msgs = app.messages[-chat_height:]
    for i in range(chat_height):
        if i < len(recent_msgs):
            sender, msg = recent_msgs[i]
            s_color = COLORS["yellow"] if sender == "Duck" else COLORS["green"]
            # Basic truncation for chat messages (approximate due to ANSI)
            clean_msg = msg[:width - 10]
            line = f"{COLORS['bold']}{s_color}{sender}:{RESET_COLOR} {clean_msg}"
            frame_lines.append(line)
        else:
            frame_lines.append("")

    # Input area
    footer = " (ESC: Q | TAB: C | H: H | F: F)"
    frame_lines.append(COLORS["green"] + "─" * width + RESET_COLOR)

    # Truncate input to avoid wrapping
    max_input = width - len("Talk to Duck: ") - len(footer) - 2
    display_input = app.input_buffer[-max_input:] if len(app.input_buffer) > max_input else app.input_buffer
    input_line = f"{COLORS['white']}Talk to Duck{footer}: {display_input}█"
    frame_lines.append(input_line)

    # Return exactly height-1 lines to avoid triggering a scroll
    return "\n".join(frame_lines[:height-1])


def render_frame(app: App, width: int, height: int):
    frame = draw_duck(app, width, height)
    # Move cursor to home and print the entire frame at once
    sys.stdout.write(CURSOR_HOME + frame)
    sys.stdout.flush()

import sys
