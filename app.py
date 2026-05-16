from typing import List, Tuple, Union
import random
from frog import Frog
from duck import Duck
from cloud import Cloud
from sun import Sun

class App:
    def __init__(self):
        self.messages: List[Tuple[str, str]] = []
        self.input_buffer: str = ""
        self.running: bool = True
        
        # Available animals
        self.available_animals = [Duck, Frog]
        self.animal_idx = 0
        self.animal = self.available_animals[self.animal_idx](10, 15)
        
        # Initial greeting
        self.add_message(self.animal.name, f"{self.animal.sound}! Welcome to the pond!")

        self.color: str = "green" if self.animal.name == "Frog" else "yellow"
        self.colors = ["green", "yellow", "cyan", "magenta", "red", "white"]
        self.hats = ["None", "Top Hat", "Cap", "Flower"]
        self.hat_idx = 0
        self.hat = "None"
        self.breadcrumbs: List[Tuple[int, int]] = []
        
        # Clouds in the sky
        self.clouds: List[Cloud] = []
        for _ in range(3):
            self.clouds.append(Cloud(random.uniform(0, 80), random.uniform(0, 5)))
            
        # The Sun
        self.sun = Sun(60, 1)

    def toggle_animal(self):
        # Save current position
        x, y = self.animal.x, self.animal.y
        
        self.animal_idx = (self.animal_idx + 1) % len(self.available_animals)
        self.animal = self.available_animals[self.animal_idx](x, y)
        
        # Update default color if it matches the previous default
        if self.animal.name == "Frog":
            self.color = "green"
        else:
            self.color = "yellow"
            
        self.add_message("System", f"Switched to: {self.animal.name}!")
        self.add_message(self.animal.name, f"{self.animal.sound}!")

    def cycle_hat(self):
        self.hat_idx = (self.hat_idx + 1) % len(self.hats)
        self.hat = self.hats[self.hat_idx]
        self.add_message("System", f"{self.animal.name} is now wearing: {self.hat}!")

    def cycle_color(self):
        current_idx = self.colors.index(self.color)
        self.color = self.colors[(current_idx + 1) % len(self.colors)]
        self.add_message("System", f"{self.animal.name} changed color to {self.color}!")

    def feed(self, width: int, height: int):
        import random
        anim_height = (height * 3) // 4
        water_line = anim_height // 2
        
        # Spawn breadcrumbs only in the water area
        bx = random.randint(0, width - 1)
        by = random.randint(water_line, anim_height - 1)
        
        self.breadcrumbs.append((bx, by))
        if len(self.breadcrumbs) > 20:
            self.breadcrumbs.pop(0)
        self.add_message(self.animal.name, f"{self.animal.sound}! (Happy munching)")

    def add_message(self, sender: str, text: str):
        self.messages.append((sender, text))
        if len(self.messages) > 20:
            self.messages.pop(0)

    def update(self, width: int, height: int):
        # Update animation
        self.animal.update(width, height)
        
        # Update clouds
        for cloud in self.clouds:
            cloud.update(width)
            
        # Update sun
        self.sun.update()
        
        # Check for eaten breadcrumbs
        ax = int(self.animal.x)
        ay = int(self.animal.y)
        
        hitbox_width = self.animal.width
        hitbox_height = self.animal.height
        
        remaining_crumbs = []
        eaten_some = False
        for bx, by in self.breadcrumbs:
            if ax <= bx < ax + hitbox_width and ay <= by < ay + hitbox_height:
                eaten_some = True
                continue
            remaining_crumbs.append((bx, by))
        
        self.breadcrumbs = remaining_crumbs
        if eaten_some:
            self.process_sound("munch munch!")

    def handle_input(self, char: str, width: int, height: int):
        if char == "\t":  # TAB
            self.cycle_color()
        elif char.lower() == "h" and not self.input_buffer:
            self.cycle_hat()
        elif char.lower() == "f" and not self.input_buffer:
            self.feed(width, height)
        elif char.lower() == "a" and not self.input_buffer:
            self.toggle_animal()
        elif char == "\r" or char == "\n":
            if self.input_buffer.strip():
                self.add_message("You", self.input_buffer)
                self.process_sound(self.input_buffer)
                self.input_buffer = ""
        elif char == "\x7f" or char == "\x08":  # Backspace
            self.input_buffer = self.input_buffer[:-1]
        elif len(char) == 1 and char.isprintable():
            self.input_buffer += char

    def process_sound(self, user_msg: str):
        import random
        
        sound = self.animal.sound
        sounds = [f"{sound}!", f"{sound} {sound.lower()}.", f"{sound.upper()}!", f"{sound}?", f"{sound}...", f"{sound}! ✨"]
        
        if "?" in user_msg:
            response = random.choice([f"{sound}?", f"{sound} {sound.lower()}?", f"{sound}... {sound.lower()}?"])
        elif "!" in user_msg or user_msg.isupper():
            response = random.choice([f"{sound.upper()}!!", f"{sound.upper()}!", f"{sound} {sound.lower()} {sound.lower()}!!!"])
        elif len(user_msg) > 50:
            response = f"{sound}... (nodding)"
        else:
            response = random.choice(sounds)
            
        self.add_message(self.animal.name, response)
