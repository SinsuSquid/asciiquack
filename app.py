from typing import List, Tuple
from duck import Duck

class App:
    def __init__(self):
        self.messages: List[Tuple[str, str]] = [("Duck", "Quack! Welcome to asciiquack!")]
        self.input_buffer: str = ""
        self.running: bool = True
        self.duck = Duck(10, 15)  # Start deeper to avoid "flying"
        self.color: str = "yellow"
        self.colors = ["yellow", "cyan", "magenta", "green", "red", "white"]
        self.hats = ["None", "Top Hat", "Cap", "Flower"]
        self.hat_idx = 0
        self.hat = "None"
        self.breadcrumbs: List[Tuple[int, int]] = []

    def cycle_hat(self):
        self.hat_idx = (self.hat_idx + 1) % len(self.hats)
        self.hat = self.hats[self.hat_idx]
        self.add_message("System", f"Duck is now wearing: {self.hat}!")

    def cycle_color(self):
        current_idx = self.colors.index(self.color)
        self.color = self.colors[(current_idx + 1) % len(self.colors)]
        self.add_message("System", f"Duck changed color to {self.color}!")

    def feed(self):
        import random
        bx = int(self.duck.x) + random.randint(-5, 15)
        by = int(self.duck.y) + random.randint(-2, 5)
        self.breadcrumbs.append((bx, by))
        if len(self.breadcrumbs) > 20:
            self.breadcrumbs.pop(0)
        self.add_message("Duck", "Quack! (Happy munching)")

    def add_message(self, sender: str, text: str):
        self.messages.append((sender, text))
        if len(self.messages) > 20:
            self.messages.pop(0)

    def update(self, width: int, height: int):
        # Update animation
        self.duck.update(width, height)
        
        # Check for eaten breadcrumbs
        # A breadcrumb is eaten if it's within the duck's body
        dx = int(self.duck.x)
        dy = int(self.duck.y)
        
        # We'll use a slightly smaller hitbox for "eating" to make it look natural
        hitbox_width = self.duck.width
        hitbox_height = self.duck.height
        
        remaining_crumbs = []
        eaten_some = False
        for bx, by in self.breadcrumbs:
            if dx <= bx < dx + hitbox_width and dy <= by < dy + hitbox_height:
                eaten_some = True
                continue
            remaining_crumbs.append((bx, by))
        
        self.breadcrumbs = remaining_crumbs
        if eaten_some:
            self.process_quack("munch munch!")

    def handle_input(self, char: str):
        if char == "\t":  # TAB
            self.cycle_color()
        elif char.lower() == "h" and not self.input_buffer:
            self.cycle_hat()
        elif char.lower() == "f" and not self.input_buffer:
            self.feed()
        elif char == "\r" or char == "\n":
            if self.input_buffer.strip():
                self.add_message("You", self.input_buffer)
                self.process_quack(self.input_buffer)
                self.input_buffer = ""
        elif char == "\x7f" or char == "\x08":  # Backspace
            self.input_buffer = self.input_buffer[:-1]
        elif len(char) == 1 and char.isprintable():
            self.input_buffer += char

    def process_quack(self, user_msg: str):
        import random
        
        quacks = ["Quack!", "Quack quack.", "QUACK!", "Quack?", "Quack...", "Quack! ✨"]
        
        if "?" in user_msg:
            response = random.choice(["Quack?", "Quack quack?", "Quack... quack?"])
        elif "!" in user_msg or user_msg.isupper():
            response = random.choice(["QUACK!!", "QUACK!", "Quack quack quack!!!"])
        elif len(user_msg) > 50:
            response = "Quack... (nodding)"
        else:
            response = random.choice(quacks)
            
        self.add_message("Duck", response)
