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
    y = int(app.duck.y)
    
    # Adjust y for hat height
    hat_height = len(duck_art) - 4
    y = max(0, y - hat_height)
    
    # Create a grid for the animation area
    lines = [[" " for _ in range(width)] for _ in range(height)]
    
    # Draw breadcrumbs
    for bx, by in app.breadcrumbs:
        if 0 <= bx < width and 0 <= by < height:
            lines[by][bx] = "."

    # Draw duck onto grid (simplified for now, just text is easier)
    text = Text()
    for row_idx in range(height):
        row_text = "".join(lines[row_idx])
        # If the duck is on this row, overlay it
        if y <= row_idx < y + len(duck_art):
            duck_row = duck_art[row_idx - y]
            # Overlay duck_row onto row_text at position x
            prefix = row_text[:x]
            suffix = row_text[x + len(duck_row):]
            text.append(prefix)
            text.append(duck_row, style=app.color)
            text.append(suffix + "\n")
        else:
            text.append(row_text + "\n", style="yellow")
    return text

def update_layout(layout: Layout, app: App):
    # Animation area
    # We'll need the size to properly position the duck, but for now we'll guess or use fixed
    layout["animation"].update(
        Panel(draw_duck(app, 40, 15), title="Quack View", border_style="blue")
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
