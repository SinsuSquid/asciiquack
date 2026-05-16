import random
from typing import List

class Cloud:
    # Cartoon-style filled clouds
    ART = [
        "      .--.      ",
        "   .-(····).    ",
        "  (·········)   ",
        "   `-------'    "
    ]

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 4
        self.speed = random.uniform(0.02, 0.08)

    def update(self, screen_width: int):
        self.x -= self.speed
        # Reset if it goes off screen
        if self.x < -self.width:
            self.x = screen_width
            # Randomize speed and y a bit when recycling
            self.speed = random.uniform(0.02, 0.08)

    def get_art(self) -> List[str]:
        return self.ART
