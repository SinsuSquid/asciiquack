import math
from typing import List

class Duck:
    ART_RIGHT = [
        "      __",
        "    <(o )___",
        "     ( ._> /",
        "      `---'"
    ]
    
    ART_LEFT = [
        "      __",
        "   ___( o)>",
        "   \\ <_. )",
        "    `---'"
    ]

    def __init__(self, x: int, y: int):
        self.x = float(x)
        self.y = float(y)
        self.target_x = float(x)
        self.target_y = float(y)
        self.width = 12
        self.height = 4
        self.facing_right = True
        self.tick = 0

    def update(self, bounds_width: int, bounds_height: int):
        self.tick += 1
        
        # Gentle floating bobbing effect
        bob_y = math.sin(self.tick * 0.1) * 0.5
        
        # Drift slowly towards target
        dx = (self.target_x - self.x) * 0.05
        dy = (self.target_y - self.y) * 0.05
        
        self.x += dx
        self.y += dy + (bob_y * 0.1) # Add a tiny bit of bob to the actual pos

        # Ensure facing direction matches movement
        if dx > 0.01:
            self.facing_right = True
        elif dx < -0.01:
            self.facing_right = False

        # Keep duck within logical bounds but don't "bounce"
        self.x = max(0, min(self.x, bounds_width - self.width))
        self.y = max(0, min(self.y, bounds_height - self.height))

    def get_art(self) -> List[str]:
        return self.ART_RIGHT if self.facing_right else self.ART_LEFT
