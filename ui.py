from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.console import Console, Group
from app import App

def make_layout() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="upper", ratio=3),
        Layout(name="lower", ratio=1)
    )
    layout["upper"].split_row(
        Layout(name="animation", ratio=2),
        Layout(name="chat", ratio=1)
    )
    layout["lower"].split_column(
        Layout(name="input")
    )
    return layout

def draw_duck(app: App, width: int, height: int) -> Text:
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
    # Duck floats on the waves, so we bob its Y based on time
    import math
    bob = math.sin(app.duck.tick * 0.2)
    y = int(app.duck.y + bob)
    
    # Adjust y for hat height
    hat_height = len(duck_art) - 4
    y = max(0, y - hat_height)
    
    text = Text()
    crumbs = set(app.breadcrumbs)

    # We'll fill the bottom of the pane with "waves"
    wave_chars = ["~", "≈", "∽"]
    
    for row_idx in range(height):
        # Is this a "water" row? (Bottom half)
        is_water = row_idx >= (height // 2)
        
        # If the duck is on this row, overlay it
        if y <= row_idx < y + len(duck_art):
            duck_row = duck_art[row_idx - y]
            
            # Clipping
            if x < 0:
                duck_row = duck_row[-x:]
                display_x = 0
            else:
                display_x = x
            if display_x + len(duck_row) > width:
                duck_row = duck_row[:width - display_x]
            
            row_chars = []
            for col_idx in range(display_x):
                if (col_idx, row_idx) in crumbs:
                    row_chars.append(".")
                elif is_water:
                    phase = (col_idx + app.duck.tick) // 5
                    row_chars.append(wave_chars[phase % len(wave_chars)])
                else:
                    row_chars.append(" ")
            
            prefix = "".join(row_chars)
            text.append(prefix, style="cyan" if is_water else "yellow")
            text.append(duck_row, style=app.color)
            
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
            text.append("".join(suffix_chars) + "\n", style="cyan" if is_water else "yellow")
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
            text.append("".join(row_chars) + "\n", style="cyan" if is_water else "yellow")
    return text

def update_layout(layout: Layout, app: App, width: int, height: int):
    # Animation area
    layout["animation"].update(
        Panel(draw_duck(app, width, height), title="Quack View", border_style="blue")
    )
    
    # Chat area
    chat_content = Text()
    for sender, msg in app.messages:
        style = "bold yellow" if sender == "Duck" else "bold green"
        chat_content.append(f"{sender}: ", style=style)
        chat_content.append(f"{msg}\n", style="white")
    
    layout["chat"].update(
        Panel(chat_content, title="Duck Chat", border_style="magenta")
    )
    
    # Input area
    footer = " (ESC: Quit | TAB: Color | H: Hat | F: Feed)"
    layout["input"].update(
        Panel(Text(app.input_buffer + "█", style="white"), title="Talk to Duck" + footer, border_style="green")
    )
