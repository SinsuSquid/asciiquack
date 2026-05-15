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
        duck_row = None
        if y <= row_idx < y + len(duck_art):
            duck_row = duck_art[row_idx - y]
        
        for col_idx in range(width):
            # Background character
            if (col_idx, row_idx) in crumbs:
                bg_char = "."
            elif is_water:
                bg_char = wave_chars[(col_idx + app.duck.tick) // 5 % len(wave_chars)]
            else:
                bg_char = " "
            
            # Duck character?
            if duck_row is not None and x <= col_idx < x + len(duck_row):
                duck_char = duck_row[col_idx - x]
                # If it's our solid-space placeholder, turn it into a real space!
                if duck_char == "·":
                    row_str += duck_color + " " + RESET_COLOR
                # Only real spaces from the art box are transparent!
                elif duck_char != " ":
                    row_str += duck_color + duck_char + RESET_COLOR
                else:
                    row_str += color + bg_char + RESET_COLOR
            else:
                row_str += color + bg_char + RESET_COLOR
        
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
    input_line = f"{COLORS['white']}Talk to Duck{footer}: {display_input}"
    frame_lines.append(input_line)

    # Return exactly height-1 lines to avoid triggering a scroll
    return frame_lines[:height-1]

def render_frame(app: App, width: int, height: int):
    # Hide cursor while drawing to avoid "ghosting"
    sys.stdout.write(HIDE_CURSOR)
    
    lines = draw_duck(app, width, height)
    output = []
    for i, line in enumerate(lines):
        # Move to exactly row i+1, column 1, print line, then clear rest of line
        output.append(move_to(i + 1, 1) + line + CLEAR_LINE)
    
    # Calculate cursor position at the end of the input line
    # The input line is the last line in our list
    last_line_idx = len(lines)
    footer = " (ESC: Q | TAB: C | H: H | F: F)"
    # Length of "Talk to Duck" + footer + ": " + display_input
    # We need to be careful with display_input truncation again
    max_input = width - len("Talk to Duck: ") - len(footer) - 2
    display_input = app.input_buffer[-max_input:] if len(app.input_buffer) > max_input else app.input_buffer
    
    cursor_col = len("Talk to Duck") + len(footer) + len(": ") + len(display_input) + 1
    
    # Move to the input position and show the cursor
    output.append(move_to(last_line_idx, cursor_col))
    output.append(SHOW_CURSOR)
    
    sys.stdout.write("".join(output))
    sys.stdout.flush()

import sys
